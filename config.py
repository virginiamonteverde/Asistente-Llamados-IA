from pathlib import Path


# Carpeta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpeta donde colocamos los PDFs
DOCUMENTS_DIR = BASE_DIR / "documents"

# Carpeta donde Chroma guardará la base vectorial local
VECTOR_DB_DIR = BASE_DIR / "vector_db"

# Configuración de Ollama
OLLAMA_BASE_URL = "http://localhost:11434"

# Modelo para generar embeddings
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Modelo para generar respuestas
CHAT_MODEL = "hermes3:8b"

# Nombre de la colección dentro de Chroma
CHROMA_COLLECTION_NAME = "pdf_documents"