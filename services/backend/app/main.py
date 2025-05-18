import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from .core.graph import build_graph

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Augmented‑LLM Router")


class Message(BaseModel):
    id: str
    content: str
    history: list[str] = []


workflow = build_graph()


@app.post("/chat")
async def chat(msg: Message):
    logger.info(f"Received chat request with id: {msg.id}")
    logger.debug(f"Message content: {msg.content}")
    logger.debug(f"History length: {len(msg.history)}")

    state = {"query": msg.content, "history": msg.history}
    try:
        logger.info("Invoking workflow")
        result = await workflow.ainvoke(state)
        logger.info("Workflow completed successfully")
        logger.debug(f"Workflow result: {result}")

        # Return the answer or response from the workflow
        if "answer" in result:
            response = {"response": result["answer"]}
            logger.info("Sending answer response")
        elif "response" in result:
            response = {"response": result["response"]}
            logger.info("Sending direct response")
        else:
            response = {"response": "No response generated"}
            logger.warning("No response or answer found in result")

        logger.debug(f"Final response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(500, str(e))


@app.get("/health")
async def health_check():
    return {"status": "ok"}
