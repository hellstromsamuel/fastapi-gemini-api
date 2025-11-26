from fastapi import Depends
from src.agents.rag_agent import RagAgent
from src.services.gemini_service import GeminiService
from src.dependencies.services import get_gemini_service


def get_rag_agent(gemini_service: GeminiService = Depends(get_gemini_service)) -> RagAgent:
    return RagAgent(gemini_service)
