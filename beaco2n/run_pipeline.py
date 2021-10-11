"""
This can be used to run the whole data scrape, process and export pipeline.
If you just want to run a single state see the scripts in the beaco2n/ directory.

"""
import argparse
from pathlib import Path
from typing import List, Union
from pandas import Timestamp

from beaco2n.metadata import parse_metadata
from beaco2n.scraper import scrape_data_pipeline
from beaco2n.process import process_beaco2n_pipeline
from beaco2n.export import export_pipeline

pathType = Union[str, Path]


def pipeline(
    metadata_filepath: pathType, download_dir: pathType, selected_vars: List, export_filepath: pathType = None
) -> None:
    """Run the pipeline to scrape, process and export data from the
    BEACO2N project (http://beacon.berkeley.edu/)

    Args:
        metadata_filepath: Path to site metadata CSV
        download_dir: Output directory for processed
        selected_vars: Variables from data we want to export
        export_filepath: Path to write dashboard data
    Returns:
        None
    """
    # First parse the metadata retrieved from the BEACO2N site
    metadata = parse_metadata(metadata_filepath=metadata_filepath, pipeline=True)
    # Then we download the data
    scrape_data_pipeline(metadata=metadata, output_directory=download_dir)
    # Process the data with OpenGHG
    results = process_beaco2n_pipeline(data_path=download_dir, metadata=metadata)

    if export_filepath is None:
        timestamp_str = Timestamp.now().round("1s").isoformat()
        export_filepath = Path(download_dir).joinpath(f"dashboard_data_{timestamp_str}")

    # Now we can export the processed data in a format expected by the dashboard
    export_pipeline(metadata=metadata, selected_vars=selected_vars, output_filepath=export_filepath)


if __name__ == "__main__":
    example_text = """Usage:

    $ python run_pipeline.py <metadata_json> <download_path>/ <variable1 variable2 ...>

    $ python run_pipeline.py <metadata_json> <download_path>/ <variable1 variable2 ...> --export /path/to/exported_data.json

    Example:

    $ python run_pipeline.py glasgow_metadata.json download/ co2

    This downloads the scraped data to download/ and exports only the CO2 measurements to a 
    file called dashboard_data_<timestamp>.json in download/

    $ python run_pipeline.py glasgow_metadata.json download/ co2 --export ~/glasgow_data.json
    
    This does the same as above but exports the CO2 data to the file glasgow_data.json
    in the user's home directory
    """

    parser = argparse.ArgumentParser(
        prog="BEACO2N scraping pipeline",
        description="Script to allow easy scraping and processing of BEACO2N data.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("json_path", help="path to JSON metadata file", type=str)
    parser.add_argument("download_dir", help="directory for data download", type=str)
    parser.add_argument("vars", help="variables to extract from data such e.g. ch4 co2", nargs="*", type=str)
    parser.add_argument("--export", help="filepath for dashboard data export")

    args = parser.parse_args()

    json_path = args.json_path
    download_dir = args.download_dir
    selected_vars = args.vars
    export_filepath = args.export

    pipeline(
        metadata_filepath=json_path,
        download_dir=download_dir,
        selected_vars=selected_vars,
        export_filepath=export_filepath,
    )
