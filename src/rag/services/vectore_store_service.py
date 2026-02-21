"""
FAISS vector store service.

Manages the creation, persistence, and retrieval of documents
using FAISS as the vector store and Cohere for embeddings.
"""
import os
from typing import List, Optional, Sequence
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.vectorstores import FAISS
from utils.config import settings

def _get_embeddings():
    return CohereEmbeddings(
        model=settings.embedding_model,
        cohere_api_key=settings.COHERE_API_KEY,
    )

def create_vector_store(
    texts: Sequence[str], 
    embeddings: List[List[float]],
    vector_store_path: str | None = None,
    top_k: int | None = None,
) -> VectorStoreRetriever:
    """Creates an index, saves it to disk, and returns a retriever."""
    
    if not embeddings:
        raise ValueError("The list of embeddings is empty.")

    store_path = vector_store_path or settings.vector_store_path
    embedding_model = _get_embeddings()


    if not embeddings or not texts:
        raise ValueError("The list of embeddings or texts is empty.")

    text_embeddings_pairs = list(zip(texts,embeddings))

    try:
        vector_store = FAISS.from_embeddings(text_embeddings_pairs, embedding_model)
        vector_store.save_local(store_path)
    except Exception as e:
        raise RuntimeError(f"Error creating/saving FAISS: {e}") from e

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )

def load_vector_store_retriever(
    vector_store_path: str | None = None,
    top_k: int | None = None,
) -> VectorStoreRetriever:
    """Loads an existing index from disk and returns a retriever."""
    
    store_path = vector_store_path or settings.vector_store_path
    top_k = top_k or settings.top_k
    embedding_model = _get_embeddings()

    if not os.path.exists(store_path):
        raise FileNotFoundError(f"FAISS index not found at: {store_path}. Please run the ingestion script first.")

    try:
        vector_store = FAISS.load_local(
            store_path, 
            embedding_model, 
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        raise RuntimeError(f"Error loading FAISS from disk: {e}") from e

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )