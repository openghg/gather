""" This script downloads the data from the sites given in the
passed metadata file.

Usage:

$ python get_data.py <node_metadata_file>

e.g.

$ python get_data.py glasgow_nodes_parsed.json

This will create a file for each site containing the data from the date the equipment
was depoyed to the date.

These files can then be processed using the OpenGHG ObsSurface.read_file function
by passing the data_type as BEACO2N.
"""
import pandas as pd
import time
from tqdm import tqdm
import json
import argparse
from pathlib import Path
from typing import Dict, Union

from gather.utils import download

__all__ = ["scrape_data", "scrape_data_pipeline"]

pathType = Union[str, Path]


def scrape_data(metadata_filepath: pathType, download_path: pathType = None) -> None:
    """Download data from the BEACO2N website for sites given in the metadata file

    Args:
        metadata_filepath: Path to metadata file, this must contain the site codes
        download_path: Folder to write data out
    Returns:
        None
    """
    with open(metadata_filepath, "r") as f:
        site_metadata = json.load(f)

    scrape_data_pipeline(metadata=site_metadata, download_path=download_path)


def scrape_data_pipeline(metadata: Dict, download_path: pathType = None) -> Dict:
    """Download data from the BEACO2N website. This version expects a dictionary of metadata instead
    of the path to the metadata JSON

    Args:
        metadata: Metadata read from JSON
        download_path: Folder to write data out
    Returns:
        dict: Dictionary of node numbers and written filepaths
    """
    # This is just the current datetime in ISO format to the nearest second
    end_date = pd.Timestamp.now().round("1s").isoformat(" ").replace(" ", "%20")

    # tqdm here just decorates the dictionary so we can track
    # the iteration process for the progress bar
    site_metadata_pbar = tqdm(metadata.items())

    written_files = {}

    for node_name, data in site_metadata_pbar:
        site_metadata_pbar.set_description(f"Getting data for {node_name}")

        name_for_url = data["long_name"].replace(" ", "%20")
        node_number = data["id"]

        # Retrieve the data from the deployment data onwards
        start_date = (
            pd.Timestamp(data["deployed"])
            .round("1s")
            .isoformat(" ")
            .replace(" ", "%20")
        )

        url = f"http://beacon.berkeley.edu/node/{node_number}/measurements/csv?name={name_for_url}&interval=60&start={start_date}&end={end_date}"

        print(f"\nGetting: {url}\n")

        data = download(url=url)

        filename = f"{node_number}_{node_name}.csv"
        output_filepath = Path(download_path).joinpath(filename)

        with open(output_filepath, "wb") as f:
            f.write(data)

        written_files[str(node_number)] = output_filepath

        time.sleep(2)

    return written_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to site metadata JSON", type=str)
    args = parser.parse_args()

    filepath = Path(args.filepath)

    scrape_data(metadata_filepath=filepath)
