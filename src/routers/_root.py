from fastapi import APIRouter, Depends, HTTPException
from google.genai.errors import ClientError
from src.dependencies.services import get_file_search_store_service, get_gen_ai_service
from src.models.generate_content import GenerateContentRequest, GenerateContentResponse
from src.services.file_search_store_service import FileSearchStoreService
from src.services.gen_ai_service import GenAiService

root_router = APIRouter(tags=["root"])


@root_router.get("/")
def get_root():
    return {"message": "FastAPI Gemini API - Checkout the swagger docs at /docs"}


@root_router.post("/generate_content", response_model=GenerateContentResponse)
def generate_content(
    body: GenerateContentRequest,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service),
    gen_ai_service: GenAiService = Depends(get_gen_ai_service),
) -> GenerateContentResponse:
    if not body.query:
        raise HTTPException(status_code=400, detail="Query is required")
    if not body.file_search_store_name:
        print("No file search store name provided")
        return gen_ai_service.generate_content(body.query)

    try:
        file_search_store = file_search_store_service.get_file_search_store(
            body.file_search_store_name)
        return gen_ai_service.generate_content(body.query, file_search_store.name)
    except ClientError as e:
        print(e)
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
