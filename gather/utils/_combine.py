from typing import List, Union
from pathlib import Path
import json


__all__ = ["combine_networks"]


def combine_networks(data_files: List, output_file: Union[str, Path]) -> None:
    """Combine the data from multiple networks into a single site
    We expect the JSON files to have been export by the OpenGHG to_dashboard function.

    Args:
        data_files: List of data files to concatenate
    Returns:
        None
    """
    combined = {}
    for file in data_files:
        data = json.loads(Path(file).read_text())
        combined.update(data)

    output_file = Path(output_file)
    output_file.write_text(json.dumps(combined))

    print(f"\nCombined data written to {str(output_file)}\n")
