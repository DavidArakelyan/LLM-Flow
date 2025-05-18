from fastmcp import Client
from .node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)
client = Client("http://web_search_tool:7001")


@log_node_calls
async def fetch_search(state):
    res = await client.search_web(state["query"])
    state.setdefault("context", []).extend(res["results"])
    return state
