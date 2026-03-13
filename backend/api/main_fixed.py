from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../backend/.env')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy load
search_fn = None
answer_fn = None

def load_modules():
    global search_fn, answer_fn
    if search_fn is None:
        from rag.pipeline import search
        from llm.groq_client_fixed import generate_answer
        search_fn = search
        answer_fn = generate_answer
        print("Modules loaded successfully")

class ChatMessage(BaseModel):
    user: str
    assistant: str

class Question(BaseModel):
    question: str
    history: Optional[List[ChatMessage]] = None

@app.post("/ask")
def ask(q: Question):
    try:
        load_modules()
        chunks = search_fn(q.question, top_k=5)
        history_list = [{"user": h.user, "assistant": h.assistant} for h in (q.history or [])]
        result = answer_fn(q.question, chunks, chat_history=history_list)
        return result
    except Exception as e:
        print(f"API Error: {e}")
        return {
            "answer": f"Sorry, there was an error processing your request. Error details: {str(e)}. Please try asking about BIS certification or standards.",
            "sources": []
        }

@app.get("/")
def root():
    return {"status": "BIS Chatbot API running"}

@app.get("/health")
def health():
    return {"health": "ok"}

