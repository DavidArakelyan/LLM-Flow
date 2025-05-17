from openai import AsyncOpenAI
from typing import Any
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def respond(inputs: dict[str, Any]) -> dict[str, Any]:
    if "query" in inputs:
        resp = await client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": inputs["query"]}]
        )
        inputs["answer"] = resp.choices[0].message.content
        return inputs
    else:
        message = inputs.get("message", "")
        return {"response": message}
