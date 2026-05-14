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

    def list_documents(self) -> list[str]:
        """
        Devuelve la lista de documentos PDF disponibles en la base vectorial.

        La lista se arma a partir del metadato file_name guardado en Chroma.
        """

        results = self.collection.get(
            include=["metadatas"]
        )

        document_names = set()

        for metadata in results["metadatas"]:
            file_name = metadata.get("file_name")

            if file_name:
                document_names.add(file_name)

        return sorted(document_names)

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        file_name: str | None = None,
    ) -> dict:
        """
        Busca los fragmentos más parecidos a una pregunta.

        Si se recibe file_name, limita la búsqueda a ese documento.
        """

        where_filter = None

        if file_name:
            where_filter = {
                "file_name": file_name
            }

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter,
        )

    def count(self) -> int:
        """
        Devuelve cuántos fragmentos hay guardados en la colección.
        """

        return self.collection.count()