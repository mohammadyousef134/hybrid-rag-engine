import time
import json
from pathlib import Path

from ingestion.load_document import load_document
from chunking.chunk_document import chunk_document
from chunking.schema.chunk import reset_chunk_counter
from chunking.vector_store import store_chunks, load_all_chunks_from_chroma, clear_collection
from chunking.bm25_store import build_bm25_index
from retrieval.fusion import hybrid_query
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer
from evaluation.grading import grade_correctness
ROOT = Path(__file__).resolve().parents[2]


FILES = [
    str(ROOT / "data" / "raw" / "cloud_computing.md"),
    str(ROOT / "data" / "raw" / "security_basics.md"),
]

STRATEGIES = ["fixed_size", "structure_aware", "semantic"]

BATCH_SIZE = 7
WAIT_BETWEEN_BATCHES = 60

with open(ROOT / "data" / "eval" / "golden_qa.json", "r", encoding="utf-8") as f:
    golden_qa = json.load(f)

comparison = {}
batches = [golden_qa[i:i + BATCH_SIZE] for i in range(0, len(golden_qa), BATCH_SIZE)]

for strategy in STRATEGIES:
    print(f"\n{'='*20} STRATEGY: {strategy} {'='*20}")

    clear_collection()
    for filename in FILES:
        reset_chunk_counter(filename)
        docs = load_document(filename)
        for doc in docs:
            chunks = chunk_document(doc, strategy=strategy)
            store_chunks(chunks)

    synced_chunks = load_all_chunks_from_chroma()
    build_bm25_index(synced_chunks)

    results = []
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

            results.append({"category": category, "verdict": verdict})
            print(f"[{verdict}] ({category}) {question}")

        if batch_num < len(batches):
            print(f"Waiting {WAIT_BETWEEN_BATCHES}s before next batch...")
            time.sleep(WAIT_BETWEEN_BATCHES)

    comparison[strategy] = results


print(f"\n{'='*20} COMPARISON {'='*20}")

for strategy, results in comparison.items():
    correct = sum(1 for r in results if r["verdict"] == "CORRECT")
    total = len(results)
    print(f"{strategy}: {correct}/{total} ({correct/total:.0%})")

print()
categories = sorted(set(item["category"] for item in golden_qa))
for category in categories:
    print(f"\n--- {category} ---")
    for strategy, results in comparison.items():
        cat_results = [r for r in results if r["category"] == category]
        correct = sum(1 for r in cat_results if r["verdict"] == "CORRECT")
        total = len(cat_results)
        print(f"{strategy}: {correct}/{total}")