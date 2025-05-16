from langgraph.graph import StateGraph, END
from typing import TypedDict
from .nodes import (
    classify_query,
    simple_responder,
    web_search_trigger,
    docs_retriever_trigger,
    code_generator,
    text_generator,
)


class GraphState(TypedDict):
    query: str
    response: str
    context: dict


def build_graph():
    # Define state schema for the graph
    g = StateGraph(state_schema=GraphState)

    # Add nodes first
    g.add_node("classifier", classify_query.classify)
    g.add_node("simple_responder", simple_responder.respond)
    g.add_node("web_search", web_search_trigger.fetch_search)
    g.add_node("docs_rag", docs_retriever_trigger.fetch_rag)
    g.add_node("code_gen", code_generator.gen_code)
    g.add_node("text_gen", text_generator.gen_text)

    # Set entry point
    g.set_entry_point("classifier")

    # Add conditional edges with functions
    g.add_conditional_edges(
        "classifier",
        {
            "simple_responder": lambda x: x.get("is_simple", False),
            "web_search": lambda x: x.get("needs_web_search", False),
            "docs_rag": lambda x: x.get("needs_doc", False),
        },
    )

    # Add conditional edges from processing nodes to generators
    g.add_conditional_edges(
        "docs_rag",
        {
            "code_gen": lambda x: x.get("wants_code", False),
            "text_gen": lambda x: x.get("wants_text", False),
        },
    )

    g.add_conditional_edges(
        "web_search",
        {
            "code_gen": lambda x: x.get("wants_code", False),
            "text_gen": lambda x: x.get("wants_text", False),
        },
    )

    g.add_edge("simple_responder", END)
    g.add_edge("code_gen", END)
    g.add_edge("text_gen", END)

    return g.compile()
