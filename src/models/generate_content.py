from typing import Optional
from google.genai.types import GroundingMetadata
from pydantic import BaseModel


class GenerateContentRequest(BaseModel):
    query: str
    file_search_store_name: str


class GenerateContentResponse(BaseModel):
    content: str
    grounding_metadata: Optional[GroundingMetadata] = None
