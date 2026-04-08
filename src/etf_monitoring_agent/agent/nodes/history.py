from copy import deepcopy

from etf_monitoring_agent.agent.state import AgentState


def load_previous_snapshot_node(state: AgentState) -> dict:
    """
    LangGraph node that creates a temporary previous ETF snapshot for testing
    the pipeline before historical storage is implemented.
    """

    if "current_snapshot" not in state:
        raise ValueError("State must contain 'current_snapshot'")
    
    previous_snapshot = deepcopy(state["current_snapshot"])

    if previous_snapshot.aum is not None:
        previous_snapshot.aum *= 0.8  
    
    return {"previous_snapshot": previous_snapshot}