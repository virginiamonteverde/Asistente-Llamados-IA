from pathlib import Path

import fitz  # PyMuPDF


def read_pdfs_from_folder(folder_path: str) -> list[dict]:
    """
    Lee todos los PDFs de una carpeta y extrae el texto página por página.

    Devuelve una lista de diccionarios.
    Cada diccionario representa una página de un PDF.

    Ejemplo de salida:
    {
        "file_name": "inspector.pdf",
        "page_number": 1,
        "text": "Texto extraído de la página..."
    }
    """

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"No existe la carpeta: {folder_path}")

    pdf_files = list(folder.glob("*.pdf"))

    pages = []

    for pdf_file in pdf_files:
        document = fitz.open(pdf_file)

        for page_index, page in enumerate(document):
            text = page.get_text()

            if text.strip():
                pages.append(
                    {
                        "file_name": pdf_file.name,
                        "page_number": page_index + 1,
                        "text": text,
                    }
                )

        document.close()

    return pages