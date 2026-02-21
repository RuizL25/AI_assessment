from langchain_openai import ChatOpenAI
from utils.config import settings

llm_client = ChatOpenAI(
    model=settings.openAI_generation_model_name,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)
