import os
from google import genai


class GenAiService():
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        self.client = genai.Client(api_key=api_key)

    def generate_content(self, query: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=query,
        )
        return response.text
