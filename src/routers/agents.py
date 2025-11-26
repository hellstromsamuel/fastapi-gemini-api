from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google.genai.errors import ClientError
from src.dependencies.agents import get_rag_agent
from src.dependencies.services import get_file_search_store_service
from src.agents.rag_agent import RagAgent
from src.models.generate_content import GenerateContentResponse
from src.services.file_search_store_service import FileSearchStoreService

agents_router = APIRouter(prefix="/agents", tags=["agents"])


class RunRagRequest(BaseModel):
    query: str
    file_search_store_name: str


@agents_router.post("/rag", response_model=GenerateContentResponse)
def run(
    body: RunRagRequest,
    rag_agent: RagAgent = Depends(get_rag_agent),
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service),
) -> GenerateContentResponse:
    try:
        file_search_store = file_search_store_service.get_file_search_store(
            body.file_search_store_name)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e

    try:
        return rag_agent.run(body.query, file_search_store.name)
    except ClientError as e:
        raise HTTPException(
            status_code=400, detail=f"Bad Request with file search store name '{body.file_search_store_name}': {e.message}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
