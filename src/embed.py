import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Use OpenAI directly for embeddings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

EMBED_MODEL = "text-embedding-3-small"

def embed_chunks(chunks):
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=chunks
    )

    return [d.embedding for d in resp.data]