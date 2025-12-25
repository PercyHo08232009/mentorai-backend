from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import generate_response
from classifier import is_supported_question

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    if not is_supported_question(req.message):
        return {
            "response": "⚠️ This question is not supported. MentorAI only helps with learning-related questions."
        }

    if req.session_id not in sessions:
        sessions[req.session_id] = []

   
    sessions[req.session_id].append({
        "role": "user",
        "content": req.message
    })

    
    sessions[req.session_id] = sessions[req.session_id][-6:]

    
    ai_response = generate_response(sessions[req.session_id])

   
    lines = ai_response.split("\n")
    unique_lines = []
    seen = set()
    for line in lines:
        stripped = line.strip()
        if stripped and stripped not in seen:
            unique_lines.append(stripped)
            seen.add(stripped)
    ai_response = "\n".join(unique_lines)

    
    sessions[req.session_id].append({
        "role": "assistant",
        "content": ai_response
    })

    return {"response": ai_response}
