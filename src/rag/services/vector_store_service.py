"""
ChromaDB vector store service.

Manages the creation, persistence, and retrieval of documents
using Chroma as the vector store.
"""
import os
from typing import List, Optional, Sequence
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_chroma import Chroma

from rag.embedding_model import embedding_client
from utils.config import settings

def create_vector_store(
    texts: Sequence[str], 
    embeddings: Sequence[List[float]],
    vector_store_path: str | None = None,
    top_k: int | None = None,
) -> VectorStoreRetriever:
    """Creates a Chroma index, saves it to disk, and returns a retriever."""
    
    if not texts or not embeddings:
        raise ValueError("The list of embeddings or texts is empty.")

    store_path = vector_store_path or settings.vector_store_path
    top_k = top_k or settings.top_k

    try:
        vector_store = Chroma.from_texts(
            texts=list(texts),
            embedding=embedding_client.client,
            persist_directory=store_path
        )
    except Exception as e:
        raise RuntimeError(f"Error creating/saving Chroma vector store: {e}") from e

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )

def load_vector_store_retriever(
    vector_store_path: str | None = None,
    top_k: int | None = None,
) -> VectorStoreRetriever:
    """Loads an existing Chroma index from disk and returns a retriever."""
    
    store_path = vector_store_path or settings.vector_store_path
    top_k = top_k or settings.top_k

    if not os.path.exists(store_path):
        raise FileNotFoundError(f"Chroma index not found at: {store_path}. Please run the ingestion script first.")

    try:
        vector_store = Chroma(
            persist_directory=store_path,
            embedding_function=embedding_client.client
        )
    except Exception as e:
        raise RuntimeError(f"Error loading Chroma from disk: {e}") from e

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )
