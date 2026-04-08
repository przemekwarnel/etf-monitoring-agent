from agent.state import AgentState
from schemas.output import ETFAnalysisOutput, DominantETF


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