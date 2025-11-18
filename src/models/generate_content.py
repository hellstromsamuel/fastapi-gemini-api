from pydantic import BaseModel


class GenerateContentRequest(BaseModel):
    query: str


class GenerateContentResponse(BaseModel):
    content: str
