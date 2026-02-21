from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import settings

ocr_client = ChatGoogleGenerativeAI(
    model=settings.google_genai_model_name,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    max_retries=2
)
