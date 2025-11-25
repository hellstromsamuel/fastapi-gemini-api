from fastapi import APIRouter

root_router = APIRouter(tags=["root"])


@root_router.get("/")
def get_root():
    return {"message": "FastAPI Gemini API - Checkout the swagger docs at /docs"}
