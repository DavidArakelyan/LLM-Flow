from typing import Any, List
from app.core.config import get_model_config, get_system_prompt, openai_client
from app.core.nodes.node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)

# Use common configuration
client = openai_client


def prepare_messages(query: str, history: List[str] = None) -> List[dict]:
    """Prepare the message list for the OpenAI API call."""
    messages = [{"role": "system", "content": get_system_prompt("chat")}]

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
            # Get chat-specific model configuration
            model_config = get_model_config("chat")
            async for chunk in await client.chat.completions.create(
                model=model_config["model"],
                messages=messages,
                stream=True,
                temperature=model_config["temperature"],
                max_tokens=model_config["max_tokens"],
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
