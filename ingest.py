from config import DOCUMENTS_DIR
from services.ai_provider import OllamaProvider
from services.pdf_reader import read_pdfs_from_folder
from services.text_splitter import split_pages_into_chunks
from services.vector_store import VectorStore


def ingest_documents():
    """
    Proceso de ingesta:
    1. Lee PDFs desde documents/
    2. Divide el texto en fragmentos
    3. Genera embeddings con Ollama
    4. Guarda fragmentos + embeddings en Chroma
    """

    print("Leyendo PDFs...")
    pages = read_pdfs_from_folder(str(DOCUMENTS_DIR))
    print(f"Páginas leídas: {len(pages)}")

    print("Dividiendo texto en fragmentos...")
    chunks = split_pages_into_chunks(pages)
    print(f"Fragmentos generados: {len(chunks)}")

    provider = OllamaProvider()
    embeddings = []

    print("Generando embeddings con Ollama...")

    for index, chunk in enumerate(chunks, start=1):
        print(f"Embedding {index}/{len(chunks)}")
        embedding = provider.get_embedding(chunk["text"])
        embeddings.append(embedding)

    print("Guardando fragmentos en Chroma...")
    vector_store = VectorStore()
    vector_store.add_chunks(chunks, embeddings)

    print("Ingesta finalizada.")
    print(f"Fragmentos guardados en base: {vector_store.count()}")


if __name__ == "__main__":
    ingest_documents()