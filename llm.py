import json
from groq import Groq

from config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"


class LLM:

    @staticmethod
    def generate(prompt: str, temperature: float = 0.3) -> str:
        """
        Generate a text response from the LLM.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous AI agent. "
                        "Always produce professional, structured, and concise responses."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()

    @staticmethod
    def generate_json(prompt: str):
        """
        Generate a JSON response from the LLM.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return ONLY valid JSON. "
                        "Do not include markdown or explanations."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return json.loads(response.choices[0].message.content)