# AI Document Explorer

AI Document Explorer es una aplicación web local en Python que permite hacer preguntas sobre documentos PDF mediante un chat con IA usando RAG.

La idea principal es que el usuario pueda cargar documentos PDF, hacer preguntas en una interfaz web y obtener respuestas basadas en la información contenida en esos documentos, incluyendo las fuentes utilizadas.

## Estado actual

Primera versión funcional.

La aplicación ya permite:

- Leer documentos PDF desde una carpeta local.
- Dividir el contenido en fragmentos.
- Generar embeddings con Ollama.
- Guardar los fragmentos en una base vectorial local con ChromaDB.
- Hacer preguntas desde una interfaz web con Flask.
- Consultar los documentos usando RAG.
- Obtener una respuesta generada por IA.
- Mostrar las fuentes utilizadas.
- Mostrar una barra animada mientras se genera la respuesta.
- Mostrar una interfaz visual moderna y profesional.

## Tecnologías utilizadas

- Python
- Flask
- Ollama
- ChromaDB
- PyMuPDF
- requests
- HTML
- CSS
- Git / GitHub

## Modelos usados con Ollama

Modelo de chat:

```txt
hermes3:8b
```

Modelo de embeddings:

```txt
nomic-embed-text:latest
```

## Arquitectura

El proyecto está pensado para no quedar atado a Ollama.

Flask no llama directamente a Ollama.  
La web utiliza servicios internos, especialmente `RagService`.

La conexión con Ollama está encapsulada en `OllamaProvider`, lo que permitirá cambiar en el futuro a otro proveedor de IA, como OpenAI, Claude, Gemini, Hugging Face u otro, sin rehacer toda la aplicación.

Flujo actual:

```txt
Usuario hace una pregunta
→ Flask recibe la pregunta
→ RagService coordina la consulta
→ Se genera el embedding de la pregunta
→ Se busca contexto relevante en ChromaDB
→ Se arma un prompt con los fragmentos encontrados
→ Ollama genera la respuesta
→ Flask muestra respuesta y fuentes en la web
```

## Estructura del proyecto

```txt
ai_document_explorer/
  app.py
  config.py
  ingest.py
  requirements.txt
  README.md
  .gitignore

  documents/
    archivos PDF locales

  vector_db/
    base vectorial local generada por ChromaDB

  services/
    __init__.py
    pdf_reader.py
    text_splitter.py
    ai_provider.py
    vector_store.py
    rag_service.py

  templates/
    index.html

  static/
    styles.css
```

## Carpetas ignoradas por Git

Las siguientes carpetas no se suben al repositorio:

```txt
documents/
vector_db/
.venv/
```

Motivo:

- `documents/` contiene PDFs locales.
- `vector_db/` contiene la base vectorial generada.
- `.venv/` contiene el entorno virtual local.

Cada instalación debe generar su propia base vectorial ejecutando `ingest.py`.

## Instalación local

Crear y activar entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Requisitos externos

Es necesario tener Ollama instalado y funcionando.

Verificar que Ollama esté activo:

```bash
ollama list
```

Descargar el modelo de embeddings:

```bash
ollama pull nomic-embed-text:latest
```

Descargar el modelo de chat:

```bash
ollama pull hermes3:8b
```

## Configuración

La configuración principal está en:

```txt
config.py
```

Actualmente define:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text:latest"
CHAT_MODEL = "hermes3:8b"
CHROMA_COLLECTION_NAME = "pdf_documents"
```

## Agregar documentos PDF

Colocar los archivos PDF dentro de:

```txt
documents/
```

Ejemplo:

```txt
documents/
  inspector.pdf
  subdirector.pdf
  director_depto_tecnico.pdf
```

## Generar la base vectorial

Después de agregar PDFs, ejecutar:

```bash
python ingest.py
```

Este proceso:

1. Lee los PDFs.
2. Extrae texto por página.
3. Divide el contenido en fragmentos.
4. Genera embeddings con Ollama.
5. Guarda los fragmentos en ChromaDB.

La base se genera en:

```txt
vector_db/
```

## Ejecutar la aplicación web

Ejecutar:

```bash
python app.py
```

Abrir en el navegador:

```txt
http://127.0.0.1:5000
```

## Uso

Desde la web se puede escribir una pregunta sobre los documentos PDF cargados.

Ejemplo:

```txt
¿Cuáles son los requisitos para postularse al llamado de director del departamento técnico?
```

La aplicación devuelve:

- Respuesta generada por IA.
- Fuentes utilizadas.
- Nombre del PDF.
- Página correspondiente.

## Limitaciones actuales

La app funciona bien para preguntas que buscan información dentro de uno o varios fragmentos de documentos.

Ejemplos:

```txt
¿Cuáles son los requisitos del llamado?
¿Qué documentación hay que presentar?
¿Qué funciones tiene el cargo?
¿Qué dice el documento sobre antecedentes?
¿Cuál es el perfil solicitado?
```

Todavía no está optimizada para preguntas comparativas globales que requieren revisar todos los documentos y hacer cálculos o rankings.

Ejemplos:

```txt
¿Qué llamado tiene más requisitos?
¿Cuál es el llamado más exigente?
Comparame todos los llamados.
```

Para ese tipo de preguntas será necesario agregar una lógica específica de análisis por documento.

## Próximas mejoras previstas

- Agregar un selector de documento.
- Permitir consultar todos los documentos o un PDF específico.
- Mejorar la calidad visual de las respuestas con párrafos y listas.
- Mejorar el prompt interno de RAG.
- Agregar lógica especial para preguntas comparativas entre documentos.
- Preparar mejor el sistema para cambiar de proveedor de IA en el futuro.
- Agregar carga de PDFs desde la interfaz web.
- Agregar historial de preguntas y respuestas.

## Estado de la primera versión

Primera versión funcional completada:

- Backend Flask funcionando.
- RAG funcionando.
- Ollama integrado mediante proveedor encapsulado.
- ChromaDB funcionando como base vectorial.
- Interfaz web inicial creada.
- Diseño visual aplicado.
- Consulta desde navegador funcionando.
