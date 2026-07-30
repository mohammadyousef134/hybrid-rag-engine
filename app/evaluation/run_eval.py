import json

from chunking.bm25_store import build_bm25_index
from chunking.vector_store import load_all_chunks_from_chroma
from retrieval.fusion import hybrid_query
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer
from evaluation.grading import grade_correctness
from pathlib import Path
root = Path(__file__).parent.parent.parent

synced_chunks = load_all_chunks_from_chroma()
build_bm25_index(synced_chunks)

with open(f"{root}/data/eval/golden_qa.json", "r", encoding="utf-8") as f:
    golden_qa = json.load(f)


results = []

for i, item in enumerate(golden_qa):
    if i >= 7:
        break
    question = item["question"]
    expected_answer = item["expected_answer"]
    category = item["category"]

    fused = hybrid_query(question, top_k=10)
    top_chunks = rerank(question, fused, top_k=3)
    answer = generate_answer(question, top_chunks)

    grade = grade_correctness(question, expected_answer, answer)

    verdict = "INCORRECT" if grade.__contains__("INCORRECT") else "CORRECT"
    results.append({
        "question": question,
        "category": category,
        "verdict": verdict,
    })
    print(f"[{verdict}] ({category}) {question}")

correct_count = sum(1 for r in results if r["verdict"] == "CORRECT")
total = len(results)

print(f"\nOverall accuracy: {correct_count}/{total} ({correct_count/total:.0%})")