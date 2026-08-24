import json
import time
from pathlib import Path

from chunking.bm25_store import build_bm25_index
from chunking.vector_store import load_all_chunks_from_chroma
from retrieval.fusion import hybrid_query
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer
from evaluation.grading import grade_correctness
from evaluation.retrieval_metrics import precision_at_k, recall_at_k, reciprocal_rank, average

ROOT = Path(__file__).resolve().parents[1]

# Gemini allows 15 requests per minute.
# Each question uses 2 requests: one for generation and one for grading.
# Keep this at 7 to stay safely below the limit (14 requests per batch).
BATCH_SIZE = 7
WAIT_BETWEEN_BATCHES = 60  # seconds
RETRIEVAL_TOP_K = 10  # chunks considered for precision/recall/MRR

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
        expected_source_file = item["source_file"]
        category = item["category"]

        fused = hybrid_query(question, top_k=RETRIEVAL_TOP_K)
        top_chunks = rerank(question, fused, top_k=3)
        answer = generate_answer(question, top_chunks)

        grade = grade_correctness(question, expected_answer, answer)
        verdict = "INCORRECT" if "INCORRECT" in grade else "CORRECT"

        results.append({
            "question": question,
            "category": category,
            "verdict": verdict,
            "precision": precision_at_k(fused, expected_source_file),
            "recall": recall_at_k(fused, expected_source_file),
            "reciprocal_rank": reciprocal_rank(fused, expected_source_file),
        })

        print(f"[{verdict}] ({category}) {question}")

    if batch_num < len(batches):
        print(f"Waiting {WAIT_BETWEEN_BATCHES}s before next batch...")
        time.sleep(WAIT_BETWEEN_BATCHES)

correct_count = sum(1 for r in results if r["verdict"] == "CORRECT")
total = len(results)

mean_precision = average([r["precision"] for r in results])
mean_recall = average([r["recall"] for r in results])
mean_mrr = average([r["reciprocal_rank"] for r in results])

print(f"\nOverall accuracy: {correct_count}/{total} ({correct_count / total:.0%})")
print(f"Processed questions: {total}/{len(golden_qa)}")
print(f"\nRetrieval quality (top {RETRIEVAL_TOP_K}, before rerank):")
print(f"  Precision@{RETRIEVAL_TOP_K}: {mean_precision:.2f}")
print(f"  Recall@{RETRIEVAL_TOP_K}:    {mean_recall:.2f}")
print(f"  MRR:            {mean_mrr:.2f}")