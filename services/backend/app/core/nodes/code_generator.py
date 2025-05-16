from openai import AsyncOpenAI
from pathlib import Path
import re, uuid
client = AsyncOpenAI()

async def gen_code(state):
    lang = 'python'
    for key in ['c++', 'cpp', '.cpp', 'typescript', '.ts', 'java', '.java']:
        if key in state['query'].lower():
            lang = 'cpp' if 'c' in key else ('typescript' if 'ts' in key else 'java')
    ext = {'python': '.py', 'cpp': '.cpp', 'typescript': '.ts', 'java': '.java'}[lang]
    prompt = f"Write a complete {lang} code file that {state['query']}"
    resp = await client.chat.completions.create(
        model="claude-3-opus-20240229",
        messages=[{"role": "user", "content": prompt}] )
    code = resp.choices[0].message.content
    fpath = Path(f"/mnt/data/{uuid.uuid4()}{ext}")
    fpath.write_text(code)
    state['generated_file'] = str(fpath)
    return state
