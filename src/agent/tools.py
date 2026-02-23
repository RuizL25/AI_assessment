from langchain_core.tools import tool
from rag.retrieval_pipeline.retrieval_pipeline import Retrieval

retrieval = Retrieval()

@tool
def query_knowledge_base(query: str) -> str:
    """Queries the knowledge base for information from uploaded manuals 
    to answer user questions."""
    return retrieval.retrieve_context(query)
