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


def format_sources(docs):
    """
    Extract and deduplicate sources from retrieved documents.
    This guarantees a clean 'Sources' section independent of LLM output.
    """
    seen = set()
    sources = []

    for doc in docs:
        doc_id = doc.metadata.get("doc", "unknown")
        chunk_id = doc.metadata.get("chunk", "unknown")

        key = f"{doc_id}-{chunk_id}"

        if key not in seen:
            seen.add(key)
            sources.append(f"[{doc_id} - {chunk_id}]")

    return "\n".join(sources)


def generate_answer(query, docs):
    """RAG generation with lazy-loaded client + structured sources."""
    client = get_client()

    prompt = build_prompt(query, docs)

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS
    )

    answer = resp.choices[0].message.content.strip()

    # ✅ Add clean sources section
    sources = format_sources(docs)

    return f"{answer}\n\nSources:\n{sources}"