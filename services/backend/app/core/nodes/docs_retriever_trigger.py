from fastmcp import Client
from .node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)
client = Client("http://docs_retriever_tool:7002")


@log_node_calls
async def fetch_rag(state):
    # assumes tool returns list of passages
    res = await client.retrieve_docs(state["query"])
    state.setdefault("context", []).extend(res["passages"])
    return state
