import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.routers._root import root_router
from src.routers.agents import agents_router
from src.routers.file_search_store import file_search_store_router

load_dotenv()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    if token != os.getenv("API_SECRET"):
        raise HTTPException(status_code=401, detail="Unauthorized")


app = FastAPI(title="FastAPI Gemini API")
app.include_router(
    file_search_store_router,
    dependencies=[Depends(verify_token)])
app.include_router(
    root_router,
    dependencies=[Depends(verify_token)])
app.include_router(
    agents_router,
    dependencies=[Depends(verify_token)])
