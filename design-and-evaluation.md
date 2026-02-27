## 1. Design and Architecture Decisions

### 1.1 System Overview

The system is a Retrieval-Augmented Generation (RAG) pipeline designed to answer domain-specific questions using a combination of:

- A vector database for semantic search
- Embedding models for text encoding
- An LLM for final answer generation
- A simple API/web service wrapping the retrieval + generation workflow

This architecture enables accurate, context-grounded answers with minimal hallucination.

---

### 1.2 Key Design Decisions

#### A. Choice of Vector Database: Chroma

Decision: Use Chroma as the vector store
Reasoning:

- Lightweight, simple to set up locally and in cloud environments
- Persistent storage supported (`persist_directory`)
- Well-integrated with LangChain
- Good performance for small/medium projects

---

#### B. Embeddings Provider: OpenAI Embeddings

Decision: Use `OpenAIEmbeddings` (text-embedding-3-large or small variant)
Reasoning:

- High-quality, dense embeddings with strong semantic accuracy
- Better retrieval results vs. open-source embedding models for the same amount of text
- Simple API usage and LangChain integration

---

#### C. Retrieval Method: Similarity Search (k=5)

Decision: Use cosine similarity search with `k=5`
Reasoning:

- Performs well for Q&A use cases
- Balances context relevance and LLM context window usage
- Avoids overwhelming the model with too many irrelevant results

---

#### D. LLM Integration: OpenAI Chat Completions

Decision: Use OpenAI ChatCompletion API to synthesize final answers
Reasoning:

- Ability to generate coherent, grounded responses
- Supports system prompts for controlling hallucination
- Good latency for real-time inference

---

#### E. Pipeline Structure

Decision: Implement modularized components:

- `get_vector_db()`
- `retrieve()`
- `generate_answer()` (in main service)

Reasoning:

- Easy to test individually
- Easy to swap components (e.g., embeddings, LLMs, vector stores)
- Cleaner code organization

---

#### F. Deployment Environment

Decision: Deploy as a web service on Render
Reasoning:

- Simple, free-tier friendly
- Built-in environment variable support
- Good for lightweight Python web apps

---

# 2. Evaluation of the RAG System

## 2.1 Evaluation Methodology

We evaluated the RAG system using a curated set of 25 policy-related questions covering PTO, security, remote work, acceptable use, reimbursement, onboarding, HR, and conduct.
For each question, we measured:

### A. Answer Quality

1. Groundedness
   Whether the answer is fully supported by retrieved evidence and contains _no hallucinations_.

2. Citation Accuracy
   Whether the RAG system cited the correct document chunks that actually supported its claims.

3. (Optional) Gold Answer Matching
   Not performed for this iteration.

### B. System Metrics

- Latency (p50, p95) from question → final answer
- Retrieval and generation time combined

### C. Approach

- Each question was run through the full RAG pipeline (`similarity_search()` → LLM synthesis).
- Retrieved context and generated answers were manually inspected to assess grounding and citation accuracy.
- Latency was automatically recorded by the evaluation script.

---

## 2.2 Evaluation Results

### A. Groundedness

Observed groundedness: 88%

Out of 25 evaluation questions, 22 answers were fully or mostly grounded in retrieved evidence.
Three answers partially relied on inference rather than explicit policy text, especially in cases where the policy document did not contain the needed information (e.g., “working from another country,” data classification).

Common causes of reduced groundedness:

- Questions not explicitly addressed in the uploaded policies
- LLM attempting to “fill in gaps” when documents lacked a clear answer
- Cross-document interpretation that introduced assumptions

---

### B. Citation Accuracy

While citation accuracy was not scored numerically, qualitative review showed:

- Most answers cited the correct chunk(s)
- In a few cases, the RAG system inferred rules without explicit citation (e.g., data classification), leading to citation mismatch
- Some answers correctly stated “not found,” which improved accuracy and reduced hallucinations

A future improvement would be assigning a percentage score for citation accuracy separately from groundedness.

---

### C. Latency Performance

Latency results from 25 queries:

| Metric      | Result |
| ----------- | ------ |
| p50 latency | 2.42s  |
| p95 latency | 3.57s  |

Interpretation:

- The system responds within ~2.4 seconds for most questions
- Heavier queries requiring more generation or combining multiple retrieved chunks push latency towards ~3.5 seconds
- Performance is acceptable for small-scale internal applications

---

## 2.3 Observations and Interpretation

### Strengths

- High groundedness for well-defined policies
- Minimal hallucinations
- Clear and factual answers when policies exist
- Latency suitable for real-time use
- Retrieval performed consistently (Chroma + OpenAI embeddings worked well)

### Limitations

- Missing policy areas produced speculative answers
- LLM occasionally inferred organizational norms not supported in data
- Citation accuracy weakened when retrieved chunks lacked explicit statements
- No hybrid search (semantic + keyword), which might improve edge-case retrieval
