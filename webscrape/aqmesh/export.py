from typing import List, Dict, Union
from pathlib import Path
from openghg.processing import search
from openghg.util import to_dashboard
import json

__all__ = ["export_pipeline", "export"]

pathType = Union[str, Path]


def export_pipeline(
    species: Union[str, List],
    selected_vars: List[str],
    sites: List[str] = None,
) -> Dict:
    """Retrieve data from the object store and export it to JSON. Pipeline version that
    expects site metadata as a dict instead of a filepath to JSON.

    Args:
        species: List of species to search for
        selected_vars: Variables to extract from data such as speices names, e.g. ["co2", "co", "pm"]
        sites: Site list, use if you only want specific site data output
    Returns:
        dict: Dictionary of processed data in JSON format
    """
    if not isinstance(species, list):
        species = [species]

    results = search(species=species, site=sites)

    if not results:
        raise ValueError(
            "Unable to find any data for the given sites. Make sure you've processed the correct data."
        )

    data = results.retrieve_all()

    json_data = to_dashboard(data=data, selected_vars=selected_vars)

    return json_data


def export(
    species: Union[str, List],
    selected_vars: List[str],
    output_filepath: str,
    sites: List[str] = None,
) -> None:
    """Retrieve data from the object store and export it to JSON.

    Args:
        species: List of species to export
        selected_vars: Variables to extract from data such as speices names, e.g. ["co2", "co", "pm"]
        output_filepath: Filepath for writing data, if not given data will be written to dashboard_data.json
        sites: Site list
    Returns:
        None
    """
    json_data = export_pipeline(
        selected_vars=selected_vars,
        species=species,
        sites=sites,
    )

    with open(output_filepath, "w") as f:
        json.dump(json_data, f)

    print(f"Data written to {output_filepath}")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("species", help="species to export", type=str)
#     parser.add_argument(
#         "vars",
#         help="variables to extract from DataFrame e.g. co2",
#         nargs="*",
#         type=str,
#     )
#     parser.add_argument(
#         "outfile", help="filename for JSON data, if not given data is written to dashboard_data.json"
#     )
#     parser.add_argument(
#         "--species", help=""
#     )

#     args = parser.parse_args()

#     sites = args.sites
#     selected_vars = args.vars
#     outfile = args.outfile
#     species = args.species

#     export
