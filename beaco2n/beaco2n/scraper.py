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
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from tqdm import tqdm
import json
import argparse
from pathlib import Path
from typing import Dict, Union

__all__ = ["scrape_data"]

pathType = Union[str, Path]

def _download_data(url: str) -> bytes:
    """Download the data at the given URL. This function tries to be polite
    and tries not to hammer the remote server with requests.

    Args:
        url: URL to csv file
    Returns:
        bytes: Returned content from http request
    """
    # If we get any of these codes we'll try again
    retriable_status_codes = [
        requests.codes.internal_server_error,
        requests.codes.bad_gateway,
        requests.codes.service_unavailable,
        requests.codes.gateway_timeout,
        requests.codes.too_many_requests,
        requests.codes.request_timeout,
    ]

    retry_strategy = Retry(
        total=3,
        status_forcelist=retriable_status_codes,
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    timeout = 20  # seconds
    data = http.get(url, timeout=timeout).content

    return data


def scrape_data(metadata_filepath: pathType, output_folder: pathType = None, pipeline: bool = False) -> None:
    """Download data from the BEACO2N website for sites given in the metadata file

    Args:
        metadata_filepath: Path to metadata file, this must contain the site codes
    Returns:
        None
    """
    with open(metadata_filepath, "r") as f:
        site_metadata = json.load(f)

    start_date = start_date.replace(" ", "%20")

    # This is just the current datetime in ISO format to the nearest second
    end_date = pd.Timestamp.now().round("1s").isoformat(" ").replace(" ", "%20")

    # tqdm here just decorates the dictionary so we can track
    # the iteration process for the progress bar
    site_metadata_pbar = tqdm(site_metadata.items())

    for node_name, data in site_metadata_pbar:
        site_metadata_pbar.set_description(f"Getting data for {node_name}")

        name_for_url = data["long_name"].replace(" ", "%20")
        node_number = data["id"]

        # Retrieve the data from the deployment data onwards
        start_date = pd.Timestamp(data["deployed"]).round("1s").isoformat(" ").replace(" ", "%20")

        url = f"http://beacon.berkeley.edu/node/{node_number}/measurements/csv?name={name_for_url}&interval=60&start={start_date}&end={end_date}"

        print(f"\nGetting: {url}")
    
        data = _download_data(url=url)
        filename = f"{node_number}_{node_name}.csv"

        if output_folder is not None:
            output_filepath = Path(output_folder).joinpath(filename)
        else:
            output_filepath = filename

        with open(output_filepath, "wb") as f:
            f.write(data)

        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to site metadata JSON", type=str)
    args = parser.parse_args()

    filepath = Path(args.filepath)

    process_sites(metadata_filepath=filepath)