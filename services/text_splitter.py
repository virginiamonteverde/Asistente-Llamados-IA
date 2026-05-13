def split_pages_into_chunks(
    pages: list[dict],
    chunk_size: int = 1800,
    chunk_overlap: int = 300,
) -> list[dict]:
    """
    Divide el texto de las páginas en fragmentos más pequeños.

    Recibe una lista de páginas como las que devuelve pdf_reader.py:

    {
        "file_name": "inspector.pdf",
        "page_number": 1,
        "text": "Texto de la página..."
    }

    Devuelve una lista de fragmentos:

    {
        "file_name": "inspector.pdf",
        "page_number": 1,
        "chunk_index": 0,
        "text": "Fragmento de texto..."
    }
    """

    chunks = []

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "file_name": page["file_name"],
                        "page_number": page["page_number"],
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                    }
                )

            start += chunk_size - chunk_overlap
            chunk_index += 1

    return chunks