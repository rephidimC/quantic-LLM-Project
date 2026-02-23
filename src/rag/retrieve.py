from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize embeddings
# embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma vector store
vectordb = Chroma(
    collection_name="policies",
    persist_directory="data/chroma",
    # embedding_function=embedding
)

# Retrieval function
def retrieve(query: str, k: int = 5):
    docs = vectordb.similarity_search(query, k=k)
    return docs