import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Use OFFICIAL OpenAI for embeddings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

EMBED_MODEL = "text-embedding-3-small"

def embed_chunks(chunks):
    vectors = []

    for chunk in chunks:
        resp = client.embeddings.create(
            model=EMBED_MODEL,
            input=chunk
        )
        vectors.append(resp.data[0].embedding)

    return vectors