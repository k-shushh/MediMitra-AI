
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_disease(disease: str, user_input: str) -> dict:

    prompt = f"""
A user described their symptoms as: "{user_input}"
The predicted disease is: {disease}

Respond ONLY with a valid JSON object — no extra text, no markdown, no backticks.
Use exactly these keys:
{{
  "about": "2-3 sentences explaining what this condition is in simple language",
  "causes": "2-3 sentences on why it may occur or what triggers it",
  "precautions": "3-4 short practical precautions as a single string, each separated by a newline"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant. Always respond with valid JSON only."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.4
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "about":       raw,
            "causes":      "Could not parse structured response.",
            "precautions": "Please consult a qualified doctor for guidance."
        }