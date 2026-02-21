from fastapi import APIRouter, HTTPException
from rag.services.vector_store_service import load_vector_store_retriever
from api.schemas.conversation_schema import SearchRequest, SearchResponse, SourceInfo

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest):
    
    request = payload

    retriever = load_vector_store_retriever()

    try:
        retrieved_docs = retriever.invoke(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sources = []    

    for doc in retrieved_docs:
        sources.append(
            SourceInfo(
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page", 0),
                content=doc.page_content,
            )
        )

    return SearchResponse(query=request.query, answer="", sources=sources)