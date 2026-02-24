import numpy as np
from sentence_transformers import SentenceTransformer

# Lightweight model suitable for CPU / Render
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks):
    """
    Convert text chunks into embedding vectors.
    """
    if isinstance(chunks, str):
        chunks = [chunks]

    vectors = model.encode(chunks, show_progress_bar=False)

    return [v.tolist() for v in vectors]