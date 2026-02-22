import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from rag.rag import RAGIngestionPipeline

def main():
    parser = argparse.ArgumentParser(description="Run the document ingestion pipeline.")
    parser.add_argument(
        "--pdf", 
        type=str, 
        required=True, 
        help="Path to the PDF file to ingest."
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file '{args.pdf}' not found.")
        sys.exit(1)

    file_name = os.path.basename(args.pdf)
    
    print("Initializing RAG Pipeline...")
    pipeline = RAGIngestionPipeline()
    
    try:
        result = pipeline.run_ingestion_pipeline(args.pdf, file_name)
        print("\n--- Ingestion Results ---")
        print(f"Characters extracted: {result.total_length}")
        print(f"Chunks generated: {result.total_chunks}")
        print(f"Descriptions generated: {result.total_descriptions}")
        print(f"Embeddings generated: {result.total_embeddings}")
        print(f"Vector Store (Chroma) ready: {result.retriever_ready}")
        print("-------------------------")
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        sys.exit(1)

main()