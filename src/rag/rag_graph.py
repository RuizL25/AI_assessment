"""
Main RAG pipeline graph.

Defines and compiles the LangGraph that orchestrates the
RAG pipeline stages: ingestion -> md conversion -> segmentation -> chunk descriptions -> Embeddings -> vector store.
"""

from rag.schemas.rag_schemas import RAGPipelineResult

from typing import Any, Dict, Sequence

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langgraph.graph import StateGraph, END
from langsmith import traceable

from rag.ingest_pipeline.ingest_pipeline import ingest
from rag.ingest_pipeline.segmentation_pipeline import markdown_structure_chunking
from rag.ingest_pipeline.chunk_description_pipeline import chunk_description_pipeline
from rag.ingest_pipeline.embeddings_pipeline import embed_documents_pipeline
from rag.ingest_pipeline.vector_store_pipeline import vector_store
from rag.config import settings
from rag.services import save_md_doc, save_raw_chunks, save_chunks_description, save_embeddings


class State(dict):
    """Shared state between RAG graph nodes.

    Attributes:
        ruta_pdf: Path to the PDF file to process.
        estrategia: Ingestion strategy ('native', 'local', 'google').
        documents: Documents extracted from the PDF.
        chunks: Chunks generated from the documents.
        retriever: Configured FAISS retriever.
    """

    ruta_pdf: str
    document_text : str
    chunks: Sequence[Document]
    chunks_descriptions: Sequence[str]
    embeddings: Sequence[list[float]]
    retriever: Any

@traceable(name="ingest_node")
def ingest_node(state: State) -> Dict[str, Any]:
    """Ingestion node: extracts text from PDF.

    Args:
        state: Current graph state with ruta_pdf and estrategia.

    Returns:
        Dictionary with extracted documents.
    """
    text = ingest(state["ruta_pdf"])
    save_md_doc(text, state["ruta_pdf"])
    return {"document_text": text}


@traceable(name="segmentation_node")
def segmentation_node(state: State) -> Dict[str, Any]:
    """Segmentation node: splits documents into chunks.

    Args:
        state: Current graph state with extracted documents.

    Returns:
        Dictionary with generated chunks.
    """
    chunks = markdown_structure_chunking(state["document_text"])
    save_raw_chunks(chunks, state["ruta_pdf"])
    return {"chunks": chunks}

@traceable(name="chunk_description_node")
def chunk_description_node(state: State) -> Dict[str, Any]:
    """Chunk description node: creates a description for each chunk.

    Args:
        state: Current graph state with generated chunks.

    Returns:
        Dictionary with chunk descriptions.
    """
    chunks_descriptions = chunk_description_pipeline(state["chunks"])
    save_chunks_description(chunks_descriptions, state["ruta_pdf"]) 
    return {"chunks_descriptions": chunks_descriptions}

@traceable(name="embeddings_node")
def embeddings_node(state: State) -> Dict[str, Any]:
    """Embeddings node: generates embeddings for each chunk.

    Args:
        state: Current graph state with generated chunks.

    Returns:
        Dictionary with generated embeddings.
    """
    embeddings = embed_documents_pipeline(state["chunks_descriptions"])
    save_embeddings_to_json(state["chunks_descriptions"], embeddings, state["ruta_pdf"])

    return {"embeddings": embeddings}


@traceable(name="vector_store_node")
def vector_store_node(state: State) -> Dict[str, Any]:
    """Vector store node: indexes chunks and creates retriever.

    Args:
        state: Current graph state with generated chunks.

    Returns:
        Dictionary with configured retriever.
    """
    retriever = vector_store_pipeline(state["chunks_descriptions"], state["embeddings"])
    return {"retriever": retriever}


workflow = StateGraph(State)
workflow.add_node("ingest", ingest_node)
workflow.add_node("segmentation", segmentation_node)
workflow.add_node("chunk_description", chunk_description_node)
workflow.add_node("embeddings", embeddings_node)
workflow.add_node("vector_store", vector_store_node)
workflow.add_edge("ingest", "segmentation")
workflow.add_edge("segmentation", "chunk_description")
workflow.add_edge("chunk_description", "embeddings")
workflow.add_edge("embeddings", "vector_store")
workflow.add_edge("vector_store", END)
workflow.set_entry_point("ingest")

rag_app = workflow.compile()


result = rag_app.invoke(
    {
        "ruta_pdf": settings.data_path,
        "estrategia": "google",
    }
)

pipeline_result = RAGPipelineResult(
    total_length=len(result["document_text"]),
    total_chunks=len(result["chunks"]),
    total_descriptions=len(result["chunks_descriptions"]),
    total_embeddings=len(result["embeddings"]),
    retriever_ready=result.get("retriever") is not None,
)

print(pipeline_result)
