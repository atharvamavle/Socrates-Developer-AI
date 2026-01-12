from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
from dotenv import load_dotenv

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# ===== Env & clients =====
load_dotenv()  # loads OPENAI_API_KEY from .env if present

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

nltk.download("punkt")
nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Pydantic models =====
class DialogueRequest(BaseModel):
    user_input: str
    conversation_history: list[dict] = []  # role/content pairs


class DialogueResponse(BaseModel):
    socratic_response: str
    processed_input: str
    tokens_used: int


# ===== NLP preprocessing =====
def preprocess_text(text: str) -> dict:
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    lemmas = [lemmatizer.lemmatize(w.lower()) for w in words]

    return {
        "sentence_count": len(sentences),
        "word_count": len(words),
        "lemmas": lemmas,
    }


# ===== GPT call =====
def generate_socratic_response(user_input: str, history: list[dict]) -> tuple[str, int]:
    try:
        system_prompt = (
            "You are a Socratic tutor. "
            "Ask probing questions instead of giving direct answers, "
            "and keep replies to 2–3 sentences."
        )

        messages = [{"role": "system", "content": system_prompt}]

        for msg in history[-5:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_input})

        resp = client.chat.completions.create(
            model="gpt-4.1-mini",  # or gpt-4o-mini / gpt-4o depending on your plan
            messages=messages,
            max_tokens=256,
        )

        text = resp.choices[0].message.content
        tokens_used = resp.usage.total_tokens

        return text, tokens_used

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")


# ===== Endpoint =====
@app.post("/dialogue", response_model=DialogueResponse)
async def dialogue(body: DialogueRequest):
    processed = preprocess_text(body.user_input)

    processed_summary = (
        f"{processed['word_count']} words, "
        f"{processed['sentence_count']} sentences"
    )

    socratic_text, tokens = generate_socratic_response(
        body.user_input,
        body.conversation_history,
    )

    return DialogueResponse(
        socratic_response=socratic_text,
        processed_input=processed_summary,
        tokens_used=tokens,
    )

