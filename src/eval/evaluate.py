import time
from src.rag.retrieve import retrieve
from src.rag.generate import generate_answer

# Sample evaluation questions
questions = [
    # PTO / Holidays
    "How many PTO days does a full-time employee receive per year?",
    "Do unused PTO days carry over to the next year?",
    "What is the company’s paid holiday schedule?",
    "How do employees request time off?",
    "Is sick leave separate from PTO?",

    # Remote Work / IT
    "What is the VPN requirement for remote work?",
    "Are employees allowed to access company systems from personal devices?",
    "What are the rules for working from another country?",
    "What security steps must employees follow when working remotely?",
    "What is the password policy for company systems?",

    # Security / Compliance
    "How do I report a security incident?",
    "What should I do if I suspect phishing?",
    "What are the acceptable use rules for email and communication tools?",
    "Are employees permitted to install unauthorized software?",
    "What is the data classification policy?",

    # Expense / Finance
    "What expenses are eligible for reimbursement?",
    "How do employees submit an expense report?",
    "What is the per-diem limit for business travel?",
    "Are home-office expenses reimbursable?",
    "How long does reimbursement processing take?",

    # HR / Employment
    "What is the parental leave policy?",
    "What is the onboarding process for new employees?",
    "How do employees update their personal information?",
    "What is the workplace code of conduct?",
    "What is the performance review cycle?",
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
