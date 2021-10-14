"""
This can be used to run the whole data scrape, process and export pipeline.
If you just want to run a single state see the scripts in the beaco2n/ directory.

"""
import argparse
from pathlib import Path
import json
from pandas import Timestamp, Timedelta
from tempfile import TemporaryDirectory
from typing import Dict, List, Union

from webscrape.beaco2n import parse_metadata, scrape_data_pipeline, process_beaco2n_pipeline, export_pipeline
from copy import deepcopy

pathType = Union[str, Path]


def combine(metadata: Dict, data: Dict) -> Dict:
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
                site_metadata = metadata[network][site]

                to_update = {k: v for k, v in site_metadata.items() if k not in data_metadata}
                data_metadata.update(to_update)

    return data_copy


def pipeline(
    metadata_filepath: pathType, selected_vars: List, export_filepath: pathType, download_path: pathType = None
) -> None:
    """Run the pipeline to scrape, process and export data from the
    BEACO2N project (http://beacon.berkeley.edu/)

    Args:
        metadata_filepath: Path to site metadata CSV
        selected_vars: Variables from data we want to export
        export_filepath: Path to write dashboard data
        download_path: Output directory for processed
    Returns:
        None
    """
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

    # First parse the metadata retrieved from the BEACO2N site
    metadata = parse_metadata(metadata_filepath=metadata_filepath, pipeline=True)

    # Then we download the data
    if not scrape_complete:
        scrape_data_pipeline(metadata=metadata, output_directory=download_path)
        now = str(Timestamp.now())
        scrape_log.write_text(now)

    # Process the data with OpenGHG
    results = process_beaco2n_pipeline(data_path=download_path, metadata=metadata)

    site_names = list(metadata["beaco2n"].keys())
    # Now we can export the processed data in a format expected by the dashboard
    json_data = export_pipeline(sites=site_names, selected_vars=selected_vars)

    # Now combine the data and metadata so we have everything in one place
    combined_data = combine(metadata=metadata, data=json_data)

    with open(export_filepath, "w") as f:
        json.dump(combined_data, f)

    print(f"\nData written to {export_filepath}")

    try:
        tmpdir.cleanup()
    except (NameError, AttributeError):
        pass


if __name__ == "__main__":
    example_text = """Usage:

    $ python run_pipeline_beaco2n.py --meta glasgow_nodes.csv --vars co2 --export glasgow_co2_data.json --dir beaco2n/

    Downloads, processes and exports the data to a glasgow_co2_data.json file. Retrieved raw files are downloaded to the
    beaco2n/ directory.

    Similary running

    $ python run_pipeline_beaco2n.py --meta glasgow_nodes.csv --vars co2 --export glasgow_co2_data.json

    would do the same thing but would store the downloaded raw files in a temporary directory which is cleaned up
    after run.

    $ python run_pipeline_beaco2n.py --meta <metadata csv> --vars <species to extract> --export <proc. data out JSON> --dir <download directory>

    """

    parser = argparse.ArgumentParser(
        prog="BEACO2N scraping pipeline",
        description="Script to allow easy scraping and processing of BEACO2N data.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--meta", help="path to JSON metadata file", type=str)
    parser.add_argument("--vars", help="variables to extract from data such e.g. ch4 co2", nargs="*", type=str)
    parser.add_argument("--export", help="filepath for dashboard data export")
    parser.add_argument("--dir", help="directory for data download", type=str)

    args = parser.parse_args()

    metadata_path = args.meta
    download_path = args.dir
    selected_vars = args.vars
    export_filepath = args.export

    pipeline(
        metadata_filepath=metadata_path,
        download_path=download_path,
        selected_vars=selected_vars,
        export_filepath=export_filepath,
    )
