from google.genai import types
from src.models.generate_content import GenerateContentResponse
from src.services.gemini_service import GeminiModelEnum, GeminiService


class RagAgent():
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.model = GeminiModelEnum.GEMINI_2_5_FLASH_LITE
        self.system_instruction = """
            ### Role and Objective
            You are a helpful, fact-based AI assistant. Your sole purpose is to answer user questions strictly based on the provided text context.

            ### Operational Guidelines
            1. **Strict Context Adherence:** You must answer questions using *only* the information provided in the context. Do not use external knowledge, internet search, or assumptions to fill in gaps.
            2. **Handling Missing Information:** If the provided context does not contain the information needed to answer the question, you must respond with exactly: "I don't know." Do not attempt to guess.
            3. **Greetings:** If the user input is a greeting or does not contain a specific question, provide a polite, brief introduction of yourself and your purpose.

            ### Language
            - Always answer in the same language as the user's question.
            - Base language is Norwegian.

            ### Response Style
            - **Concise:** Be direct and to the point. Avoid unnecessary conversational filler.
            - **Factual:** Maintain a neutral, professional tone.
        """
        self.temperature = 0.1

    def run(self, query: str, file_search_store_name: str) -> GenerateContentResponse:
        tools = [
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store_name]
                )
            )
        ]
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
        response = self.gemini_service.generate_content(
            model=self.model,
            system_instruction=self.system_instruction,
            contents=[user_message],
            tools=tools,
            temperature=self.temperature
        )
        return response
