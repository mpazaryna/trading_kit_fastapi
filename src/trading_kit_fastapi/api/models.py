# src/trading_kit_fastapi/api/models.py
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class StockData(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    dates: List[str] = Field(..., description="List of dates in YYYY-MM-DD format")
    prices: List[float] = Field(
        ..., description="List of closing prices corresponding to the dates"
    )
    short_window: int = Field(10, description="Short-term WMA window size")
    long_window: int = Field(30, description="Long-term WMA window size")
    precision: int = Field(2, description="Decimal precision for calculations")


class AnalysisResult(BaseModel):
    company_name: str
    short_wma: Dict[str, Optional[float]]
    long_wma: Dict[str, Optional[float]]
    signals: Dict[str, Optional[int]]
    summary: Dict[str, int]
