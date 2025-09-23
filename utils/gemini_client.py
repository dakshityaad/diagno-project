import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    """
    A client to interact with the Google Gemini Pro API.
    """
    def __init__(self):
        """
        Initializes the Gemini client by configuring the API key.
        """
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the Gemini model based on a given prompt.

        Args:
            prompt: The input text prompt for the model.

        Returns:
            The generated text response from the model.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response from Gemini: {e}")
            return "Sorry, I encountered an error while processing your request. Please try again."

# You can create a single instance to be used across the application
gemini_client = GeminiClient()
