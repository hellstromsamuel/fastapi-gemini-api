from enum import Enum
from google import genai
from google.genai.types import Content, GenerateContentConfig, Tool
from src.models.generate_content import GenerateContentResponse


class GeminiModelEnum(str, Enum):
    GEMINI_3_0_PRO_PREVIEW = "gemini-3.0-pro-preview"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"


class GeminiService():
    def __init__(self, gemini_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)

    def generate_content(
        self,
        model: GeminiModelEnum,
        system_instruction: str,
        contents: list[Content],
        tools: list[Tool],
        temperature: float = 1.0
    ) -> GenerateContentResponse:
        config = GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
            temperature=temperature
        )

        response = self.client.models.generate_content(
            model=model.value,
            contents=contents,
            config=config
        )

        content = response.text
        grounding_metadata = None
        if response.candidates and len(response.candidates) > 0:
            grounding_metadata = response.candidates[0].grounding_metadata

        return GenerateContentResponse(content=content, grounding_metadata=grounding_metadata)
