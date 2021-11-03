"""
This can be used to run the whole data scrape, process and export pipeline.
If you just want to run a single state see the scripts in the beaco2n/ directory.

"""
import argparse
from gather.pipeline import run_beaco2n

if __name__ == "__main__":
    example_text = """Usage:

    $ python run_pipeline_beaco2n.py --vars co2 --export glasgow_co2_data.json --dir beaco2n/

    Downloads, processes and exports the data to a glasgow_co2_data.json file. Retrieved raw files are downloaded to the
    beaco2n/ directory.

    Similary running

    $ python run_pipeline_beaco2n.py --vars co2 --export glasgow_co2_data.json

    would do the same thing but would store the downloaded raw files in a temporary directory which is cleaned up
    after run.

    $ python run_pipeline_beaco2n.py --vars <species to extract> --export <processed data out JSON> --dir <download directory>

    """

    parser = argparse.ArgumentParser(
        prog="BEACO2N scraping pipeline",
        description="Script to allow easy scraping and processing of BEACO2N data.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # parser.add_argument("--meta", help="path to JSON metadata file", type=str)
    parser.add_argument(
        "--vars", help="variables to extract from data such e.g. ch4 co2", nargs="*", type=str
    )
    parser.add_argument("--export", help="filepath for dashboard data export")
    parser.add_argument("--dir", help="directory for data download", type=str)

    args = parser.parse_args()

    # metadata_path = args.meta
    download_path = args.dir
    selected_vars = args.vars
    export_filepath = args.export

    run_beaco2n(
        download_path=download_path,
        selected_vars=selected_vars,
        export_filepath=export_filepath,
    )
