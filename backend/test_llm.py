from llm.groq_client_fixed import generate_answer
from rag.pipeline import search

test_cases = [
    {"question": "What is BIS certification process?", "expected_topic": "certification"},
    {"question": "How to get hallmark for gold jewellery?", "expected_topic": "hallmark"},
]

for tc in test_cases:
    print(f"\n=== Testing: {tc['question']} ===")
    chunks = search(tc['question'], top_k=5)
    print(f"Retrieved {len(chunks)} chunks from sources: {[c['title'][:50] for c in chunks]}")
    result = generate_answer(tc['question'], chunks)
    print(f"Answer length: {len(result['answer'].split())} words")
    print("Answer preview:", result['answer'][:200], "...")

