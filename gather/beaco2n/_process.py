""" This file processes the files downloaded from the BEACO2N site using the get_data.py script

Usage:

$ python process_beaco2n.py data_folder/ glasgow_nodes_parsed.json

This processes all files in data_folder that have matching site names in glasgow_nodes_parsed.json

"""
from pathlib import Path
from typing import Dict, Union

__all__ = ["process_beaco2n_pipeline"]


pathType = Union[str, Path]


def process_beaco2n_pipeline(filepaths: Dict, metadata: Dict) -> Dict[str, Dict]:
    """Process the scraped data that has been written to file. This expects a dictionary of the type
    created by scrape_data_pipeline.

    Args:
        filepaths: Dictionary of scraped data filepaths, keyed by node id
    Returns:
        dict: Dictionary of Datasource records for each data file.
    """
    from openghg.modules import ObsSurface

    results = {}
    for node_id, filepath in filepaths.items():
        filename = filepath.stem
        split = filename.split("_")

        site_id = str(split[0])
        site_name = split[1]

        # Lookup the site metadata
        site_metadata = metadata[site_name]

        site_id_meta = str(site_metadata["id"])
        inlet = site_metadata["magl"]
        # Instrument name taken from http://beacon.berkeley.edu/metadata/
        instrument = "shinyei"
        network = "beaco2n"

        if site_id != site_id_meta:
            raise ValueError(
                f"Mismatch between read site ID ({site_id}) and metadata ID ({site_id_meta})"
            )
        try:
            result = ObsSurface.read_file(
                filepath=filepath,
                data_type="BEACO2N",
                site=site_name,
                network=network,
                inlet=inlet,
                instrument=instrument,
            )

            results[filename] = result
        except ValueError:
            # If there's no change to the available data we'll get a
            # "This file has been uploaded previously with the filename" error so catch that here
            results[filename] = "No change to data"

    return results
