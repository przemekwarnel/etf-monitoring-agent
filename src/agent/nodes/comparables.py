from agent.state import AgentState
from tools.comparables import find_comparable_etfs


def find_comparables_node(state: AgentState) -> dict:
    """
    LangGraph node that finds comparable ETFs for the current snapshot
    and stores them in the agent state.
    """

    current_snapshot = state.get("current_snapshot")
    if not current_snapshot:
        return {"comparable_etfs": []}

    comparable_etfs = find_comparable_etfs(current_snapshot)

    return {"comparable_etfs": comparable_etfs}