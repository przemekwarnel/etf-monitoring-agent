from agent.state import AgentState
from schemas.output import ETFAnalysisOutput, DominantETF


def build_status_reason(state: AgentState, status: str) -> str:
    """Generate a human-readable explanation for the final ETF status."""

    if status == "review":
        status_reason = "A lower-cost alternative with sufficient scale was identified."
    elif status == "monitor":
        status_reason = "Potential risk signals were detected and may require attention."
    elif state.get("detected_changes"):
        status_reason = "Changes were detected, but they do not currently indicate elevated risk."
    else:
        status_reason = "No material changes or risk signals were detected."

    return status_reason


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
    
    dominant = state.get("dominant_etf")
    output_dominant = None

    if dominant is not None:
        output_dominant = DominantETF(
            ticker=dominant.ticker,
            fund_name=dominant.fund_name,
            expense_ratio=dominant.expense_ratio,
            aum=dominant.aum,
            currency=dominant.currency,
            replication_method=dominant.replication_method,
        )

    return ETFAnalysisOutput(
        ticker=state["ticker"],
        status=status,
        status_reason=build_status_reason(state, status),
        detected_changes=state.get("detected_changes", []),
        risk_flags=state.get("risk_flags", []),
        dominant_etf=output_dominant,
    )


def synthesize_output_node(state: AgentState) -> dict:
    """
    LangGraph node that synthesizes the final ETF analysis output
    and stores it in the agent state.
    """

    final_output = synthesize_output(state)
    return {"final_output": final_output}