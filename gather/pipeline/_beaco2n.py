from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Union

from gather.beaco2n import (
    scrape_data_pipeline,
    process_beaco2n_pipeline,
)
from gather.utils import load_json, export_pipeline
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

                to_update = {
                    k: v for k, v in site_metadata.items() if k not in data_metadata
                }
                data_metadata.update(to_update)

    return data_copy


def run_beaco2n(selected_vars: List, download_path: pathType = None) -> Dict:
    """Run the pipeline to scrape, process and export data from the
    BEACO2N project (http://beacon.berkeley.edu/)

    Args:
        selected_vars: Variables from data we want to export
        download_path: Output directory for processed
    Returns:
        dict: Dictionary of network data
    """
    if download_path is None:
        tmpdir = TemporaryDirectory()
        download_path = tmpdir.name

    if not isinstance(selected_vars, list):
        selected_vars = [selected_vars]

    # Do a quick check to make sure co2 is in the selected vars, for this
    # network we only have CO2 measurements
    if not(any(f for f in selected_vars if "co2" in f)):
        raise ValueError("We can only export CO2 data from BEACO2N.")

    # First load the metadata
    metadata = load_json(filename="beaco2n_sites.json")

    filepaths = scrape_data_pipeline(metadata=metadata, download_path=download_path)

    # Process the data with OpenGHG
    process_beaco2n_pipeline(filepaths=filepaths, metadata=metadata)

    # Here we want to export all the sites
    site_names = list(metadata.keys())
    # Now we can export the processed data in a format expected by the dashboard
    json_data = export_pipeline(sites=site_names, selected_vars=selected_vars)

    # Now combine the data and metadata so we have everything in one place
    combined_data = _combine(metadata=metadata, data=json_data)

    try:
        tmpdir.cleanup()
    except (NameError, AttributeError):
        pass

    return combined_data
