from etf_monitoring_agent.schemas.internal import ETFSnapshot, ComparableETF
from etf_monitoring_agent.agent.state import AgentState


def find_dominant_etf(
    current: ETFSnapshot,
    comparables: list[ComparableETF],
) -> ComparableETF | None:
    """
    Identify if a more cost-efficient and sufficiently large ETF exists
    among comparable instruments.
    """
    
    if current.expense_ratio is None or current.aum is None:
        return None
    
    best_expense_ratio: float = current.expense_ratio
    dominant_etf: ComparableETF | None = None

    for comparable in comparables:
        if (
            comparable.expense_ratio is not None 
            and comparable.aum is not None
            and comparable.expense_ratio < best_expense_ratio
            and comparable.aum >= 0.5 * current.aum
        ):
            best_expense_ratio = comparable.expense_ratio
            dominant_etf = comparable
    
    return dominant_etf


def dominance_node(state: AgentState) -> dict:
    """
    LangGraph node that identifies a dominant ETF among comparables
    and stores it in the agent state.
    """

    if "current_snapshot" not in state or "comparable_etfs" not in state:
        raise ValueError("State must contain current_snapshot and comparable_etfs")

    current = state["current_snapshot"]
    comparables = state["comparable_etfs"]

    dominant_etf = find_dominant_etf(current, comparables)
    
    return {"dominant_etf": dominant_etf}
