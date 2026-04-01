from agent.state import AgentState
from schemas.output import ETFAnalysisOutput, ComparableAnalysis


def synthesize_output(state: AgentState) -> ETFAnalysisOutput:
    """
    Build the final structured ETF analysis output from the current agent state.
    """
    
    # Status logic
    if state.get("dominant_etf") is not None:
        status = "review"
    elif state.get("risk_flags"):
        status = "monitor"
    else:
        status = "stable"
    
    # Comparable analysis
    comparable_etfs = state.get("comparable_etfs", [])

    comparable_analysis = ComparableAnalysis(
        found_comparables = len(comparable_etfs) > 0,
        alternatives=[],
    )

    return ETFAnalysisOutput(
        ticker=state["ticker"],
        status=status,
        detected_changes=state.get("detected_changes", []),
        risk_flags=state.get("risk_flags", []),
        comparable_analysis=comparable_analysis,
    )


def synthesize_output_node(state: AgentState) -> dict:
    """
    LangGraph node that synthesizes the final ETF analysis output
    and stores it in the agent state.
    """

    final_output = synthesize_output(state)
    return {"final_output": final_output}