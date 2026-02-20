# Company Policy RAG System

This project is a Retrieval-Augmented Generation (RAG) application that answers questions about internal company policies. It uses a local vector store (Chroma) and the OpenRouter API for LLM inference.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Company Policy RAG Application
This project is a Retrieval-Augmented Generation (RAG) system that answers questions about a synthetic company-policy corpus using free-tier models from OpenRouter, local embeddings, and a local Chroma vector database.
🚀 Features
Local document ingestion (PDF, Markdown, HTML, TXT)
Deterministic chunking and processing (seeded)
Local embedding using sentence-transformers
Chroma vector database for storage
RAG retrieval + generation pipeline
FastAPI web application with:
/ — User chat UI
/chat — RAG API
/health — Health check
Fully compatible with OpenRouter free-tier models
Ready for deployment on Render/Railway
📦 1. Setup
Clone the repo
git clone <your-repo-url>
cd rag-app
Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
Install dependencies
pip install -r requirements.txt
Set up environment variables
Create a .env file:
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=mistral-small # default free-tier
📚 2. Ingest Documents
Place all policy documents into:
data/corpus/
Run ingestion:
python -m src.ingest.load_docs
python -m src.ingest.chunk_docs
python -m src.ingest.embed_store
This will create:
data/chroma/
(vector index)
💬 3. Run the Web App
uvicorn src.app.main:app --reload
Visit:
http://localhost:8000
🧪 4. Run Deterministic Seeds
python seed.py
📄 5. Project Structure
(Already shown above)
📊 6. Evaluation & Metrics
Evaluation scripts will be added in /src/eval/ (later steps).
✅ Step 1 is complete.
✅ STEP 2 — Ingestion & Indexing
We now build three modules:
✔ load_docs.py — load + clean documents
✔ chunk_docs.py — deterministic chunking
✔ embed_store.py — embed & store chunks in Chroma
Below are the complete production-ready files.
