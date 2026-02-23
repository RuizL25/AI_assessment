from fastapi import FastAPI
from api.routers import conversation_router

app = FastAPI(title="Support Agent API")
app.include_router(conversation_router.router)
