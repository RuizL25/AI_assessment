"""
Pydantic schemas for the RAG pipeline.

Defines the input and output data models used
by the graph nodes and pipeline functions.
"""

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    """Input schema for the ingestion pipeline.

    Attributes:
        ruta_pdf: Absolute or relative path to the PDF file to process.
        estrategia: Ingestion method to use ('native', 'local', 'google').
    """

    ruta_pdf: str = Field(..., description="Ruta al archivo PDF a procesar")


class DocumentChunk(BaseModel):
    """Representation of a processed document chunk.

    Attributes:
        page_content: Textual content of the chunk.
        source: Path to the source file.
        page: Page number of origin.
        chunk_type: Type of ingestion used.
    """

    page_content: str = Field(..., description="Textual content of the chunk")
    source: str = Field(..., description="Path to the source file")
    page: int = Field(..., description="Page number of origin")
    chunk_type: str = Field(..., description="Type of ingestion used")


class RAGPipelineResult(BaseModel):
    """Complete result of the RAG pipeline.

    Attributes:
        total_documents: Number of documents extracted.
        total_chunks: Number of chunks generated.
        retriever_ready: Indicates if the retriever was created successfully.
    """

    total_length: int = Field(..., description="Number of documents extracted")
    total_chunks: int = Field(..., description="Number of chunks generated")
    total_descriptions: int = Field(..., description="Number of descriptions generated")
    total_embeddings: int = Field(..., description="Number of embeddings generated")
    retriever_ready: bool = Field(
        ..., description="Indicates if the retriever was created"
    )
