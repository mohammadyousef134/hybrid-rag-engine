from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def verify_citations(answer: str | None, chunks: list[dict]) -> str | None:
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(f"[{i}] {chunk['text']}")
    context = "\n\n".join(context_blocks)

    prompt = f"""Below is an answer that cites numbered sources like [1], [2], etc.
For each citation in the answer, check whether the claim it's attached to is actually supported by that numbered source.

Sources:
{context}

Answer to check:
{answer}

For each citation number used in the answer, respond with:
[N] - SUPPORTED or NOT SUPPORTED, with a one-sentence reason.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text

def build_prompt(question: str, chunks: list[dict]) -> str:
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        blocks.append(f"[{i}] {chunk['text']}")

    context = "\n\n".join(blocks)

    prompt = f"""Answer the question using ONLY the context below. 
Cite the source of each claim using the bracketed number, like [1] or [2].
If the context doesn't contain enough information to answer, say so clearly instead of guessing.

Context:
{context}

Question: {question}

"""

    return prompt


def generate_answer(question: str, chunks: list[dict]) -> str | None:
    prompt = build_prompt(question, chunks)

    answer = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    ).text


    return answer