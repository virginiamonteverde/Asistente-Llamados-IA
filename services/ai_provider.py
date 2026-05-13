import requests

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