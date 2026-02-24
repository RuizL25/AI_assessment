"""
Embeddings module wrapper for the pipeline.

Provides a high-level function to generate embeddings
of documents using the embedding factory singleton.
"""

from typing import List
from rag.embedding_model import embedding_client
from langsmith import traceable

@traceable(name="embed_documents")
def embed_documents(documents: List[str]) -> List[List[float]]:
    """Generates embeddings for a list of documents.

    Args:
        documents: List of strings to vectorize.

    Returns:
        List of embedding vectors (one per document).

    Raises:
        ValueError: If the list of documents is empty.
        RuntimeError: If the embedding generation fails.
    """
    if not documents:
        raise ValueError("The list of documents is empty.")

    try:
        embeddings = embedding_client.embed_documents(documents)
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}") from e
