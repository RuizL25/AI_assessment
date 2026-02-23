from fastapi import APIRouter, HTTPException
from api.schemas.conversation_schema import ChatRequest, ChatResponse
from agent.chat_agent import agent_executor

router = APIRouter(prefix="/api/v1", tags=["Conversation"])

@router.post("/conversation", response_model=ChatResponse)
def chat_endpoint(query: ChatRequest):
    try:
        result = agent_executor.invoke({"input": query.query, "chat_history": []})
        return ChatResponse(answer=result["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
