from services.ai_provider import GeminiProvider, OllamaProvider
from services.vector_store import VectorStore


class RagService:
    """
    Servicio principal del RAG.

    Coordina:
    1. convertir la pregunta en embedding,
    2. buscar fragmentos relevantes en Chroma,
    3. reordenar los fragmentos según coincidencia con la pregunta,
    4. armar un prompt con contexto,
    5. pedirle una respuesta al modelo de chat,
    6. devolver respuesta y fuentes.
    """

    def __init__(self):
        self.embedding_provider = OllamaProvider()
        self.chat_provider = GeminiProvider()
        self.vector_store = VectorStore()

    def list_documents(self) -> list[str]:
        """
        Devuelve la lista de documentos disponibles para consultar.
        """

        return self.vector_store.list_documents()

    def _score_result(self, question: str, document: str, metadata: dict) -> int:
        """
        Calcula un puntaje simple para priorizar resultados cuyo archivo o texto
        coincidan mejor con palabras importantes de la pregunta.

        Esto ayuda cuando Chroma encuentra varios documentos parecidos.
        """

        question_normalized = question.lower()
        document_normalized = document.lower()
        file_name_normalized = metadata["file_name"].lower().replace("_", " ")

        score = 0

        important_words = [
            word
            for word in question_normalized.replace("?", "").split()
            if len(word) > 3
        ]

        for word in important_words:
            if word in file_name_normalized:
                score += 3

            if word in document_normalized:
                score += 1

        return score

    def ask(
        self,
        question: str,
        n_results: int = 5,
        file_name: str | None = None,
    ) -> dict:
        """
        Recibe una pregunta del usuario y devuelve una respuesta basada en los PDFs.

        Si se recibe file_name, busca únicamente dentro de ese documento.
        """

        question_embedding = self.embedding_provider.get_embedding(question)

        search_results = self.vector_store.search(
            query_embedding=question_embedding,
            n_results=n_results,
            file_name=file_name,
        )

        documents = search_results["documents"][0]
        metadatas = search_results["metadatas"][0]

        if not documents:
            return {
                "question": question,
                "selected_document": file_name,
                "answer": "No encontré fragmentos relacionados en el documento seleccionado.",
                "sources": [],
            }

        combined_results = []

        for document, metadata in zip(documents, metadatas):
            score = self._score_result(
                question=question,
                document=document,
                metadata=metadata,
            )

            combined_results.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "score": score,
                }
            )

        combined_results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        top_score = combined_results[0]["score"]

        if top_score > 0:
            combined_results = [
                item for item in combined_results if item["score"] == top_score
            ]

        context_parts = []

        for index, item in enumerate(combined_results):
            document = item["document"]
            metadata = item["metadata"]

            context_parts.append(
                f"Fuente {index + 1}: "
                f"{metadata['file_name']}, página {metadata['page_number']}\n"
                f"{document}"
            )

        context = "\n\n---\n\n".join(context_parts)

        selected_document_text = ""

        if file_name:
            selected_document_text = (
                f"\nEl usuario seleccionó específicamente el documento: {file_name}.\n"
                "Respondé únicamente usando información de ese documento.\n"
            )

        prompt = f"""
Sos un asistente que responde preguntas usando únicamente la información de documentos PDF.
{selected_document_text}

Reglas:
- Respondé solo con la información que aparece en el contexto.
- Si el contexto contiene información parcial, respondé con esa información y aclaralo.
- Solo si el contexto no contiene nada relacionado con la pregunta, decí: "No encuentro información suficiente en el documento seleccionado para responder eso."
- No inventes datos.
- Respondé en español claro.
- Separá la respuesta en párrafos breves.
- Si corresponde, usá viñetas para que la respuesta sea más fácil de leer.
- Cuando corresponda, mencioná de qué documento o página sale la información.
- Si hay varias fuentes parecidas, priorizá la fuente cuyo título, nombre de archivo o contenido coincida mejor con la pregunta del usuario.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""

        answer = self.chat_provider.generate_answer(prompt)

        sources = []

        for item in combined_results:
            metadata = item["metadata"]

            sources.append(
                {
                    "file_name": metadata["file_name"],
                    "page_number": metadata["page_number"],
                    "chunk_index": metadata["chunk_index"],
                }
            )

        return {
            "question": question,
            "selected_document": file_name,
            "answer": answer.strip(),
            "sources": sources,
        }