import chromadb

def store_embeddings(chunks, embeddings):
    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name="policies",
        metadata={"hnsw:space": "cosine"}
    )

    ids = [f"chunk-{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
