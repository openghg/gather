import argparse
from gather.utils import combine_networks

if __name__ == "__main__":
    example_text = """Usage:

    $ python run_pipeline_aqmesh.py --species <species> --vars <species vars> --export <JSON file out> --dir <optional download folder>

    Example:
    
    $ python run_pipeline_aqmesh.py --species co2 --vars co2 --export aq_mesh.json --dir aqmesh_download/
    """

    parser = argparse.ArgumentParser(
        prog="OpenGHG gather dataset combining tool",
        description="Script to allow the easy concatenation of JSON format datasets into a single JSON file",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", help="input data files", nargs="*", type=str)
    parser.add_argument("--output", help="output data file", type=str)

    args = parser.parse_args()

    infiles = args.input
    outfile = args.output

    combine_networks(data_files=infiles, output_file=outfile)
