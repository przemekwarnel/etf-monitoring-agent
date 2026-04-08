from typing import List, Literal

from pydantic import BaseModel, Field


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


# --- Comparable analysis ---

class ComparableETF(BaseModel):
    ticker: str
    dominance: bool
    dominance_reasons: List[str]
    tradeoffs: List[str]


class ComparableAnalysis(BaseModel):
    found_comparables: bool
    alternatives: List[ComparableETF]


# --- Final output ---

class ETFAnalysisOutput(BaseModel):
    ticker: str
    status: Literal["stable", "monitor", "review"]

    detected_changes: List[DetectedChange]
    risk_flags: List[RiskFlag]

    comparable_analysis: ComparableAnalysis