from typing import Optional
from google.genai.types import GroundingMetadata
from pydantic import BaseModel


class GenerateContentResponse(BaseModel):
    content: str
    grounding_metadata: Optional[GroundingMetadata] = None
