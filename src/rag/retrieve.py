from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize embeddings
# embedding = OpenAIEmbeddings(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# # Initialize Chroma vector store
# vectordb = Chroma(
#     collection_name="policies",
#     persist_directory="data/chroma",
#     embedding_function=embedding
# )

# # Retrieval function
# def retrieve(query: str, k: int = 5):
#     docs = vectordb.similarity_search(query, k=k)
#     return docs

def get_vector_db():
    embedding = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    vectordb = Chroma(
        collection_name="policies",
        persist_directory="data/chroma",
        embedding_function=embedding
    )

    return vectordb

# Retrieval function
def retrieve(query: str, k: int = 5):
    vectordb = get_vector_db()
    docs = vectordb.similarity_search(query, k=k)
    return docs