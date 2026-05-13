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

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            try:
                result = rag_service.ask(question, n_results=5)

                answer = result.get("answer")
                sources = result.get("sources", [])

            except Exception as e:
                error = f"Ocurrió un error al consultar los documentos: {e}"

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        sources=sources,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)