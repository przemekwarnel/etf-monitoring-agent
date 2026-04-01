try:
    from typing import TypedDict, NotRequired  # type: ignore
except ImportError:
    from typing import TypedDict
    from typing_extensions import NotRequired
    
from schemas.internal import ETFSnapshot, ComparableETF
from schemas.output import DetectedChange, RiskFlag, ETFAnalysisOutput


class AgentState(TypedDict):
    """
    Typed state object passed between LangGraph nodes in the ETF analysis pipeline.
    """

    ticker: str
    current_snapshot: NotRequired[ETFSnapshot]
    previous_snapshot: NotRequired[ETFSnapshot]
    detected_changes: NotRequired[list[DetectedChange]]
    risk_flags: NotRequired[list[RiskFlag]]
    comparable_etfs: NotRequired[list[ComparableETF]]
    dominant_etf: NotRequired[ComparableETF]
    final_output: NotRequired[ETFAnalysisOutput]