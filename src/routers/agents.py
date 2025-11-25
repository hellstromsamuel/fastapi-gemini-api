from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google.genai.errors import ClientError

from agents.rag_agent import RagAgent
from dependencies.agents import get_rag_agent
from models.generate_content import GenerateContentResponse

agents_router = APIRouter(prefix="/agents", tags=["agents"])


class RunRagRequest(BaseModel):
    query: str
    file_search_store_name: str


@agents_router.post("/rag", response_model=GenerateContentResponse)
def run(
    body: RunRagRequest,
    rag_agent: RagAgent = Depends(get_rag_agent),
) -> GenerateContentResponse:
    try:
        return rag_agent.run(body.query, body.file_search_store_name)
    except ClientError as e:
        raise HTTPException(
            status_code=400, detail=f"Bad Request with file search store name '{body.file_search_store_name}': {e.message}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
