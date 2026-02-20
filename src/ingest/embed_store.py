import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from src.ingest.chunk_docs import chunk_text
from src.embed import embed_chunks
import chromadb


CHUNK_FILE = Path("data/chunks.txt")

def build_db():

    client = chromadb.PersistentClient(path="data/chroma")
    collection = client.create_collection(name="policies", metadata={"hnsw:space": "cosine"}, get_or_create=True)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    items = CHUNK_FILE.read_text().splitlines()
    ids, texts, meta = [], [], []

    for line in items:
        parts = line.split("||", 2)
        if len(parts) != 3:
            print(f"Skipping malformed line: {line}")
            continue
        doc, chunk_id, text = parts
        chunk_id_full = f"{doc}-{chunk_id}"

        ids.append(chunk_id_full)
        texts.append(text)
        meta.append({"doc": doc, "chunk": chunk_id})

    embeddings = model.encode(texts, convert_to_numpy=True)

    collection.add(ids=ids, documents=texts, metadatas=meta, embeddings=embeddings)
    print("Vector DB built successfully.")

if __name__ == "__main__":
    build_db()
