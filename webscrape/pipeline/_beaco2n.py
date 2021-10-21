import argparse
from pathlib import Path
import json
from pandas import Timestamp, Timedelta
from tempfile import TemporaryDirectory
from typing import Dict, List, Union

from webscrape.beaco2n import parse_metadata, scrape_data_pipeline, process_beaco2n_pipeline, export_pipeline
from webscrape.utils import load_json
from copy import deepcopy

pathType = Union[str, Path]

__all__ = ["run_beaco2n"]


def _combine(metadata: Dict, data: Dict) -> Dict:
    """Combine metadata and data, making sure there is data for each site

    Args:
        metadata: Dictionary of metadata
        data: Dictionary of JSONified data
    Returns:
        dict: Copy of data dictionary with extra metadata
    """
    data_copy = deepcopy(data)

    for network, network_data in data_copy.items():
        for species, species_data in network_data.items():
            for site, siteData in species_data.items():
                data_metadata = siteData["metadata"]
                site_metadata = metadata[site]

                to_update = {k: v for k, v in site_metadata.items() if k not in data_metadata}
                data_metadata.update(to_update)

    return data_copy


def run_beaco2n(selected_vars: List, export_filepath: pathType, download_path: pathType = None) -> None:
    """Run the pipeline to scrape, process and export data from the
    BEACO2N project (http://beacon.berkeley.edu/)

    Args:
        selected_vars: Variables from data we want to export
        export_filepath: Path to write dashboard data
        download_path: Output directory for processed
    Returns:
        None
    """
    if download_path is None:
        tmpdir = TemporaryDirectory()
        download_path = tmpdir.name

    # TODO - remove these checks for now, not necessary within the serverless pipeline setting
    # Can add them into another function that wraps this maybe?
    # # Check to see if we've downloaded the data within the last 6 hours, only useful
    # # if running this locally
    # scrape_log = Path("scrape_log.txt")

    # scrape_complete = False
    # if scrape_log.exists():
    #     scrape_time_str = scrape_log.read_text()
    #     scrape_time = Timestamp(scrape_time_str)

    #     if Timestamp.now() - scrape_time < Timedelta(hours=6.0):
    #         scrape_complete = True

    # First parse the metadata retrieved from the BEACO2N site
    # metadata = parse_metadata(metadata_filepath=metadata_filepath, pipeline=True)

    # First load the metadata
    metadata = load_json(filename="beaco2n_sites.json")

    # Then we download the data
    # if not scrape_complete:
    scrape_data_pipeline(metadata=metadata, output_directory=download_path)
    # now = str(Timestamp.now())
    # scrape_log.write_text(now)

    # Process the data with OpenGHG
    results = process_beaco2n_pipeline(data_path=download_path, metadata=metadata)

    site_names = list(metadata.keys())
    # Now we can export the processed data in a format expected by the dashboard
    json_data = export_pipeline(sites=site_names, selected_vars=selected_vars)

    # Now combine the data and metadata so we have everything in one place
    combined_data = _combine(metadata=metadata, data=json_data)

    with open(export_filepath, "w") as f:
        json.dump(combined_data, f)

    print(f"\nData written to {export_filepath}")

    try:
        tmpdir.cleanup()
    except (NameError, AttributeError):
        pass
