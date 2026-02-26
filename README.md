# Quantic LLM Policy Assistant

This project is a **RAG-based LLM app** that answers company policy questions using local documents. It uses **FastAPI**, **ChromaDB**, **HuggingFace/OpenRouter embeddings**, and a **local corpus** of Markdown files.

---

# Step 1 — Project Setup

1. Clone the repository:

```bash
git clone <repo_url>
cd quantic-LLM-Project
```

2. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file at the root with your API keys:

```
OPENROUTER_API_KEY=<your_openrouter_key>
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

For OpenAI (optional):

```
OPENAI_API_KEY=<your_openai_key>
```

---

# Step 2 — Prepare Document Corpus

1. Add your company policy documents in Markdown format inside:

```
./data/corpus/
```

2. Process documents into chunks (optional preprocessing):

```bash
python src/ingest/load_docs.py
python src/ingest/chunk_docs.py
```

3. Build the embedding store in ChromaDB:

```bash
python src/ingest/embed_store.py
```

- ChromaDB will persist to `./data/chroma/`

---

# Step 3 — Embeddings Setup

- `src/embed.py` handles embeddings using OpenRouter or OpenAI.
- Example usage:

```python
from src.embed import embed_chunks

chunks = ["Example text to embed"]
embeddings = embed_chunks(chunks)
```

- **Environment variables** must be set for API keys.

---

# Step 4 — RAG Retrieval and LLM

- `src/rag/retrieve.py` — fetches top-K relevant document chunks from Chroma.
- `src/rag/generate.py` — uses OpenRouter LLM to answer questions based on retrieved context.

Example usage:

```python
from src.rag.retrieve import retrieve
from src.rag.generate import generate_answer

docs = retrieve("What is the remote work policy?")
answer = generate_answer("What is the remote work policy?", docs)
print(answer)
```

- The **LLM prompt** includes context and cites sources in `[doc - chunk]` format.

---

# Step 5 — Run FastAPI App Locally

1. Start the app:

```bash
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Open in your browser:

```
http://127.0.0.1:8000
```

3. Enter a query in the provided text box to test the RAG system.

---

# Step 6 — Deployment on Render

1. Select **Web Service**.
2. Connect your GitHub repository.
3. Set build and start commands:

```bash
# Build (optional if dependencies are in requirements.txt)
pip install -r requirements.txt

# Start
uvicorn src.app.main:app --host 0.0.0.0 --port $PORT
```

4. Set environment variables in Render dashboard (same as `.env`):

- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`

5. Deploy the service. After a few minutes, your API should be live.

---

# Step 7 — CI/CD with GitHub Actions

- Workflow: `.github/workflows/python-app.yml`

Example:

```yaml
name: Python CI

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt

      - name: Run smoke test
        run: python -c "import src.app.main"
```

**Notes:**

- Secrets must be set in GitHub Actions for OpenRouter or OpenAI keys.
- Workflow runs automatically on pushes or pull requests to `master`.
- Smoke test ensures imports are correct; it **does not start the server**.

---

# Step 8 — Local Evaluation

- File: `src/eval/evaluate.py`
- This script runs **locally only**; cannot run on Render.
- Usage:

```bash
python src/eval/evaluate.py
```

- Evaluates your LLM + retrieval performance against a test dataset or sample queries.

---

# Step 9 — File Structure Overview

```
.
├── .env
├── requirements.txt
├── README.md
├── src/
│   ├── app/
│   │   ├── main.py
│   │   └── templates/
│   ├── rag/
│   │   ├── retrieve.py
│   │   └── generate.py
│   ├── ingest/
│   │   ├── load_docs.py
│   │   ├── chunk_docs.py
│   │   └── embed_store.py
│   ├── eval/
│   │   └── evaluate.py
│   ├── embed.py
│   └── utils.py
├── data/
│   ├── corpus/
│   ├── processed/
│   └── chroma/
└── .github/workflows/python-app.yml
```

---

# Step 10 — Notes & Tips

- Always activate your virtual environment before running scripts locally:

```bash
source venv/bin/activate
```

- `.env` keys are required for both **embedding** and **LLM** calls.
- Render **Web Service** cannot run `evaluate.py`; use it locally.
- ChromaDB persists locally in `./data/chroma/`. For production, you may want **cloud persistence**.
