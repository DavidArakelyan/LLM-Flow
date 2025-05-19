from pathlib import Path
import re
import uuid
from app.core.config import get_model_config, get_system_prompt, openai_client
from app.core.nodes.node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)
client = openai_client


@log_node_calls
async def gen_code(state):
    logger.info(f"Starting code generation for query: {state['query']}")

    lang = "python"
    for key in ["c++", "cpp", ".cpp", "typescript", ".ts", "java", ".java"]:
        if key in state["query"].lower():
            lang = "cpp" if "c" in key else ("typescript" if "ts" in key else "java")
    ext = {"python": ".py", "cpp": ".cpp", "typescript": ".ts", "java": ".java"}[lang]
    prompt = f"Write a complete {lang} code file that {state['query']}"
    # Get code-specific model configuration
    model_config = get_model_config("code")
    resp = await client.chat.completions.create(
        model=model_config["model"],
        messages=[
            {"role": "system", "content": get_system_prompt("code")},
            {"role": "user", "content": prompt},
        ],
        temperature=model_config["temperature"],
        max_tokens=model_config["max_tokens"],
    )
    code = resp.choices[0].message.content
    fpath = Path(f"/mnt/data/{uuid.uuid4()}{ext}")
    fpath.write_text(code)
    state["generated_file"] = str(fpath)
    return state
