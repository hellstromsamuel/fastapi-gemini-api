from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers.test import test_router

load_dotenv()

app = FastAPI(title="FastAPI Gemini API")
app.include_router(test_router)


@app.get("/")
def get_root():
    return {"message": "FastAPI Gemini API - Checkout the swagger docs at /docs"}
