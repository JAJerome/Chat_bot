# This file will send messages to LLaMA and get replies back.

import httpx      
import os        
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Load our secret API key from .env
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Groq’s API URL and LLaMA model name
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192" # this model is best for this usecase mam


async def get_llama_response(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful chatbot to help the user based on their questions."},
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(API_URL, headers=headers, json=body)
        data = res.json()

        #  the chatbot  reply text
        return data["choices"][0]["message"]["content"].strip()




# now im using single file this chatbot 

# Start FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# This is the endpoint: it listens to POST requests at /chat
@app.post("/simple chatbot", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # this Takes user's message, send to LLaMA, return LLaMA's reply
    reply = await get_llama_response(request.message)
    return ChatResponse(reply=reply)
