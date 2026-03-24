from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class ETFAnalysisInput(BaseModel):
    ticker: str = Field(..., description="ETF ticker symbol, e.g. VWCE, IWDA")
    lookback_days: int = Field(
        default=90,
        ge=1,
        le=365,
        description="Number of days to look back for change detection",
    )
    as_of_date: Optional[date] = Field(
        default=None,
        description="Optional reference date for analysis (defaults to today)",
    )