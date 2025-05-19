from typing import Any, List, Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI
from .node_logging import log_node_calls, get_node_logger

# Initialize logger first
logger = get_node_logger(__name__)

# Try to load environment from workspace root
workspace_env = Path(__file__).resolve().parents[5] / ".env"
logger.debug(f"Looking for .env at: {workspace_env}")
if workspace_env.exists():
    logger.info(f"Loading environment from {workspace_env}")
    load_dotenv(dotenv_path=workspace_env, verbose=True, override=True)
else:
    logger.warning(f"No .env file found at {workspace_env}")


def get_openai_client() -> Optional[AsyncOpenAI]:
    """Initialize OpenAI client with proper error handling."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return None
    if not api_key.startswith("sk-"):
        logger.error("OPENAI_API_KEY appears to be invalid (should start with 'sk-')")
        return None
    return AsyncOpenAI(api_key=api_key)


client = get_openai_client()

SYSTEM_PROMPT = """You are a helpful AI assistant. Be concise and direct in your responses.
Focus on providing accurate and relevant information."""


def prepare_messages(query: str, history: List[str] = None) -> List[dict]:
    """Prepare the message list for the OpenAI API call."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add history messages if available
    if history:
        for msg in history:
            messages.append({"role": "user", "content": msg})

    # Add the current query
    messages.append({"role": "user", "content": query})
    return messages


@log_node_calls
async def respond(inputs: dict[str, Any]) -> dict[str, Any]:
    try:
        if not client:
            error_msg = "OpenAI client not properly initialized. Check OPENAI_API_KEY environment variable."
            logger.error(error_msg)
            return {"response": error_msg}

        if "query" not in inputs:
            logger.warning("No query found in inputs")
            return {"response": inputs.get("message", "No message provided")}

        messages = prepare_messages(
            query=inputs["query"], history=inputs.get("history", [])
        )

        logger.debug(f"Sending request with {len(messages)} messages")
        try:
            response = ""
            async for chunk in await client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=2000,
            ):
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content

            inputs["response"] = response
            logger.debug(f"Returning state from responder: {inputs}")
            return inputs
        except Exception as api_error:
            error_msg = f"OpenAI API error: {str(api_error)}"
            logger.error(error_msg)
            return {"response": error_msg}

    except Exception as e:
        logger.error(f"Error in simple responder: {str(e)}", exc_info=True)
        return {"response": f"An error occurred: {str(e)}"}
