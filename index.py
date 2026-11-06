
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

from chatbot import ask_chatbot


# --------------------------------
# FastAPI Application
# --------------------------------

app = FastAPI(
    title="Cyberathon RAG Chatbot",
    description="AI-powered Cyberathon information chatbot",
    version="1.0"
)


# --------------------------------
# Request Model
# --------------------------------


class QuestionRequest(BaseModel):

    question: str

    chat_history: List[Dict[str, str]] = Field(
        default_factory=list
    )


# --------------------------------
# Home API
# --------------------------------

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Cyberathon RAG Chatbot API is running"
    }


# --------------------------------
# Chat API
# --------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        answer = ask_chatbot(
            question,
            request.chat_history
        )

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
