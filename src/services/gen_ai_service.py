from google import genai
from google.genai import types

from src.models.generate_content import GenerateContentResponse


class GenAiService():
    def __init__(self, gemini_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.description = "Answer questions based on information from tools provided."
        self.system_instruction = """
            Never make up your own information or assumptions.
            Always answer consise and to the point.
            If you don't have the required information, you must respond 'I don't know'.
            """

    def generate_content(self, query: str, file_search_store_name: str) -> GenerateContentResponse:
        tools = [
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store_name]
                )
            )
        ]

        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=tools
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=query,
            config=config
        )

        content = response.text
        grounding_metadata = None
        if response.candidates and len(response.candidates) > 0:
            grounding_metadata = response.candidates[0].grounding_metadata

        return GenerateContentResponse(content=content, grounding_metadata=grounding_metadata)
