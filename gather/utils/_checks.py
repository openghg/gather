from typing import Union
import math
import pandas as pd

__all__ = ["check_date", "check_nan"]


def check_date(date: str) -> str:
    """Check if a date string can be converted to a pd.Timestamp
    and returns NA if not.

    Returns a string that can be JSON serialised.

    Args:
        date: String to test
    Returns:
        str
    """
    try:
        d = pd.Timestamp(date)
        if pd.isnull(d):
            return "NA"

        return date
    except ValueError:
        return "NA"


def check_nan(data: Union[int, float]) -> Union[str, float, int]:
    """Check if a number is Nan.

    Returns a string that can be JSON serialised.

    Args:
        data: Number
    Returns:
        str, float, int: Returns NA if not a number else number
    """
    if math.isnan(data):
        return "NA"
    else:
        return round(data, 3)
