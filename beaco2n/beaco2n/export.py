""" 
This script is used to retrieve data from the OpenGHG object store, process it to a format
that's expected by the dashboard and then write it to a JSON file.

Usage:

$ python retrieve_export.py <node_data_json> <species to extract> <outfile filename (optional)>

for example

$ python retrieve_export.py glasgow_nodes_parsed.json co2 co pm

This will create a dashboard_data.json file with data from the sites in glasgow_nodes_parsed.json and
CO2, CO and PM (particulate matter) measurements.

To export to a different filename

$ python retrieve_export.py glasgow_nodes_parsed.json co2 co pm --out my_data_file.json

For help

$ python retrieve_export.py -h

"""
from openghg.processing import search
from openghg.util import to_dashboard
import argparse
import json
from pathlib import Path
from typing import Dict, List, Union

__all__ = ["export", "export_pipeline"]

pathType = Union[str, Path]


def export_pipeline(metadata: Dict, selected_vars: List[str], output_filepath: pathType) -> None:
    """Retrieve data from the object store and export it to JSON. Pipeline version that
    expects site metadata as a dict instead of a filepath to JSON.

    Args:
        metadata: Site metadata
        selected_vars: Variables to extract from data such as speices names, e.g. ["co2", "co", "pm"]
        output_filepath: Filepath for writing data, if not given data will be written to dashboard_data.json
    Returns:
        None
    """
    site_names = list(metadata.keys())
    results = search(site=site_names)

    if not results:
        raise ValueError(
            "Unable to find any data for the given sites. Make sure you've processed the correct data."
        )

    data = results.retrieve_all()

    to_dashboard(data=data, selected_vars=selected_vars, filename=output_filepath)

    print(f"Data written to {output_filepath}")


def export(json_path: Union[str, Path], selected_vars: List[str], output_filepath: str) -> None:
    """Retrieve data from the object store and export it to JSON.

    Args:
        json_path: Path to site JSON
        selected_vars: Variables to extract from data such as speices names, e.g. ["co2", "co", "pm"]
        output_filepath: Filepath for writing data, if not given data will be written to dashboard_data.json
    Returns:
        None
    """
    json_path = Path(json_path)
    site_data = json.loads(json_path.read_text())

    export_pipeline(metadata=site_data, selected_vars=selected_vars, output_filepath=output_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", help="path to JSON metadata file", type=str)
    parser.add_argument(
        "vars", help="variables to extract from data such e.g. co co2 pm", nargs="*", type=str
    )
    parser.add_argument(
        "--out", help="filename for JSON data, if not given data is written to dashboard_data.json"
    )

    args = parser.parse_args()

    json_path = args.json_path
    selected_vars = args.vars
    outfile = args.out

    retrieve_export(json_path=json_path, selected_vars=selected_vars, output_filename=outfile)
