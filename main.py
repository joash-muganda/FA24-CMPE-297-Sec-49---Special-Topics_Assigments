import asyncio
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import openai
import tiktoken
from dotenv import load_dotenv
import json  # Correct import for JSON parsing
import httpx

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize tiktoken encoder
encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")

class ChatInput(BaseModel):
    message: str
    conversation_history: list

@app.post("/chat")
async def chat(chat_input: ChatInput):
    try:
        # Prepare the messages for the API call
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend(chat_input.conversation_history)
        messages.append({"role": "user", "content": chat_input.message})

        # Log the prepared messages
        print("Sending messages to OpenAI:", messages)  # Debugging line

        # Count tokens in the conversation
        token_count = sum(len(encoder.encode(msg["content"])) for msg in messages)

        # If token count exceeds 4000, trim the conversation history
        while token_count > 4000:
            removed_message = messages.pop(1)  # Remove the oldest message after the system message
            token_count -= len(encoder.encode(removed_message["content"]))
        
        print("Token count after trimming:", token_count)  # Debugging line

        # Create a generator for streaming the response
        async def generate_response():
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "stream": True
                    }
                ) as response:
                    print("OpenAI API response status:", response.status_code)  # Debugging line
                    if response.status_code != 200:
                        print("Error from OpenAI API:", await response.aread())  # Debugging line
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.strip() == "[DONE]":
                                break
                            try:
                                print("Received data chunk from OpenAI:", data)  # Debugging line
                                chunk = json.loads(data)  # Correct JSON parsing
                                content = chunk['choices'][0]['delta'].get('content', '')
                                if content:
                                    print("Streaming content:", content)  # Debugging line
                                    yield content
                            except Exception as e:
                                print("Error parsing chunk:", e)  # Debugging line
                                pass

        return StreamingResponse(generate_response(), media_type="text/event-stream")

    except Exception as e:
        print("Error in chat endpoint:", e)  # Debugging line
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define templates directory
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
