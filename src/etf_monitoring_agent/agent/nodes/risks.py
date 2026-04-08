from etf_monitoring_agent.schemas.output import DetectedChange, RiskFlag
from etf_monitoring_agent.agent.state import AgentState


def classify_risks(detected_changes: list[DetectedChange]) -> list[RiskFlag]:
    """
    Classify ETF risk flags based on previously detected changes.
    """

    risk_flags = []

    for change in detected_changes:
        if change.change_type == "expense_ratio_increase":
            risk_flags.append(
                RiskFlag(
                    risk_type="cost_risk",
                    severity=change.severity,
                    confidence=0.8,
                )
            )
        
        elif change.change_type == "aum_decrease":
            risk_flags.append(
                RiskFlag(
                    risk_type="liquidity_risk",
                    severity=change.severity,
                    confidence=0.8,
                )
            )

        elif change.change_type == "top_holding":
            risk_flags.append(
                RiskFlag(
                    risk_type="concentration_risk",
                    severity=change.severity,
                    confidence=0.8,
                )
            )

    return risk_flags


def classify_risks_node(state: AgentState) -> dict:
    """
    LangGraph node that classifies ETF risk flags from detected changes
    and stores them in the agent state.
    """

    detected_changes = state.get("detected_changes", [])
    risk_flags = classify_risks(detected_changes)

    return {"risk_flags": risk_flags}