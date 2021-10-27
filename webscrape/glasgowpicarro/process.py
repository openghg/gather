from openghg.modules import ObsSurface
from typing import Dict, Union
from pathlib import Path

pathType = Union[str, Path]

__all__ = ["process_pipeline"]


def process_pipeline(filepath: pathType) -> Dict[str, Dict[Union[str, Dict]]]:
    """Process the data from the Glasgow Science tower Picarro"""
    filepath = Path(filepath)
    filename = filepath.name

    results = {}

    try:
        results[filename] = ObsSurface.read_file(
            filepath=filepath,
            data_type="GLASGOWPICARRO",
            network="npl_picarro",
            site="GST",
        )
    except ValueError:
        results[filename] = "No change to data"

    return results
