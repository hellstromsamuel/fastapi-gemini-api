from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from google.genai.errors import ClientError
from google.genai.types import Document, FileSearchStore
from src.dependencies.services import get_file_search_store_service
from src.services.file_search_store_service import FileSearchStoreService

file_search_store_router = APIRouter(
    prefix="/file_search_store", tags=["file_search_store"])


@file_search_store_router.get("/", response_model=list[FileSearchStore])
def list_file_search_stores(
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> list[FileSearchStore]:
    try:
        return file_search_store_service.list_file_search_stores()
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.post("/", response_model=FileSearchStore)
def create_file_search_store(
    file_search_store_name: str,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> FileSearchStore:
    if not file_search_store_name:
        raise HTTPException(
            status_code=400, detail="'file_search_store_name' is required")

    try:
        file_search_store = file_search_store_service.create_file_search_store(
            file_search_store_name)
        return file_search_store
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.get("/", response_model=FileSearchStore)
def get_file_search_store(
    file_search_store_name: str,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> FileSearchStore:
    if not file_search_store_name:
        raise HTTPException(
            status_code=400, detail="'file_search_store_name' is required")

    try:
        file_search_store = file_search_store_service.get_file_search_store(
            file_search_store_name)
        return file_search_store
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.delete("/", response_model=str)
def delete_file_search_store(
    file_search_store_name: str,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> str:
    try:
        file_search_store_service.delete_file_search_store(
            file_search_store_name)
        return f"File search store {file_search_store_name} deleted successfully"
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.post("/documents", response_model=str)
def import_file(
    file_upload: UploadFile = None,
    file_display_name: str = Form(...),
    file_search_store_name: str = Form(...),
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> str:
    if not file_upload:
        raise HTTPException(
            status_code=400, detail="'file_upload' is required")
    if not file_display_name:
        raise HTTPException(
            status_code=400, detail="'file_display_name' is required")
    if not file_search_store_name:
        raise HTTPException(
            status_code=400, detail="'file_search_store_name' is required")

    file_search_store = None
    try:
        file_search_store = file_search_store_service.get_file_search_store(
            file_search_store_name)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e

    document_exists = file_search_store_service.document_exists(
        file_upload.content_type,
        file_display_name,
        file_search_store.name)
    if document_exists:
        raise HTTPException(
            status_code=400, detail=f"Document with type '{file_upload.content_type}' and display name '{file_display_name}' already exists in file search store '{file_search_store_name}'")

    try:
        file_search_store_service.import_file(
            file_upload=file_upload,
            file_display_name=file_display_name,
            file_search_store_name=file_search_store.name)
        return f"File {file_display_name} imported successfully"
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.get("/documents", response_model=list[Document])
def list_documents(
    file_search_store_name: str,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> list[Document]:
    try:
        return file_search_store_service.list_documents(file_search_store_name)
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e


@file_search_store_router.delete("/documents", response_model=str)
def delete_document(
    document_name: str,
    file_search_store_service: FileSearchStoreService = Depends(
        get_file_search_store_service)
) -> str:
    try:
        file_search_store_service.delete_document(document_name)
        return f"Document {document_name} deleted successfully"
    except ClientError as e:
        raise HTTPException(status_code=400, detail=e.message) from e
