import logging
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any
from .nodes import simple_responder
from .nodes.node_logging import get_node_logger

logger = get_node_logger(__name__)


class SimpleGraphState(TypedDict):
    query: str
    response: str


def build_simple_graph():
    """Builds a simple workflow that just responds to queries directly."""
    logger.info("Building simple LangGraph workflow")

    # Initialize the graph with state schema
    g = StateGraph(state_schema=SimpleGraphState)

    # Add the simple responder node
    logger.info("Adding simple responder node")
    g.add_node("responder", simple_responder.respond)

    # Set it as entry point
    logger.info("Setting entry point")
    g.set_entry_point("responder")

    # Add edge to END
    logger.info("Adding terminal edge")
    g.add_edge("responder", END)

    # Compile the graph
    logger.info("Compiling graph")
    return g.compile()
