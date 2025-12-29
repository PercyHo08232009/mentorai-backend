import requests
import os

OPENROUTER_API_KEY = "ENTER_YOUR_API_OPENROUTER_KEY"


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
            "model": "ENTER YOUR MODEL",
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
<<<<<<< HEAD
        return f"⚠️ AI service error: {str(e)}"
=======
        return f"⚠️ AI service error: {str(e)}"
>>>>>>> 338342138b282483579892c59b03a2491140a888
