import os
import google.generativeai as genai

class ReportAgent:
    def __init__(self):
        # Load Google API key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # you can use gemini-pro too

    def respond(self, message: str) -> str:
        """
        Uses Google Gemini to analyze lab reports or medical test descriptions.
        """
        try:
            prompt = (
                "You are a helpful medical assistant. "
                "give a short consise summary in about 4 sentences not more than that"
                "Interpret the following lab report or health-related text in simple terms like first start with the basic info and then change the paragraphs to bullet points. "
                "Be clear and patient. "
                "Always add a note that the user should consult a real doctor for confirmation.\n\n"
                f"Report: {message}"
            )

            response = self.model.generate_content(prompt)

            return response.text if response and response.text else "⚠️ No response from Gemini."

        except Exception as e:
            return f"⚠️ ReportAgent internal error: {str(e)}"
