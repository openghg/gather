""" This can be used to retrieve, process and export the required AQMesh data.

"""

from webscrape.pipeline import run_aqmesh

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

    run_aqmesh(
        species=species,
        selected_vars=selected_vars,
        export_filepath=export_filepath,
        download_path=download_dir,
    )
