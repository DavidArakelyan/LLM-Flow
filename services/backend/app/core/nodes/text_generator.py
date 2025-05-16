from openai import AsyncOpenAI
from pathlib import Path
import uuid
client = AsyncOpenAI()

async def gen_text(state):
    fmt = '.md' if 'markdown' in state['query'].lower() else '.txt'
    prompt = f"{state['query']}"
    resp = await client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}])
    text = resp.choices[0].message.content
    fpath = Path(f"/mnt/data/{uuid.uuid4()}{fmt}")
    fpath.write_text(text)
    state['generated_file'] = str(fpath)
    return state
