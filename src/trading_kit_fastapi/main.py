from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from trading_kit.strategies.analyze_stock_trends import analyze_stock_trends

app = FastAPI()


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


def nan_to_none(value):
    if isinstance(value, float) and np.isnan(value):
        return None
    return value


@app.post("/analyze_stock_trends", response_model=AnalysisResult)
async def analyze_stock_trends_endpoint(stock_data: StockData):
    try:
        # Convert input data to pandas Series
        prices = pd.Series(
            stock_data.prices, index=pd.to_datetime(stock_data.dates), name="Close"
        )

        # Perform trend analysis
        short_wma, long_wma, signals = analyze_stock_trends(
            prices,
            short_window=stock_data.short_window,
            long_window=stock_data.long_window,
            precision=stock_data.precision,
        )

        # Convert results to dictionaries, handling NaN values
        short_wma_dict = {
            date.strftime("%Y-%m-%d"): nan_to_none(value)
            for date, value in short_wma.items()
        }
        long_wma_dict = {
            date.strftime("%Y-%m-%d"): nan_to_none(value)
            for date, value in long_wma.items()
        }
        signals_dict = {
            date.strftime("%Y-%m-%d"): nan_to_none(
                int(value) if not np.isnan(value) else None
            )
            for date, value in signals.items()
        }

        # Calculate summary of non-NaN signals
        signal_summary = signals.dropna().astype(int).value_counts().to_dict()
        signal_summary = {str(k): int(v) for k, v in signal_summary.items()}

        # Prepare and return the response
        return AnalysisResult(
            company_name=stock_data.company_name,
            short_wma=short_wma_dict,
            long_wma=long_wma_dict,
            signals=signals_dict,
            summary=signal_summary,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Trend Analysis API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
