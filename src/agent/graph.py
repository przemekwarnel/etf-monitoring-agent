from langgraph.graph import StateGraph

from agent.state import AgentState
from agent.nodes.fetch import fetch_current_snapshot_node
from agent.nodes.history import load_previous_snapshot_node
from agent.nodes.changes import detect_changes_node
from agent.nodes.risks import classify_risks_node


def build_graph():
    """
    Build and compile the minimal LangGraph pipeline for ETF analysis.

    Current flow:
    fetch → previous → detect_changes → classify_risks
    """

    builder = StateGraph(AgentState)

    builder.add_node("fetch", fetch_current_snapshot_node)
    builder.add_node("previous", load_previous_snapshot_node)
    builder.add_node("detect_changes", detect_changes_node)
    builder.add_node("classify_risks", classify_risks_node)

    builder.set_entry_point("fetch")

    builder.add_edge("fetch", "previous")
    builder.add_edge("previous", "detect_changes")
    builder.add_edge("detect_changes", "classify_risks")

    return builder.compile()