try:
    from typing import TypedDict, NotRequired  # type: ignore
except ImportError:
    from typing import TypedDict
    from typing_extensions import NotRequired
    
from schemas.internal import ETFSnapshot
from schemas.output import DetectedChange


class AgentState(TypedDict):
    """
    Typed state object passed between LangGraph nodes in the ETF analysis pipeline.
    """
    
    current_snapshot: ETFSnapshot
    previous_snapshot: ETFSnapshot
    detected_changes: NotRequired[list[DetectedChange]]