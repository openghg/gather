import json
from pathlib import Path
from typing import Dict, List, Union

__all__ = ["load_json"]


def load_json(filename: str) -> Dict:
    """Read JSON file from metadata folder

    Args:
        filename: Name of metadata file
    Returns:
        dict: Dictionary of data
    """
    filepath = (
        Path(__file__).resolve().parent.parent.joinpath("metadata").joinpath(filename)
    )

    metadata: Dict = json.loads(filepath.read_text())

    return metadata


def parse_json(data: Union[str, bytes]) -> Dict:
    """Parse the string or bytes passed in and make sure
    a dictionary/list is created. Otherwise passing values such as 10 in to the
    decoder returns "valid" JSON.

    Args:
        data: Data to be deserialised
    Returns:
        dict/list: Data structure from data
    """
    data: Union[List, Dict] = json.loads(data)

    if not isinstance(data, (dict, list)):
        raise TypeError("We expect a dictionary or list from JSON data")

    return data
