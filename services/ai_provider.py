import os
import requests

from google import genai

from config import OLLAMA_BASE_URL, EMBEDDING_MODEL, CHAT_MODEL


class OllamaProvider:
    """
    Implementación concreta para hablar con Ollama.

    La idea es que el resto del proyecto use esta clase como proveedor de IA,
    sin llamar directamente a Ollama desde Flask.
    """

    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.embedding_model = EMBEDDING_MODEL
        self.chat_model = CHAT_MODEL

    def get_embedding(self, text: str) -> list[float]:
        """
        Convierte un texto en un vector numérico usando el modelo de embeddings de Ollama.
        """

        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.embedding_model,
                "prompt": text,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["embedding"]

    def generate_answer(self, prompt: str) -> str:
        """
        Genera una respuesta usando el modelo de chat de Ollama.
        """

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.chat_model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]


class GeminiProvider:
    """
    Implementación concreta para generar respuestas con Gemini.

    La API key se toma desde la variable de entorno GEMINI_API_KEY.
    No debe escribirse la clave dentro del código.
    """

    def __init__(self):
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError(
                "No se encontró la variable de entorno GEMINI_API_KEY."
            )

        self.client = genai.Client()
        self.chat_model = "gemini-2.5-flash"

    def generate_answer(self, prompt: str) -> str:
        """
        Genera una respuesta usando Gemini.
        """

        response = self.client.models.generate_content(
            model=self.chat_model,
            contents=prompt,
        )

        return response.text