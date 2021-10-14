""" This can be used to retrieve, process and export the required AQMesh data.

"""

import argparse
from pathlib import Path
import json
from pandas import Timestamp, Timedelta
from tempfile import TemporaryDirectory
from typing import Dict, List, Union

from webscrape.aqmesh import scrape_data, process_pipeline, export_pipeline

pathType = Union[str, Path]


def pipeline(
    species: Union[str, List],
    selected_vars: List,
    export_filepath: pathType,
    download_path: pathType,
    sites: List = None,
) -> None:
    """Run the whole processing pipeline

    Args:
        species: List of species to process
        selected_vars: Variables from data we want to export
        export_filepath: Path to write dashboard data
        download_path: Output directory for processed
        sites: List of sites to export
    Returns:
        None
    """
    if not isinstance(species, list):
        species = [species]

    if download_path is None:
        tmpdir = TemporaryDirectory()
        download_path = tmpdir.name

    # Check to see if we've downloaded the data within the last 6 hours
    scrape_log = Path("scrape_log.txt")

    scrape_complete = False
    if scrape_log.exists():
        scrape_time_str = scrape_log.read_text()
        scrape_time = Timestamp(scrape_time_str)

        if Timestamp.now() - scrape_time < Timedelta(hours=6.0):
            scrape_complete = True

    file_list = scrape_data(species=species, download_path=download_path)
    processing_results = process_pipeline(extracted_files=file_list)

    # Not all sites might have measurements for each species
    all_sites = set()
    for species, site_data in processing_results.items():
        all_sites.update(site_data.keys())

    if sites is not None:
        sites = [s.lower() for s in sites]
        all_sites = all_sites.intersection(sites)

    all_sites = list(all_sites)
    json_data = export_pipeline(
        species=species, selected_vars=selected_vars, output_filepath=export_filepath, sites=all_sites
    )

    with open(export_filepath, "w") as f:
        json.dump(json_data, f)

    print(f"\nData written to {export_filepath}")

    try:
        tmpdir.cleanup()
    except (NameError, AttributeError):
        pass


if __name__ == "__main__":
    example_text = """Usage:

    $ python run_pipeline_aqmesh.py --species <species> --vars <species vars> --export <JSON file out> --dir <optional download folder>

    Example:
    
    $ python run_pipeline_aqmesh.py --species co2 --vars co2 --export aq_mesh.json --dir aqmesh_download/

    Downloads the CO2 data to aqmesh_download/, processes it and exports it to aq_mesh.json

    $ python run_pipeline_aqmesh.py --species co2 --vars co2 --export aq_mesh.json

    Does the same but ownloads the CO2 data to a temporary directory, processes it and exports it to aq_mesh.json

    """
    parser = argparse.ArgumentParser(
        prog="AQMesh scraping pipeline",
        description="Script to allow easy scraping and processing of AQMesh data.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--species", help="species data to export", nargs="*", type=str)
    parser.add_argument(
        "--vars", help="variables to extract from data such e.g. ch4 co2", nargs="*", type=str
    )
    parser.add_argument("--export", help="filepath for dashboard data export")
    parser.add_argument("--dir", help="directory for data download", type=str)

    args = parser.parse_args()

    species = args.species
    selected_vars = args.vars
    export_filepath = args.export
    download_dir = args.dir

    pipeline(
        species=species,
        selected_vars=selected_vars,
        export_filepath=export_filepath,
        download_path=download_dir,
    )
