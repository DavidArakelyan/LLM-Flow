from pathlib import Path
import uuid
from app.core.config import get_model_config, get_system_prompt, openai_client
from app.core.nodes.node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)
client = openai_client


@log_node_calls
async def gen_text(state):
    fmt = ".md" if "markdown" in state["query"].lower() else ".txt"
    prompt = f"{state['query']}"
    # Get text-specific model configuration
    model_config = get_model_config("text")
    resp = await client.chat.completions.create(
        model=model_config["model"],
        messages=[
            {"role": "system", "content": get_system_prompt("text")},
            {"role": "user", "content": prompt},
        ],
        temperature=model_config["temperature"],
        max_tokens=model_config["max_tokens"],
    )
    text = resp.choices[0].message.content
    fpath = Path(f"/mnt/data/{uuid.uuid4()}{fmt}")
    fpath.write_text(text)
    state["generated_file"] = str(fpath)
    return state
