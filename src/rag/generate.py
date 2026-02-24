import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

LLM_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "meta-llama/llama-3.1-8b-instruct"
)

MAX_TOKENS = 500


def build_prompt(query, docs):
    context = ""

    for doc in docs:
        context += f"[{doc.metadata['doc']} - {doc.metadata['chunk']}]: {doc.page_content}\n"

    return f"""
You are an assistant answering company policy questions only.
Do not provide information outside the given context. 
Cite sources in [doc_id - chunk_id] format.

Context:
{context}

Question: {query}

Answer concisely and cite sources in [doc - chunk] format.
"""


def generate_answer(query, docs):
    prompt = build_prompt(query, docs)

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS
    )

    return resp.choices[0].message.content