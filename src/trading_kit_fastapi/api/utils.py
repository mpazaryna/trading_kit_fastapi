from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


def to_dict_with_nan(data: pd.Series) -> Dict[str, Optional[float]]:
    """
    Convert a pandas Series to a dictionary, handling NaN values.

    Args:
        data (pd.Series): The pandas Series to convert. The index should be datetime objects,
                          and the values should be floats.

    Returns:
        Dict[str, Optional[float]]: A dictionary where the keys are date strings in 'YYYY-MM-DD' format
                                    and the values are either floats or None if the original value was NaN.
    """
    return {
        date.strftime("%Y-%m-%d"): nan_to_none(value) for date, value in data.items()
    }


def to_signal_dict_with_nan(data: pd.Series) -> Dict[str, Optional[int]]:
    """
    Convert a pandas Series of signals to a dictionary, handling NaN values.

    Args:
        data (pd.Series): The pandas Series to convert. The index should be datetime objects,
                          and the values should be integers or NaN.

    Returns:
        Dict[str, Optional[int]]: A dictionary where the keys are date strings in 'YYYY-MM-DD' format
                                  and the values are either integers or None if the original value was NaN.
    """
    return {
        date.strftime("%Y-%m-%d"): nan_to_none(
            int(value) if not np.isnan(value) else None
        )
        for date, value in data.items()
    }


def nan_to_none(value: Any) -> Optional[Any]:
    """
    Convert NaN values to None.

    Args:
        value (Any): The value to check.

    Returns:
        Optional[Any]: None if the value is NaN, otherwise the value itself.
    """
    try:
        return None if np.isnan(value) else value
    except TypeError:
        return value
