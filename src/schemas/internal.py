from pydantic import BaseModel, Field
from typing import List, Optional


class Holding(BaseModel):
    name: str
    weight: float = Field(..., ge=0.0, le=100.0)


class AllocationItem(BaseModel):
    name: str
    weight: float = Field(..., ge=0.0, le=100.0)


class ETFSnapshot(BaseModel):
    ticker: str
    fund_name: Optional[str] = None
    issuer: Optional[str] = None
    expense_ratio: Optional[float] = Field(default=None, ge=0.0)
    aum: Optional[float] = Field(default=None, ge=0.0)
    currency: Optional[str] = None
    replication_method: Optional[str] = None

    top_holdings: List[Holding] = []
    sector_allocation: List[AllocationItem] = []
    country_allocation: List[AllocationItem] = []
    price: Optional[float] = None