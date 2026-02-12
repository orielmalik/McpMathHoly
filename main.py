from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import Dict, List
from consts import model, allow, position
import Logger

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=allow, allow_methods=allow, allow_headers=allow)

active_sessions: Dict[str, OpenAI] = {}
chat_memory: Dict[str, List[dict]] = {}

class OpenRouterSchemaBody(BaseModel):
    api_key: str

class AskRequest(BaseModel):
    api_key: str
    category: str
    question: str

class ChatRequest(BaseModel):
    api_key: str
    message: str

@app.post("/connect")
async def connect(body: OpenRouterSchemaBody):
    Logger.printer("INFO", f"Attempting connection for API key: {body.api_key[:6]}***")
    if body.api_key in active_sessions:
        Logger.printer("INFO", f"API key already connected.")
        return {"status": "already_connected"}

    try:
        client = OpenAI(api_key=body.api_key, base_url="https://openrouter.ai/api/v1")
        completion = client.chat.completions.create(
            model=model,
            messages=[position]
        )
        active_sessions[body.api_key] = client
        chat_memory[body.api_key] = [
            {"role": "system", "content": "You are a mathematics expert. Only answer math questions. Format: Category: <category>. Question: <question>. Analyze and answer precisely."}
        ]
        Logger.printer("INFO", f"Connection successful for API key: {body.api_key[:6]}***")
        return {"status": "connected", "model_response": completion.choices[0].message.content}
    except Exception as e:
        Logger.printer("ERROR", f"Connection failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Connection failed")

@app.post("/ask")
async def ask_math(request: AskRequest):
    if request.api_key not in active_sessions:
        Logger.printer("ERROR", "Attempted ask without connection")
        raise HTTPException(status_code=403, detail="Not connected")

    client = active_sessions[request.api_key]
    message_content = f"Category: {request.category}. Question: {request.question}"

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a mathematics expert. Only answer math questions."},
                {"role": "user", "content": message_content}
            ]
        )
        Logger.printer("INFO", f"Ask request processed: {request.category}")
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        Logger.printer("ERROR", f"Ask request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Model request failed")

@app.post("/chat")
async def chat(request: ChatRequest):
    if request.api_key not in active_sessions:
        Logger.printer("ERROR", "Attempted chat without connection")
        raise HTTPException(status_code=403, detail="Not connected")

    client = active_sessions[request.api_key]
    memory = chat_memory[request.api_key]
    memory.append({"role": "user", "content": request.message})

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=memory
        )
        assistant_message = completion.choices[0].message.content
        memory.append({"role": "assistant", "content": assistant_message})
        Logger.printer("INFO", f"Chat message processed")
        return {"response": assistant_message}
    except Exception as e:
        Logger.printer("ERROR", f"Chat request failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Model request failed")

if __name__ == "__main__":
    import uvicorn
    Logger.printer("INFO", "Starting FastAPI backend...")
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)