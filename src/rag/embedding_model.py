from abc import ABC, abstractmethod
from typing import List, Any
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.config import settings

class BaseEmbeddingAdapter(ABC):
    client: Any
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        pass

class OpenAIEmbeddingAdapter(BaseEmbeddingAdapter):
    def __init__(self):
        self.client = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.OPENAI_API_KEY
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed_query(text)

class GeminiEmbeddingAdapter(BaseEmbeddingAdapter):
    def __init__(self):
        self.client = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.GOOGLE_API_KEY
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed_query(text)

def get_embedding_adapter(provider: str) -> BaseEmbeddingAdapter:
    if provider.lower() == "openai":
        return OpenAIEmbeddingAdapter()
    elif provider.lower() == "gemini":
        return GeminiEmbeddingAdapter()
    else:
        raise ValueError(f"Embeddings provider not supported: {provider}")

embedding_client = get_embedding_adapter(getattr(settings, "embedding_provider", "openai"))
