from langchain_community.vectorstores import Chroma
from src.embed import embed_chunks

def get_vector_db():
    vectordb = Chroma(
        collection_name="policies",
        persist_directory="data/chroma"
    )
    return vectordb

def retrieve(query: str, k: int = 5):
    vectordb = get_vector_db()
    query_vector = embed_chunks(query)[0]

    docs = vectordb.similarity_search_by_vector(
        embedding=query_vector,
        k=k
    )

    return docs