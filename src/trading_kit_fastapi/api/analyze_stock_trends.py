"""
This module defines the FastAPI route for analyzing stock trends. It includes
a POST endpoint that accepts stock data, performs trend analysis using the
analyze_stock_trends function from the trading_kit library, and returns the
results in a structured format.

Dependencies:
- FastAPI for creating the API route.
- Pydantic for input validation and response schemas.
- Pandas and NumPy for data manipulation.
- trading_kit for the stock trend analysis logic.

Routes:
- POST /analyze_stock_trends: Analyzes stock trends based on provided stock data.
"""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from trading_kit.strategies.analyze_stock_trends import analyze_stock_trends as ast

from trading_kit_fastapi.api.models import AnalysisResult, StockData  # Updated import

router = APIRouter()


def nan_to_none(value: float) -> Optional[float]:
    """
    Converts NaN values to None.

    Args:
        value (float): The value to check for NaN.

    Returns:
        Optional[float]: None if the value is NaN, otherwise the original value.
    """
    if isinstance(value, float) and np.isnan(value):
        return None
    return value


@router.post("/analyze_stock_trends", response_model=AnalysisResult)
async def analyze_stock_trends_endpoint(stock_data: StockData) -> AnalysisResult:
    """
    Analyzes stock trends based on provided stock data.

    This endpoint accepts stock data including prices, dates, and analysis parameters.
    It performs trend analysis using the analyze_stock_trends function from the
    trading_kit library and returns the results in a structured format.

    Args:
        stock_data (StockData): The stock data for analysis, including prices, dates,
                                short and long window sizes, and precision.

    Returns:
        AnalysisResult: The result of the trend analysis, including short and long
                        weighted moving averages, signals, and a summary of signals.

    Raises:
        HTTPException: If the analysis fails, an HTTP 400 error is raised with a
                       descriptive error message.
    """
    try:
        # Convert input data to pandas Series
        prices = pd.Series(
            stock_data.prices, index=pd.to_datetime(stock_data.dates), name="Close"
        )

        # Perform trend analysis
        short_wma, long_wma, signals = ast(
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
