import json
from pathlib import Path
from typing import Dict

__all__ = ["load_json"]

def load_json(filename: str) -> Dict:
    """ Read JSON file from metadata folder

    Args:
        filename: Name of metadata file
    Returns:
        dict: Dictionary of data
    """
    filepath = Path(__file__).resolve().parent.parent.joinpath("metadata").joinpath(filename)

    return json.loads(filepath.read_text())