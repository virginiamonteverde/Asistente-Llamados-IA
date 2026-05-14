from flask import Flask, render_template, request

from services.rag_service import RagService

app = Flask(__name__)

rag_service = RagService()


@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = None
    sources = []
    error = None
    selected_document = ""

    documents = rag_service.list_documents()

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_document = request.form.get("selected_document", "").strip()

        if not selected_document:
            error = "Tenés que seleccionar un documento antes de hacer una pregunta."

        elif not question:
            error = "Tenés que escribir una pregunta."

        else:
            try:
                result = rag_service.ask(
                    question=question,
                    file_name=selected_document,
                    n_results=2,
                )

                answer = result.get("answer")
                sources = result.get("sources", [])

            except Exception as e:
                error = f"Ocurrió un error al consultar el documento: {e}"

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        sources=sources,
        error=error,
        documents=documents,
        selected_document=selected_document,
    )


if __name__ == "__main__":
    app.run(debug=True)