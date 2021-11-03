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
from addict import Dict as aDict
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, Union

from gather.utils import is_date, is_nan

__all__ = ["parse_metadata"]


def parse_metadata(metadata_filepath: Union[str, Path], pipeline: bool = False) -> Dict:
    """Parse the metadata file retreived from the BEACO2N site

    Args:
        metadata_filepath: Path of raw CSV metadata file
        pipeline: Are we running as part of the pipeline? If True
        return the parsed site information dictionary.
    Returns:
        dict: Dictionary of site metadata
    """
    metadata_filepath = Path(metadata_filepath).resolve()
    raw_metadata = pd.read_csv(metadata_filepath)

    site_metadata = aDict()
    for index, row in raw_metadata.iterrows():
        site_name = row["node_name_long"].lower().replace(" ", "")
        site_data = site_metadata[site_name]

        site_data["long_name"] = row["node_name_long"]
        site_data["id"] = row["id"]
        site_data["latitude"] = round(row["lat"], 5)
        site_data["longitude"] = round(row["lng"], 5)
        site_data["magl"] = is_nan(row["height_above_ground"])
        site_data["masl"] = is_nan(row["height_above_sea"])
        site_data["deployed"] = is_date(row["deployed"])
        site_data["node_folder_id"] = row["node_folder_id"]

    # Convert to a normal dict
    metadata = site_metadata.to_dict()

    if not pipeline:
        output_filepath = f"{str(metadata_filepath.stem)}_parsed.json"
        print(f"\nMetadata written to ./{output_filepath}")
        with open(output_filepath, "w") as f:
            json.dump(metadata, f, sort_keys=True, indent=4)

    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path of file to parse", type=str)
    args = parser.parse_args()

    filepath = Path(args.filepath)
