import requests
import os

OPENROUTER_API_KEY = "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"


SYSTEM_PROMPT = """
You are MentorAI, an educational assistant.
Always answer in numbered lists.
One idea per line.
Use simple language for high school students.
Do not repeat points.
"""

# =========================
# AI RESPONSE GENERATOR
# =========================
def generate_response(messages):
    try:
        payload = {
            "model": "xiaomi/mimo-v2-flash:free",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        data = response.json()

        if "choices" not in data:
            return "⚠️ AI error. Try again."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ AI service error: {str(e)}"
