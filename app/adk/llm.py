from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

gemini_llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, api_key=settings.GEMINI_API_KEY)