from openghg.processing import search
from openghg.util import to_dashboard
from pathlib import Path
from typing import Dict, List, Union


pathType = Union[str, Path]

__all__ = ["export_pipeline"]


def export_pipeline(
    selected_vars: List[str] = ["co2", "ch4"],
    species: List[str] = ["co2", "ch4"],
) -> Dict:
    """Retrieve data from the object store and export it to JSON. Pipeline version that
    expects site metadata as a dict instead of a filepath to JSON.

    Args:
        sites: Site names
        selected_vars: Variables to extract from data such as speices names, e.g. ["co2", "co", "pm"]
        species: List of species to search for, use may speed up data retrieval.
    Returns:
        dict: Dictionary of processed data in JSON format
    """
    results = search(site="kvh", species=species)

    if not results:
        raise ValueError(
            "Unable to find any data for the given sites. Make sure you've processed the correct data."
        )

    data = results.retrieve_all()

    json_data = to_dashboard(data=data, selected_vars=selected_vars)

    return json_data
