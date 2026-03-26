from langgraph.graph import StateGraph

from agent.nodes.changes import detect_changes_node
from agent.state import AgentState


def build_graph():
    """
    Build and compile the minimal LangGraph pipeline for ETF analysis.

    The current version contains a single node for change detection.
    """

    builder = StateGraph(AgentState)

    builder.add_node("detect_changes", detect_changes_node)

    builder.set_entry_point("detect_changes")

    graph = builder.compile()

    return graph