"""
This can be used to run the whole data scrape, process and export pipeline.
If you just want to run a single state see the scripts in the beaco2n/ directory.

"""
import argparse
from pathlib import Path
from typing import Union

from beaco2n.metadata import parse_metadata
from beaco2n.scraper import scrape_data
from beaco2n.process import process_beaco2n
from beaco2n.export import retrieve_export

pathType = Union[str, Path]


def pipeline(metadata_filepath: pathType, output_directory: pathType = None) -> None:
    """Run the pipeline to scrape, process and export data from the
    BEACO2N project (http://beacon.berkeley.edu/)

    Args:
        metadata_filepath: Path to site metadata CSV
        output_directory: Output directory for processed
        data
    Returns:
        None
    """
    metadata = parse_metadata(metadata_filepath=metadata_filepath, pipeline=True)
    
