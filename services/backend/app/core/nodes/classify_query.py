"""Classify the query into simple / needs web search / needs doc / wants_code / wants_text."""

from .node_logging import log_node_calls, get_node_logger

logger = get_node_logger(__name__)


@log_node_calls
def classify(state):
    logger.info("Starting query classification")
    q = state["query"]
    lower = q.lower()
    state["is_simple"] = len(q.split()) < 20 and not any(
        k in lower for k in ["generate", "create", "write", "code", "document", "pdf"]
    )
    state["needs_web_search"] = (
        "latest" in lower or "current" in lower or "today" in lower
    )
    state["needs_doc"] = "attached" in lower or "document" in lower
    state["wants_code"] = any(
        ext in lower
        for ext in [
            ".cpp",
            ".py",
            ".java",
            ".ts",
            "c++",
            "python",
            "typescript",
            "java",
        ]
    )
    state["wants_text"] = not state["wants_code"]
    return state
