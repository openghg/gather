from typing import Union

__all__ = ["is_date", "is_nan"]

def is_date(date: str) -> str:
    """Functional but pretty limited"""
    try:
        d = pd.Timestamp(date)
        if pd.isnull(d):
            return "NA"

        return date
    except ValueError:
        return "NA"


def is_nan(data: Union[int, float]) -> Union[str, float, int]:
    try:
        if math.isnan(data):
            return "NA"
        else:
            return round(data, 3)
    except TypeError as e:
        print(data, e)