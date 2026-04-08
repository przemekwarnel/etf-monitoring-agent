from etf_monitoring_agent.schemas.internal import ETFSnapshot
from etf_monitoring_agent.schemas.output import DetectedChange

from etf_monitoring_agent.agent.state import AgentState


def detect_changes(current: ETFSnapshot, previous: ETFSnapshot) -> list[DetectedChange]:
    """
    Detect material changes between two ETF snapshots.

    Currently supports:
    - expense ratio changes
    - AUM changes
    - individual top holding weight changes
    
    Returns a list of DetectedChange objects describing the detected differences.
    """

    changes = []

    # Expense ratio
    if current.expense_ratio is not None and previous.expense_ratio is not None:
        expense_ratio_change = current.expense_ratio - previous.expense_ratio
        if abs(expense_ratio_change) >= 0.001:
            if abs(expense_ratio_change) >= 0.005:
                severity = "high"
            elif abs(expense_ratio_change) >= 0.002:
                severity = "medium"
            else:                 
                severity = "low"
            
            if expense_ratio_change > 0:
                change_type = "expense_ratio_increase"
            else:
                change_type = "expense_ratio_decrease"
            
            description = (
                f"Expense ratio changed from {previous.expense_ratio:.2%} to {current.expense_ratio:.2%} " 
                f"({expense_ratio_change:.2%})."
            )
            changes.append(DetectedChange(change_type=change_type, severity=severity, description=description))
    
    # AUM
    if (
        current.aum is not None
        and previous.aum is not None
        and previous.aum != 0
    ):
        aum_change_pct = (current.aum - previous.aum) / previous.aum
        if abs(aum_change_pct) >= 0.2:
            if abs(aum_change_pct) >= 0.5:
                severity = "high"
            elif abs(aum_change_pct) >= 0.35:
                severity = "medium"
            else:
                severity = "low"
            
            if aum_change_pct > 0:
                change_type = "aum_increase"
            else:                
                change_type = "aum_decrease"
            
            description = (
                f"AUM changed from {previous.aum:.2f} to {current.aum:.2f} "
                f"({aum_change_pct:.1%})."
            )
            changes.append(DetectedChange(change_type=change_type, severity=severity, description=description))
    
    # Top holdings
    prev_holdings = {h.name: h.weight for h in previous.top_holdings}
    for holding in current.top_holdings:
        prev_weight = prev_holdings.get(holding.name)
        if prev_weight is not None:
            holding_weight_change = holding.weight - prev_weight
            if abs(holding_weight_change) >= 5.0:
                if abs(holding_weight_change) >= 10.0:
                    severity = "high"
                elif abs(holding_weight_change) >= 7.5:
                    severity = "medium"
                else:
                    severity = "low"
                description = f"Holding '{holding.name}' weight changed from {prev_weight:.2f}% to {holding.weight:.2f}%."
                changes.append(DetectedChange(change_type="top_holding", severity=severity, description=description))

    return changes


def detect_changes_node(state: AgentState) -> dict: 
    """
    LangGraph node that detects changes between current and previous ETF snapshots
    and stores them under 'detected_changes' in the agent state.
    """

    if "current_snapshot" not in state or "previous_snapshot" not in state:
        raise ValueError("State must contain current_snapshot and previous_snapshot")

    changes = detect_changes(state["current_snapshot"], state["previous_snapshot"])
    return {"detected_changes": changes}