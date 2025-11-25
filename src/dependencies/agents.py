from fastapi import Depends
from src.agents.rag_agent import RagAgent
from src.services.gen_ai_service import GenAiService
from src.dependencies.services import get_gen_ai_service


def get_rag_agent(gen_ai_service: GenAiService = Depends(get_gen_ai_service)) -> RagAgent:
    return RagAgent(gen_ai_service)
