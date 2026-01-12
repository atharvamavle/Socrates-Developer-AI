from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
from dotenv import load_dotenv

from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

import re

# ===== Env & clients =====
load_dotenv()  # loads OPENAI_API_KEY from .env if present

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://socrates-developer-ai.vercel.app",
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


# ===== Simple NLP helpers (tokenization + lemmatization) =====
def simple_sent_tokenize(text: str) -> list[str]:
    """Naive sentence tokenizer based on punctuation."""
    sentences = re.split(r"[.!?]+", text)
    return [s.strip() for s in sentences if s.strip()]


def simple_word_tokenize(text: str) -> list[str]:
    """Naive word tokenizer: split on whitespace and strip edge punctuation."""
    tokens = []
    for raw in text.split():
        token = re.sub(r"^[^\w]+|[^\w]+$", "", raw)
        if token:
            tokens.append(token)
    return tokens


def simple_lemmatize(word: str) -> str:
    """Very lightweight lemmatizer for English nouns/verbs."""
    w = word.lower()
    # plural -> singular
    if len(w) > 3 and w.endswith("ies"):
        return w[:-3] + "y"        # studies -> study
    if len(w) > 3 and w.endswith("es"):
        return w[:-2]              # uses -> us (approx)
    if len(w) > 2 and w.endswith("s"):
        return w[:-1]              # plants -> plant
    return w


# ===== NLP preprocessing =====
def preprocess_text(text: str) -> dict:
    sentences = simple_sent_tokenize(text)
    words = simple_word_tokenize(text)
    lemmas = [simple_lemmatize(w) for w in words]

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
            model="gpt-4.1-mini",
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
