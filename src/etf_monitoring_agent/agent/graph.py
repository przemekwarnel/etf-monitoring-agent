from langgraph.graph import StateGraph

from etf_monitoring_agent.agent.state import AgentState
from etf_monitoring_agent.agent.nodes.fetch import fetch_current_snapshot_node
from etf_monitoring_agent.agent.nodes.history import load_previous_snapshot_node
from etf_monitoring_agent.agent.nodes.changes import detect_changes_node
from etf_monitoring_agent.agent.nodes.risks import classify_risks_node
from etf_monitoring_agent.agent.nodes.comparables import find_comparables_node
from etf_monitoring_agent.agent.nodes.dominance import dominance_node
from etf_monitoring_agent.agent.nodes.synthesize import synthesize_output_node


def build_graph():
    """
    Build and compile the minimal LangGraph pipeline for ETF analysis.

    Current flow:
    fetch → previous → detect_changes → classify_risks → find_comparables → dominance → synthesize
    """

    builder = StateGraph(AgentState)

    builder.add_node("fetch", fetch_current_snapshot_node)
    builder.add_node("previous", load_previous_snapshot_node)
    builder.add_node("detect_changes", detect_changes_node)
    builder.add_node("classify_risks", classify_risks_node)
    builder.add_node("find_comparables", find_comparables_node)
    builder.add_node("dominance", dominance_node)
    builder.add_node("synthesize", synthesize_output_node)

    builder.set_entry_point("fetch")

    builder.add_edge("fetch", "previous")
    builder.add_edge("previous", "detect_changes")
    builder.add_edge("detect_changes", "classify_risks")
    builder.add_edge("classify_risks", "find_comparables")
    builder.add_edge("find_comparables", "dominance")
    builder.add_edge("dominance", "synthesize")

    return builder.compile()