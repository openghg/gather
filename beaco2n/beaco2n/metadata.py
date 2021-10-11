"""
This script extracts the site data available in the CSV located at
http://beacon.berkeley.edu/get_latest_nodes/csv/

To use:

$ python extract_site_data.py get_latest_nodes.csv

Will create a file called

get_latest_nodes_parsed.json

Or for other files with the same schema

$ python extract_site_data.py <filepath_to_csv>

"""
import json
import pandas as pd
from collections import defaultdict
import math
import argparse
import numpy as np
from pathlib import Path
from typing import Dict, Union

__all__ = ["parse_metadata"]


def _date_or_not(date: str) -> str:
    """Functional but pretty limited"""
    try:
        d = pd.Timestamp(date)
        if pd.isnull(d):
            return "NA"

        return date
    except ValueError:
        return "NA"


def _nan_or_not(data: Union[int, float]) -> Union[str, float, int]:
    try:
        if math.isnan(data):
            return "NA"
        else:
            return round(data, 3)
    except TypeError as e:
        print(data, e)


def parse_metadata(metadata_filepath: Union[str, Path], pipeline: bool = False) -> Union[Dict, None]:
    """Parse the metadata file retreived from the BEACO2N site

    Args:
        metadata_filepath: Path of raw CSV metadata file
        pipeline: Are we running as part of the pipeline? If True
        return the parsed site information dictionary.
    Returns:
        dict or None
    """
    site_data = pd.read_csv(metadata_filepath)

    site_dict = defaultdict(dict)

    for index, row in site_data.iterrows():
        site_name = row["node_name_long"].lower().replace(" ", "")
        node_data = site_dict[site_name]

        node_data["long_name"] = row["node_name_long"]
        node_data["id"] = row["id"]
        node_data["latitude"] = round(row["lat"], 5)
        node_data["longitude"] = round(row["lng"], 5)
        node_data["magl"] = _nan_or_not(row["height_above_ground"])
        node_data["masl"] = _nan_or_not(row["height_above_sea"])
        node_data["deployed"] = _date_or_not(row["deployed"])
        node_data["node_folder_id"] = row["node_folder_id"]

    if pipeline:
        return site_dict
    else:
        output_filepath = f"{str(filepath.stem)}_parsed.json"
        with open(output_filepath, "w") as f:
            json.dump(site_dict, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path of file to parse", type=str)
    args = parser.parse_args()

    filepath = Path(args.filepath)
