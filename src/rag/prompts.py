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
Act as an expert in semantic analysis and information retrieval (RAG) optimization for technical documentation.
Your task is to generate a concise, dense, keyword-rich description of the provided text chunk, optimized for vector search embeddings.
This chunk is part of a knowledge base for an AI assistant answering technical questions about product specifications, manuals, operating metrics, and performance data.

Input Text:
"{chunk_text}"

Directives:
1. Contextualize & Identify Format: Summarize the core technical topic. Explicitly state if the chunk represents a table, matrix, specification list, or standard prose.
2. Tabular Data Mapping: If the chunk contains tabular or matrix data, identify the relationship being mapped. Explicitly list the primary keys (e.g., Part Numbers, Model Series) and the specific parameters/column headers provided (e.g., Input Voltage, Torque, Duty Cycle, Full Load Current, dimensions, units).
3. Entity & Metric Extraction: Extract critical entities like product families, exact technical terminology, metric names, and units of measurement (e.g., Amps, Nm, Watts, Hz, Sec) that users might query.
4. Intent Matching: Phrase the description to match potential engineering or technical queries (e.g., "Electrical specifications mapping base part numbers to operating speed and locked rotor current for 110V single-phase power").
5. Semantic Density: Maximize high-value keywords. Strip out filler words (e.g., "This chunk shows"). Do not describe the actual specific values of every cell; instead, describe *what categories of data* are available in the chunk.

Output Constraints:
- Return ONLY the description text.
- NO Markdown formatting (no headers, asterisks, bullet points, or bolding). Plain text only.
- NO introductory phrases. Start immediately with the descriptive content.
"""