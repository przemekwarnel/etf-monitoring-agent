from agent.state import AgentState
from schemas.output import ETFAnalysisOutput


def synthesize_output(state: AgentState) -> ETFAnalysisOutput:
    """
    Build the final structured ETF analysis output from the current agent state.
    """
    
    if state.get("dominant_etf") is not None:
        status = "review"
    elif state.get("risk_flags"):
        status = "monitor"
    else:
        status = "stable"

    return ETFAnalysisOutput(
        ticker=state["ticker"],
        status=status,
        detected_changes=state.get("detected_changes", []),
        risk_flags=state.get("risk_flags", []),
        dominant_etf=state.get("dominant_etf"),
    )


def synthesize_output_node(state: AgentState) -> dict:
    """
    LangGraph node that synthesizes the final ETF analysis output
    and stores it in the agent state.
    """

    final_output = synthesize_output(state)
    return {"final_output": final_output}