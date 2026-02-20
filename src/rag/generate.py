import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENAI_API_BASE"))

LLM_MODEL = os.getenv("OPENROUTER_MODEL", "mistral-small")

MAX_TOKENS = 500

def build_prompt(query, docs):
    context = ""
    for i, doc in enumerate(docs):
        context += f"[{doc.metadata['doc']} - {doc.metadata['chunk']}]: {doc.page_content}\n"

    prompt = f"""
You are an assistant answering questions only about our company policies. 
Do not provide information outside the given context. 
Cite sources in [doc_id - chunk_id] format.

Context:
{context}

Question: {query}

Answer concisely and cite source doc IDs.
Max length: {MAX_TOKENS} tokens.
"""
    return prompt

def generate_answer(query, docs):
    prompt = build_prompt(query, docs)
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS
    )
    return resp.choices[0].message.content
