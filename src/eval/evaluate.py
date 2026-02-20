import time
from src.rag.retrieve import retrieve
from src.rag.generate import generate_answer

# Sample evaluation questions
questions = [
    "How many PTO days does a full-time employee get?",
    "What is the remote work VPN requirement?",
    "How do I report a security incident?",
    "What are the acceptable use rules for email?",
    "Describe parental leave policy",
]

def eval_groundedness_and_latency():
    latencies = []
    grounded_correct = 0

    for q in questions:
        start = time.time()
        docs = retrieve(q, k=5)
        answer = generate_answer(q, docs)
        latency = time.time() - start
        latencies.append(latency)

        # Simple groundedness check: answer mentions at least one source doc ID
        if any(doc.metadata['doc'] in answer for doc in docs):
            grounded_correct += 1

        print(f"Q: {q}\nAnswer: {answer}\nLatency: {latency:.2f}s\n---")

    p50 = sorted(latencies)[len(latencies)//2]
    p95 = sorted(latencies)[int(len(latencies)*0.95)-1]

    print(f"Groundedness: {grounded_correct/len(questions)*100:.2f}%")
    print(f"Latency p50: {p50:.2f}s, p95: {p95:.2f}s")

if __name__ == "__main__":
    eval_groundedness_and_latency()
