from agent.state import AgentState
from tools.etf_data import fetch_etf_snapshot


def fetch_current_snapshot_node(state: AgentState) -> dict:
    """
    LangGraph node that fetches the current ETF snapshot using the ticker
    and stores it in the agent state.
    """

    if "ticker" not in state:
        raise ValueError("State must contain 'ticker'")

    current_snapshot = fetch_etf_snapshot(state["ticker"])
    return {"current_snapshot": current_snapshot}