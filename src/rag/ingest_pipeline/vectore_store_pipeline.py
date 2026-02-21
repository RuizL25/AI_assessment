"""
FAISS vector store service.

Manages the creation, persistence, and retrieval of documents
using FAISS as the vector store and Cohere for embeddings.
"""

from typing import List, Sequence

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.vectorstores import FAISS
from rag.services.vector_store_service import create_vector_store
from utils.config import settings


def vector_store(
    texts: Sequence[str], 
    embeddings: Sequence[List[float]],
    vector_store_path: str | None = None,
    top_k: int | None = None,
) -> VectorStoreRetriever:
    """Creates a FAISS vector store from chunks and returns a retriever.

    Generates embeddings for the chunks using Cohere, builds a FAISS index,
    persists it to disk, and configures a similarity retriever.

    Args:
        texts: List of texts to index.
        embeddings: List of embeddings to index.
        vector_store_path: Directory where to persist the index.
                           Defaults to settings.vector_store_path.
        top_k: Number of documents to return per search.
               Defaults to settings.top_k.

    Returns:
        Retriever configured for similarity search.

    Raises:
        ValueError: If the list of embeddings is empty.
        RuntimeError: If the vector store or embeddings creation fails.
    """
    if not embeddings or not texts:
        raise ValueError("The list of embeddings or texts is empty.")

    store_path = vector_store_path or settings.vector_store_path
    top_k = top_k or settings.top_k

    retriever = create_vector_store(texts, embeddings, store_path, top_k)

    return retriever