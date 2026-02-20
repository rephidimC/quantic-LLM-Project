from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.rag.retrieve import retrieve
from src.rag.generate import generate_answer

app = FastAPI()
templates = Jinja2Templates(directory="src/app/templates")

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Web UI
@app.get("/")
async def chat_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat API endpoint
@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return JSONResponse({"error": "No query provided"}, status_code=400)

    docs = retrieve(query, k=5)
    answer = generate_answer(query, docs)
    return {"answer": answer, "sources": [doc.metadata['doc'] for doc in docs]}
