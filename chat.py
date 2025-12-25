import requests
import os

OPENROUTER_API_KEY = "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"


SYSTEM_PROMPT = """
You are MentorAI, an educational assistant.
Always return lists line by line, numbered, with one item per line.
Do not merge items into paragraphs.
Do not duplicate items.
Use simple language suitable for high school students.
"""

def generate_response(messages):
    try:
        
        prompt_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "xiaomi/mimo-v2-flash:free",
                "messages": prompt_messages,
            },
            timeout=30,
        )

        data = response.json()

        if "error" in data:
            return f"⚠️ AI service error: {data['error']}"
        if "choices" not in data or not data["choices"]:
            return "⚠️ AI service returned unexpected response"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ AI error: {str(e)}"
