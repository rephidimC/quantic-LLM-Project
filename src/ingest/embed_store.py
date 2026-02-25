import chromadb
from pathlib import Path
from src.embed import embed_chunks

CHUNK_FILE = Path("data/chunks.txt")


def build_db():
    client = chromadb.PersistentClient(path="data/chroma")

    # Always recreate collection cleanly
    try:
        client.delete_collection("policies")
    except Exception:
        pass

    collection = client.create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"}
    )

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

    # 🔥 USE CENTRAL EMBEDDING FUNCTION
    embeddings = embed_chunks(texts)

    print("Embedding dimension:", len(embeddings[0]))

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=meta,
        embeddings=embeddings
    )

    print("Vector DB built successfully.")


if __name__ == "__main__":
    build_db()