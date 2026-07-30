from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def grade_correctness(question: str, expected_answer: str, answer: str) -> str:
    prompt = f"""You are grading whether an AI-generated answer is correct.

Question: {question}
Expected answer: {expected_answer}
AI's actual answer: {answer}

Does the AI's answer correctly convey the same information as the expected answer?
Minor differences in wording or extra correct detail are fine — focus on whether the core facts match.

Respond in exactly this format:
VERDICT: CORRECT or INCORRECT
REASON: one sentence explaining why
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )
    return response.text
