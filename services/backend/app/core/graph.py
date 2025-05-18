import logging
import asyncio
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Callable
from .nodes import (
    classify_query,
    simple_responder,
    web_search_trigger,
    docs_retriever_trigger,
    code_generator,
    text_generator,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GraphState(TypedDict):
    query: str
    response: str
    context: dict


def log_state_wrapper(node_name: str, node_func: Callable) -> Callable:
    """Wrapper to log state before and after node execution."""

    async def wrapped(state: dict[str, Any]) -> dict[str, Any]:
        logger.debug(f"\n{'=' * 50}")
        logger.debug(f"Entering node: {node_name}")
        logger.debug(f"Input state: {state}")

        # Handle both async and sync functions
        if asyncio.iscoroutinefunction(node_func):
            result = await node_func(state)
        else:
            result = node_func(state)

        logger.debug(f"Node {node_name} completed")
        logger.debug(f"Output state: {result}")
        logger.debug(f"{'=' * 50}\n")
        return result

    return wrapped


def log_condition(name: str, condition_func: Callable) -> Callable:
    """Wrapper to log conditional transitions."""

    def wrapped(state: dict[str, Any]) -> bool:
        result = condition_func(state)
        logger.debug(f"Condition check for transition to {name}: {result}")
        logger.debug(f"Current state for condition: {state}")
        return result

    return wrapped


def visualize_graph(g: StateGraph) -> str:
    """Generate a Mermaid graph visualization of the LangGraph structure."""
    logger.info("Generating Mermaid graph visualization")

    # Start Mermaid graph definition
    mermaid = ["graph TD"]

    # Add nodes with styling
    seen_nodes = set()

    def add_node(node_name: str):
        if node_name == "END":
            style = "[/END\\]"
        elif node_name == "classifier":
            style = "[Classifier{<br/>Entry Point}]"
        else:
            style = "[" + node_name + "]"

        if node_name not in seen_nodes:
            mermaid.append(f"    {node_name}{style}")
            seen_nodes.add(node_name)

    # Process all branches
    for source, destinations in g.branches.items():
        add_node(source)
        for dest in destinations:
            add_node(dest)
            edge_style = " -->"
            # Check for conditional transitions
            if source == "classifier":
                if dest == "simple_responder":
                    edge_style = " -->|is_simple|"
                elif dest == "web_search":
                    edge_style = " -->|needs_web_search|"
                elif dest == "docs_rag":
                    edge_style = " -->|needs_doc|"
            elif source in ["docs_rag", "web_search"]:
                if dest == "code_gen":
                    edge_style = " -->|wants_code|"
                elif dest == "text_gen":
                    edge_style = " -->|wants_text|"
            mermaid.append(f"    {source}{edge_style} {dest}")

    logger.debug("Generated Mermaid graph:\n" + "\n".join(mermaid))
    return "\n".join(mermaid)


def dump_graph_visualization(g: StateGraph, output_path: str = "graph.mmd"):
    """Dump the graph visualization to a file."""
    mermaid = visualize_graph(g)
    with open(output_path, "w") as f:
        f.write(mermaid)
    logger.info(f"Graph visualization saved to {output_path}")
    return output_path


def build_graph():
    logger.info("Building LangGraph workflow")
    g = StateGraph(state_schema=GraphState)

    # Add nodes with logging wrappers
    logger.info("Adding nodes to graph...")
    g.add_node("classifier", log_state_wrapper("classifier", classify_query.classify))
    g.add_node(
        "simple_responder",
        log_state_wrapper("simple_responder", simple_responder.respond),
    )
    g.add_node(
        "web_search", log_state_wrapper("web_search", web_search_trigger.fetch_search)
    )
    g.add_node(
        "docs_rag", log_state_wrapper("docs_rag", docs_retriever_trigger.fetch_rag)
    )
    g.add_node("code_gen", log_state_wrapper("code_gen", code_generator.gen_code))
    g.add_node("text_gen", log_state_wrapper("text_gen", text_generator.gen_text))

    # Set entry point
    logger.info("Setting classifier as entry point")
    g.set_entry_point("classifier")

    # Add conditional edges with logging
    logger.info("Adding conditional edges from classifier")
    g.add_conditional_edges(
        "classifier",
        {
            "simple_responder": log_condition(
                "simple_responder",
                lambda x: x.get(
                    "is_simple", True
                ),  # Changed default to True for testing
            ),
            "web_search": log_condition(
                "web_search", lambda x: x.get("needs_web_search", False)
            ),
            "docs_rag": log_condition("docs_rag", lambda x: x.get("needs_doc", False)),
        },
    )

    logger.info("Adding conditional edges from docs_rag")
    g.add_conditional_edges(
        "docs_rag",
        {
            "code_gen": log_condition(
                "code_gen_from_docs", lambda x: x.get("wants_code", False)
            ),
            "text_gen": log_condition(
                "text_gen_from_docs", lambda x: x.get("wants_text", False)
            ),
        },
    )

    logger.info("Adding conditional edges from web_search")
    g.add_conditional_edges(
        "web_search",
        {
            "code_gen": log_condition(
                "code_gen_from_web", lambda x: x.get("wants_code", False)
            ),
            "text_gen": log_condition(
                "text_gen_from_web", lambda x: x.get("wants_text", False)
            ),
        },
    )

    # Add terminal edges with state propagation
    logger.info("Adding terminal edges")

    def end_handler(state):
        """Ensure state is propagated to the end"""
        logger.debug(f"Final state at END: {state}")
        return state

    g.add_node("end", end_handler)
    g.add_edge("simple_responder", "end")
    g.add_edge("code_gen", "end")
    g.add_edge("text_gen", "end")
    g.add_edge("end", END)

    logger.info("Compiling graph")
    compiled_graph = g.compile()
    logger.info("Graph compilation completed successfully")

    # Generate and save visualization
    # dump_graph_visualization(g, "workflow_graph.mmd")

    return compiled_graph
