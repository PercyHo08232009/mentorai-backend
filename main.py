from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import generate_response
from classifier import is_supported_question

app = FastAPI(title="MentorAI Backend")

# =========================
# CORS (VERY IMPORTANT)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hugging Face requires this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SESSION MEMORY (LIGHT)
# =========================
sessions = {}
MAX_MESSAGES = 6

class ChatRequest(BaseModel):
    session_id: str
    message: str

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"status": "MentorAI backend running"}

# =========================
# CHAT ENDPOINT
# =========================
@app.post("/chat")
def chat(req: ChatRequest):
    if not is_supported_question(req.message):
        return {
            "response": "⚠️ MentorAI only answers learning-related questions."
        }

    if req.session_id not in sessions:
        sessions[req.session_id] = []

    sessions[req.session_id].append({
        "role": "user",
        "content": req.message.strip()
    })

    sessions[req.session_id] = sessions[req.session_id][-MAX_MESSAGES:]

    ai_reply = generate_response(sessions[req.session_id])

    # Deduplicate lines
    seen = set()
    clean_lines = []
    for line in ai_reply.split("\n"):
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            clean_lines.append(line)

    final_reply = "\n".join(clean_lines)

    sessions[req.session_id].append({
        "role": "assistant",
        "content": final_reply
    })

    return {"response": final_reply}
