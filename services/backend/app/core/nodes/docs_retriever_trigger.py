from fastmcp import Client
client = Client("http://docs_retriever_tool:7002")

async def fetch_rag(state):
    # assumes tool returns list of passages
    res = await client.retrieve_docs(state['query'])
    state.setdefault('context', []).extend(res['passages'])
    return state
