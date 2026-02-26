import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"


def get_client():
    """
    Lazy-load the OpenAI client only when embeddings are needed.
    Works in GitHub Actions (import-safe) and Render (runtime env vars available).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Embeddings cannot be created.")

    return OpenAI(api_key=api_key)


def embed_chunks(chunks):
    client = get_client()   # Only created when actually needed

    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=chunks
    )
    return [d.embedding for d in resp.data]