import os

from dotenv import load_dotenv
from groq import Groq

from .base_provider import AIProvider

load_dotenv()


class GroqProvider(AIProvider):

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.1-8b-instant"

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content

    def generate_json(self, prompt: str):

        return self.generate(prompt)