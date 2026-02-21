"""
System prompts for the RAG pipeline.

Contains the prompt templates used by the different
components of the pipeline, such as multimodal OCR extraction.
"""

PROMPT_IMAGES_TO_TEXT: str = """
Act as an expert OCR (Optical Character Recognition) engine.
Your task is to transcribe the content of this image into a structured Markdown document.

Directives:
1. **Structure & Hierarchy:** Accurately reflect the document layout. Use Markdown headers (#, ##) for titles and lists (*, -) for bullet points.
2. **Tables:** Represent any grid or tabular data using correct Markdown table syntax.
3. **Content Integrity:** Transcribe text exactly as written, including punctuation and spelling errors. Do not correct the source text.
4. **Styling:** Maintain text styling such as **bold** and *italics* where visible.
5. **Unreadable Content:** If parts of the text are completely illegible, mark them as [illegible].

Output Constraints:
- Return the raw Markdown string ONLY.
- Do NOT provide introductory text (e.g., "Here is the transcription").
- Do NOT wrap the output in code blocks (```markdown). Start directly with the text.
"""


PROMPT_CHUNK_DESCRIPTION: str = """
Act as an expert in semantic analysis and information retrieval (RAG).
Your task is to generate a concise, dense, and keyword-rich description of the provided text chunk.
This description will be used to generate vector embeddings to improve search retrieval.
This chunks are for a Voice assistant that will answer techinacl questions about the manual documents and products specifications.

Input Text:
"{chunk_text}"

Directives:
1. **Contextualize:** Summarize the core topic of the chunk. If the text is a fragment, infer the context based on the content.
2. **Entity Extraction:** Identify and include key entities (names, specific terminology, dates, metric names) that are critical for retrieval.
3. **Intent Matching:** Write the description in a way that aligns with potential user queries (e.g., "Details regarding X process" rather than just "A paragraph about X").
4. **Density:** Avoid fluff words. Focus on semantic density.

Output Constraints:
- Return the description text ONLY.
- Do NOT use Markdown formatting (no headers, no bolding). Plain text is best for embeddings.
- Do NOT provide introductory text (e.g., "This chunk is about..."). Start directly with the description.
"""