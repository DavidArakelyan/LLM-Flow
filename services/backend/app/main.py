from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from .core.graph import build_graph

app = FastAPI(title="Augmented‑LLM Router")

class Message(BaseModel):
    id: str
    content: str
    history: list[str] = []

workflow = build_graph()

@app.post("/chat")
async def chat(msg: Message):
    state = {"query": msg.content, "history": msg.history}
    try:
        result = await workflow.ainvoke(state)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))
