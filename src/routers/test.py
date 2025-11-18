from fastapi import APIRouter, Depends
from src.dependencies.services import get_gen_ai_service
from src.models.generate_content import GenerateContentRequest, GenerateContentResponse
from src.services.gen_ai_service import GenAiService

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.get("/")
def get_test():
    return {"message": "Test"}


@test_router.post("/generate_content", response_model=GenerateContentResponse)
def generate_content(
    body: GenerateContentRequest,
    gen_ai_service: GenAiService = Depends(get_gen_ai_service)
) -> GenerateContentResponse:
    return GenerateContentResponse(content=gen_ai_service.generate_content(body.query))
