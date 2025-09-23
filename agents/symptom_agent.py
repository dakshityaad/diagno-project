import os
import google.generativeai as genai

class SymptomAgent:
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
                "You are a medical assistant. "
                "The user is describing their symptoms. "
                "Give a possible explanation of what condition it could be, "
                "suggest simple remedies, and advise consulting a doctor if serious.\n\n"
                f"Symptoms: {message}"
            )

            response = self.model.generate_content(prompt)
            return response.text if response and response.text else "⚠️ No response from Gemini."

        except Exception as e:
            return f"⚠️ SymptomAgent internal error: {str(e)}"
