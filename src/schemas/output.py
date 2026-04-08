from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from schemas.internal import ComparableETF


# --- Risk flags ---

class RiskFlag(BaseModel):
    risk_type: Literal[
        "concentration_risk",
        "cost_risk",
        "liquidity_risk",
        "structure_risk",
    ]
    severity: Literal["low", "medium", "high"]
    confidence: float = Field(..., ge=0.0, le=1.0)


# --- Detected changes ---

class DetectedChange(BaseModel):
    change_type: str
    severity: Literal["low", "medium", "high"]
    description: str


# --- Final output ---

class ETFAnalysisOutput(BaseModel):
    ticker: str
    status: Literal["stable", "monitor", "review"]

    detected_changes: List[DetectedChange]
    risk_flags: List[RiskFlag]

    dominant_etf: Optional[ComparableETF] = None