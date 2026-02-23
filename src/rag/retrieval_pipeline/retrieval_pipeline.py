from rag.services.vector_store_service import load_vector_store_retriever
from langsmith import traceable

class Retrieval:
    @traceable(name="retrieve_context")
    def retrieve_context(self, query: str) -> str:
        retriever = load_vector_store_retriever()
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
