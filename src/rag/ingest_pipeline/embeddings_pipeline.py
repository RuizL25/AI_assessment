"""
Embeddings module wrapper for the pipeline.

Provides a high-level function to generate embeddings
of documents using the Cohere service.
"""

from typing import List

from langchain_core.documents import Document

from rag.services.embeddings_service import embed_documents


def embed_documents_pipeline(chunks_descriptions: List[str]) -> List[List[float]]:
    """Calls the embeddings service to generate embeddings for a list of documents.

    Args:
        chunks_descriptions : List of the chunks descriptions to vectorize.

    Returns:
        List of embedding vectors (one per document).

    Raises:
        ValueError: If the list of documents is empty.
        RuntimeError: If the embedding generation fails.
    """
    if not chunks_descriptions:
        raise ValueError("The list of documents is empty.")

    try:
        embeddings = embed_documents(chunks_descriptions)

        return embeddings
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}")