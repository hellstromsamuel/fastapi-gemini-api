import os
import time
import shutil
from pathlib import Path
from fastapi import UploadFile
from google import genai
from google.genai.types import Document, FileSearchStore


class FileSearchStoreService:
    def __init__(self, gemini_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)

    def list_file_search_stores(self) -> list[FileSearchStore]:
        return self.client.file_search_stores.list()

    def create_file_search_store(self, name: str) -> FileSearchStore:
        return self.client.file_search_stores.create(
            config={'display_name': name})

    def get_file_search_store(self, name: str) -> FileSearchStore:
        return self.client.file_search_stores.get(name=name)

    def delete_file_search_store(self, name: str) -> None:
        self.client.file_search_stores.delete(
            name=name, config={'force': True})

    def import_file(
        self,
        file_upload: UploadFile,
        file_display_name: str,
        file_search_store_name: str,
    ) -> None:
        # Create temp directory if it doesn't exist
        upload_dir = Path("temp_uploads")
        upload_dir.mkdir(exist_ok=True)

        # Upload file to temp directory
        file_path = upload_dir / file_upload.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_upload.file, buffer)

        # Upload and import a file into the File Search store, supply a file name which will be visible in citations
        operation = self.client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=file_search_store_name,
            config={
                "display_name": file_display_name
            }
        )

        # Wait until import is complete
        while not operation.done:
            time.sleep(5)
            operation = self.client.operations.get(operation)

        # Delete temp file
        os.remove(file_path)

    def list_documents(self, file_search_store_name: str) -> list[Document]:
        documents = self.client.file_search_stores.documents.list(
            parent=file_search_store_name
        )
        return documents

    def document_exists(self, file_type: str, display_name: str, file_search_store_name: str) -> bool:
        documents = self.list_documents(file_search_store_name)
        if not documents or len(documents) == 0:
            return False
        for document in documents:
            if document.mime_type == file_type and document.display_name == display_name:
                return True
        return False

    def delete_document(self, name: str) -> None:
        self.client.file_search_stores.documents.delete(
            name=name,
            config={'force': True}
        )
