import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vector_db():
    key = os.getenv("OPENAI_API_KEY")
    print("Loaded OPENAI_API_KEY?", bool(key))  # Debug
    if not key:
        raise ValueError("OPENAI_API_KEY not found in environment.")

    embedding = OpenAIEmbeddings(api_key=key)

    vectordb = Chroma(
        collection_name="policies",
        persist_directory="data/chroma",
        embedding_function=embedding
    )

    return vectordb

def retrieve(query: str, k: int = 5):
    vectordb = get_vector_db()
    docs = vectordb.similarity_search(query, k=k)
    return docs