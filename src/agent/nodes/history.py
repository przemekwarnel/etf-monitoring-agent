from copy import deepcopy

from agent.state import AgentState


def load_previous_snapshot_node(state: AgentState) -> AgentState:
    """
    LangGraph node that creates a temporary previous ETF snapshot for testing
    the pipeline before historical storage is implemented.
    """

    previous_snapshot = deepcopy(state["current_snapshot"])

    if previous_snapshot.aum is not None:
        previous_snapshot.aum *= 0.8  # Simulate a 20% decrease in AUM for testing
    
    state["previous_snapshot"] = previous_snapshot
    
    return state