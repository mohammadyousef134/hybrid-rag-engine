import json
import time
from pathlib import Path

from chunking.bm25_store import build_bm25_index
from chunking.vector_store import load_all_chunks_from_chroma
from retrieval.fusion import hybrid_query
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer
from evaluation.grading import grade_correctness

ROOT = Path(__file__).resolve().parents[1]

BATCH_SIZE = 7
WAIT_BETWEEN_BATCHES = 60  # seconds

synced_chunks = load_all_chunks_from_chroma()
build_bm25_index(synced_chunks)

with open(ROOT / "data" / "eval" / "golden_qa.json", "r", encoding="utf-8") as f:
    golden_qa = json.load(f)

results = []
batches = [golden_qa[i:i + BATCH_SIZE] for i in range(0, len(golden_qa), BATCH_SIZE)]

for batch_num, batch in enumerate(batches, start=1):
    print(f"\n--- Batch {batch_num}/{len(batches)} ---")

    for item in batch:
        question = item["question"]
        expected_answer = item["expected_answer"]
        category = item["category"]

        fused = hybrid_query(question, top_k=10)
        top_chunks = rerank(question, fused, top_k=3)
        answer = generate_answer(question, top_chunks)

        grade = grade_correctness(question, expected_answer, answer)
        verdict = "INCORRECT" if "INCORRECT" in grade else "CORRECT"

        results.append({
            "question": question,
            "category": category,
            "verdict": verdict,
        })

        print(f"[{verdict}] ({category}) {question}")

    if batch_num < len(batches):
        print(f"Waiting {WAIT_BETWEEN_BATCHES}s before next batch...")
        time.sleep(WAIT_BETWEEN_BATCHES)

correct_count = sum(1 for r in results if r["verdict"] == "CORRECT")
total = len(results)

print(f"\nOverall accuracy: {correct_count}/{total} ({correct_count / total:.0%})")
print(f"Processed questions: {total}/{len(golden_qa)}")