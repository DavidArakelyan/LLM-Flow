from fastmcp import Client
client = Client("http://web_search_tool:7001")

async def fetch_search(state):
    res = await client.search_web(state['query'])
    state.setdefault('context', []).extend(res['results'])
    return state
