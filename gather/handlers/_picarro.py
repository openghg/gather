from typing import Dict
from gather.pipeline import run_glasgow_picarro


def picarro(data: bytes) -> Dict:
    """Pass the data to the Glasgow Picarro pipeline function

    Args:
        data: Binary data
    Returns:
        dict: Dictionary of processed data
    """
    return run_glasgow_picarro(data=data)
