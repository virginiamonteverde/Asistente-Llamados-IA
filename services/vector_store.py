import chromadb

from config import VECTOR_DB_DIR, CHROMA_COLLECTION_NAME


class VectorStore:
    """
    Servicio encargado de guardar y consultar fragmentos en Chroma.

    Chroma es la base vectorial local.
    Guarda:
    - el texto del fragmento,
    - su embedding,
    - metadatos como archivo, página e índice de fragmento.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME
        )

    def add_chunks(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        """
        Guarda fragmentos y embeddings en la base vectorial.

        chunks y embeddings deben tener el mismo largo.
        """

        if len(chunks) != len(embeddings):
            raise ValueError("La cantidad de fragmentos y embeddings no coincide.")

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            chunk_id = (
                f"{chunk['file_name']}-"
                f"page-{chunk['page_number']}-"
                f"chunk-{chunk['chunk_index']}"
            )

            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append(
                {
                    "file_name": chunk["file_name"],
                    "page_number": chunk["page_number"],
                    "chunk_index": chunk["chunk_index"],
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(self, query_embedding: list[float], n_results: int = 5) -> dict:
        """
        Busca los fragmentos más parecidos a una pregunta.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

    def count(self) -> int:
        """
        Devuelve cuántos fragmentos hay guardados en la colección.
        """

        return self.collection.count()