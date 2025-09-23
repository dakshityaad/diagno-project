import os
import google.generativeai as genai

class KnowledgeAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def respond(self, message: str) -> str:
        try:
            prompt = (
                "answer in para graph no bold texts"
                "try to answer in points"
                "You are a medical genius your know everything about medical science and issues. "
                "Give a possible explanation of what condition it could be, "
                "tell facts, suggest simple remedies.\n\n"
                f"Symptoms: {message}"
            )

            response = self.model.generate_content(prompt)
            return response.text if response and response.text else "⚠️ No response from Gemini."

        except Exception as e:
            return f"⚠️ KnowlegdAgent internal error: {str(e)}"
