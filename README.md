# Support Agent

A document-based conversational support agent using a Retrieval-Augmented Generation (RAG) architecture. It processes PDF documents into a vector database and provides a chat API to query them.

## Prerequisites

- Docker and Docker Compose
- API Keys:
  - OpenAI API Key (`OPENAI_API_KEY`)
  - Google Gemini API Key (`GOOGLE_API_KEY`)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Configure Environment Variables:**
   Create a `.env` file based on the example and fill in your API keys:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY and GOOGLE_API_KEY
   ```

3. **Data Processing (Ingestion):**
   The repository includes a script to process raw PDFs into the ChromaDB vector database.
   Using the Series 76 PDF file, you need to run the ingestion script via Docker:
   ```bash
   docker build -t rag-agent .
   docker run --rm -v $(pwd)/data:/app/data --env-file .env rag-agent python src/ingest.py --pdf data/input_ingest/series_76_tables.pdf
   ```
   This processes the PDF using Google Gemini Multimodal OCR, chunks the text, creates embeddings using OpenAI, and stores them in a local Chroma vector database inside the `data/vector_store` directory. This step is needed only when you add a new PDF to the knowledge base.

   The process finish when a similar message to the following is displayed:
   
   ```
   --- Ingestion Results ---
   Characters extracted: 14928
   Chunks generated: 17
   Embeddings generated: 17
   Vector Store (Chroma) ready: True
   -------------------------
   ```

## How to Run the Application

### Interactive Console Chat

Start a conversational session directly in your terminal:
```bash
docker-compose run --build chat
```
This opens an interactive REPL where you can type messages and receive responses from the agent. Type `exit` or `quit` to end the conversation.

### REST API

To start the API server instead:
```bash
docker-compose up --build api
```
- The API will be available at: `http://localhost:8000`
- Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`

## Usage

### Console Chat (recommended for conversations)

```
============================================================
  RAG Support Agent - Interactive Console Chat
  Type 'exit' or 'quit' to end the conversation.
============================================================

You: What is the Series 76?
Agent: The Series 76 is...

You: Tell me more about section 3
Agent: Section 3 covers...
```

### REST API

You can also test the chat endpoint using curl or through the Swagger UI:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/conversation' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What is the Series 76?"
}'
```

## Design Choices & Architecture

- **Ingestion Pipeline (Facade Pattern):** I used a sequential script (`ingest.py`) that uses `RAGIngestionPipeline` to process PDFs. It uses Google Gemini as an OCR engine to extract structured Markdown text from scanned or complex PDFs.
- **Vector Database:** I chose **ChromaDB** for storing embeddings locally. It is lightweight, file-based, and integrates perfectly with LangChain.
- **Agent Architecture:** The conversation API is powered by a LangChain `AgentExecutor` using the `create_tool_calling_agent` pattern. The agent is provided with a single tool (`query_knowledge_base`) that wraps the ChromaDB retriever. This allows the LLM to autonomously decide when and what to search in the knowledge base.
- **Singletons & Adapters:** LLM models and embedding clients are initialized as singletons (`rag.generation_model.llm_client`, `rag.multimodal_model.ocr_client`, etc.) to prevent memory leaks and reduce latency. An adapter pattern is used for embeddings, allowing easy swapping between OpenAI and Google embeddings via the configuration.
- **Langsmith integration:** I decided to integrate LangSmith to enable full prompt traceability, monitor token consumption in real time, and bring a higher level of technical maturity to the project.