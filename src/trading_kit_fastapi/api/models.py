"""
This module defines the Pydantic models used for input validation and response schemas
in the Trading Kit FastAPI application.

Pydantic models are used to ensure data integrity and provide automatic data validation
and parsing. They are preferred over raw dictionaries for the following reasons:

1. **Type Safety**: Pydantic models enforce type hints, ensuring that the data conforms
   to the expected types. This reduces runtime errors and improves code reliability.

2. **Data Validation**: Pydantic models automatically validate input data, raising
   informative errors when the data does not meet the specified constraints. This helps
   in catching invalid data early in the request processing pipeline.

3. **Data Parsing**: Pydantic models can parse and convert input data into the desired
   types, making it easier to work with different data formats (e.g., converting strings
   to dates).

4. **Documentation**: Pydantic models provide a clear and concise way to document the
   expected structure of the data, making the codebase more maintainable and easier to
   understand.

5. **Integration with FastAPI**: Pydantic models integrate seamlessly with FastAPI,
   allowing for automatic request validation and response serialization. This reduces
   boilerplate code and improves developer productivity.

The following models are defined in this module:

- `StockData`: Represents stock data for a company, including dates, prices, and
  calculation parameters.
- `AnalysisResult`: Represents the result of analyzing stock data, including WMA values,
  trading signals, and a summary of the analysis.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, conlist


class StockData(BaseModel):
    """
    Model representing stock data for a company.

    Attributes:
        company_name (str): Name of the company.
        dates (List[str]): List of dates in YYYY-MM-DD format.
        prices (List[float]): List of closing prices corresponding to the dates.
        short_window (int): Short-term WMA window size. Default is 10.
        long_window (int): Long-term WMA window size. Default is 30.
        precision (int): Decimal precision for calculations. Default is 2.
    """

    company_name: str = Field(..., description="Name of the company")
    dates: conlist(str, min_length=1) = Field(
        ..., description="List of dates in YYYY-MM-DD format"
    )
    prices: conlist(float, min_length=1) = Field(
        ..., description="List of closing prices corresponding to the dates"
    )
    short_window: int = Field(10, description="Short-term WMA window size")
    long_window: int = Field(30, description="Long-term WMA window size")
    precision: int = Field(2, description="Decimal precision for calculations")


class AnalysisResult(BaseModel):
    """
    Model representing the analysis result of stock data.

    Attributes:
        company_name (str): Name of the company.
        short_wma (Dict[str, Optional[float]]): Short-term WMA values keyed by date.
        long_wma (Dict[str, Optional[float]]): Long-term WMA values keyed by date.
        signals (Dict[str, Optional[int]]): Trading signals keyed by date.
        summary (Dict[str, int]): Summary of the analysis.
    """

    company_name: str = Field(..., description="Name of the company")
    short_wma: Dict[str, Optional[float]] = Field(
        ..., description="Short-term WMA values keyed by date"
    )
    long_wma: Dict[str, Optional[float]] = Field(
        ..., description="Long-term WMA values keyed by date"
    )
    signals: Dict[str, Optional[int]] = Field(
        ..., description="Trading signals keyed by date"
    )
    summary: Dict[str, int] = Field(..., description="Summary of the analysis")
