import os
from src.services.gen_ai_service import GenAiService
from src.services.file_search_store_service import FileSearchStoreService


def get_gen_ai_service() -> GenAiService:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return GenAiService(gemini_api_key)


def get_file_search_store_service() -> FileSearchStoreService:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return FileSearchStoreService(gemini_api_key)
