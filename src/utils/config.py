"""
Centralized configuration module for the RAG project.

Uses pydantic-settings to load environment variables and define
default values for pipeline parameters.
"""

from pydantic_settings import BaseSettings
from pydantic import SecretStr
from typing import Optional

class Settings(BaseSettings):
    """Global configuration for the RAG pipeline.

    Automatically loads environment variables from a `.env` file
    and defines default values for each parameter.

    Attributes:
        data_path: Path to the PDF file to process.
        embedding_model: Name of the embedding model.
        vector_store_path: Directory where the Chroma vector store is persisted.
        top_k: Number of documents to return in the similarity search.
        GOOGLE_API_KEY: Google API key for multimodal OCR with Gemini.
        OPENAI_API_KEY: OpenAI API key for answer generation with GPT.
    """

    data_path: str = "./data/input_ingest/series_76_tables.pdf"
    
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-large"
    
    vector_store_path: str = "./data/vector_store"
    output_dir: str = "./data/output_ingest"
    
    top_k: int = 10
    
    google_genai_model_name: str = "gemini-2.5-flash"
    openAI_generation_model_name : str = "gpt-4.1-mini"

    GOOGLE_API_KEY: Optional[SecretStr] = None
    OPENAI_API_KEY: Optional[SecretStr] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()