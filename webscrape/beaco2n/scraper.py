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

from webscrape.utils import download

__all__ = ["scrape_data", "scrape_data_pipeline"]

pathType = Union[str, Path]


# def download(url, filename):
    # """ From https://stackoverflow.com/a/63831344/

    # """
#     import functools
#     import pathlib
#     import shutil
#     import requests
#     from tqdm.auto import tqdm

#     r = requests.get(url, stream=True, allow_redirects=True)
#     if r.status_code != 200:
#         r.raise_for_status()  # Will only raise for 4xx codes, so...
#         raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
#     file_size = int(r.headers.get("Content-Length", 0))
#     path = pathlib.Path(filename).expanduser().resolve()
#     path.parent.mkdir(parents=True, exist_ok=True)
#     desc = "(Unknown total file size)" if file_size == 0 else ""
#     r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
#     with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
#         with path.open("wb") as f:
#             shutil.copyfileobj(r_raw, f)
#     return path


# def _download_data(url: str) -> bytes:
#     """Download the data at the given URL. This function tries to be polite
#     and tries not to hammer the remote server with requests.

#     Args:
#         url: URL to csv file
#     Returns:
#         bytes: Returned content from http request
#     """
#     # If we get any of these codes we'll try again
#     retriable_status_codes = [
#         requests.codes.internal_server_error,
#         requests.codes.bad_gateway,
#         requests.codes.service_unavailable,
#         requests.codes.gateway_timeout,
#         requests.codes.too_many_requests,
#         requests.codes.request_timeout,
#     ]

#     retry_strategy = Retry(
#         total=3,
#         status_forcelist=retriable_status_codes,
#         allowed_methods=["HEAD", "GET", "OPTIONS"],
#         backoff_factor=1,
#     )

#     adapter = HTTPAdapter(max_retries=retry_strategy)

#     http = requests.Session()
#     http.mount("https://", adapter)
#     http.mount("http://", adapter)

#     timeout = 20  # seconds
#     data = http.get(url, timeout=timeout).content

#     return data


def scrape_data(metadata_filepath: pathType, output_directory: pathType = None) -> None:
    """Download data from the BEACO2N website for sites given in the metadata file

    Args:
        metadata_filepath: Path to metadata file, this must contain the site codes
        output_directory: Folder to write data out
    Returns:
        None
    """
    with open(metadata_filepath, "r") as f:
        site_metadata = json.load(f)

    scrape_data_pipeline(metadata=site_metadata, output_directory=output_directory, pipeline=pipeline)


def scrape_data_pipeline(metadata: Dict, output_directory: pathType = None) -> None:
    """Download data from the BEACO2N website. This version expects a dictionary of metadata instead
    of the path to the metadata JSON

    Args:
        metadata: Metadata read from JSON
        output_directory: Folder to write data out
    Returns:
        None
    """
    # This is just the current datetime in ISO format to the nearest second
    end_date = pd.Timestamp.now().round("1s").isoformat(" ").replace(" ", "%20")

    # tqdm here just decorates the dictionary so we can track
    # the iteration process for the progress bar
    site_metadata_pbar = tqdm(metadata.items())

    print(metadata)

    for node_name, data in site_metadata_pbar:
        site_metadata_pbar.set_description(f"Getting data for {node_name}")

        name_for_url = data["long_name"].replace(" ", "%20")
        node_number = data["id"]

        # Retrieve the data from the deployment data onwards
        start_date = pd.Timestamp(data["deployed"]).round("1s").isoformat(" ").replace(" ", "%20")

        url = f"http://beacon.berkeley.edu/node/{node_number}/measurements/csv?name={name_for_url}&interval=60&start={start_date}&end={end_date}"

        print(f"\nGetting: {url}\n")

        data = download(url=url)
        filename = f"{node_number}_{node_name}.csv"

        if output_directory is not None:
            output_filepath = Path(output_directory).joinpath(filename)
        else:
            output_filepath = filename

        with open(output_filepath, "wb") as f:
            f.write(data)

        time.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to site metadata JSON", type=str)
    args = parser.parse_args()

    filepath = Path(args.filepath)

    process_sites(metadata_filepath=filepath)
