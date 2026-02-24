"""
Main RAG Ingestion Pipeline.

Orchestrates the ingestion pipeline sequentially: 
PDF Reading (OCR) -> Segmentation -> Embeddings -> Vector Store.
"""

import os
from typing import List
from langchain_core.documents import Document
from rag.schemas.rag_schema import RAGPipelineResult
from utils.config import settings


from rag.ingest_pipeline.ingest_pipeline import GoogleVisionIngestor
from rag.ingest_pipeline.segmentation_pipeline import mixed_structure_chunking
from rag.ingest_pipeline.embeddings_pipeline import embed_documents_pipeline
from rag.ingest_pipeline.vector_store_pipeline import vector_store


from rag.services.save_md_doc import save_md_doc
from rag.services.save_raw_chunks import save_chunks
from rag.services.save_embeddings import save_embeddings_to_json

class RAGIngestionPipeline:
    """Facade to orchestrate the RAG pipeline steps."""

    def __init__(self):
        self.ingestor = GoogleVisionIngestor()

    def run_ingestion_pipeline(self, pdf_path: str, file_name: str) -> RAGPipelineResult:
        """Runs the entire ingestion pipeline sequentially.

        Args:
            pdf_path: Absolute or relative path to the PDF to process.
            file_name: Name used to save the intermediate files.

        Returns:
            RAGPipelineResult containing statistics about the pipeline run.
        """
        print(f"Starting ingestion pipeline for: {pdf_path}")


        document_text = self.ingestor.ingest(pdf_path)
        save_md_doc(document_text, file_name)
        

        chunks: List[Document] = list(mixed_structure_chunking(document_text))
        save_chunks(chunks, file_name)
        chunks_text = [chunk.page_content for chunk in chunks]

        embeddings = embed_documents_pipeline(chunks_text)
        save_embeddings_to_json(chunks_text, embeddings, file_name)

        retriever = vector_store(chunks_text, embeddings)

        return RAGPipelineResult(
            total_length=len(document_text),
            total_chunks=len(chunks),
            total_embeddings=len(embeddings),
            retriever_ready=retriever is not None,
        )
