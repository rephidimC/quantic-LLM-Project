import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "meta-llama/llama-3.1-8b-instruct"
)

MAX_TOKENS = 500


def get_client():
    """Create the OpenRouter client only when needed (lazy load)."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


def build_prompt(query, docs):
    context = ""

    for doc in docs:
        context += f"[{doc.metadata['doc']} - {doc.metadata['chunk']}]: {doc.page_content}\n"

    return f"""
You are an assistant answering company policy questions only.
Do not provide information outside the given context. 
Cite sources in [doc - chunk] format.

Context:
{context}

Question: {query}

Answer concisely and cite sources in [doc - chunk] format.
"""


def generate_answer(query, docs):
    """RAG generation with lazy-loaded client."""
    client = get_client()

    prompt = build_prompt(query, docs)

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS
    )

    return resp.choices[0].message.content