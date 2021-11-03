from addict import Dict as aDict
from pathlib import Path
from typing import Dict, Union
from pandas import read_csv
from openghg.util import is_date

__all__ = ["parse_metadata"]

pathType = Union[str, Path]


def parse_metadata(filepath: pathType) -> Dict:
    """Parse AQMesh metadata

    Args:
        filepath: Path to metadata CSV
        pipeline: If running in pipeline skip the writing of metadata to file
    Returns:
        dict: Dictionary of metadata
    """

    filepath = Path(filepath)
    raw_metadata = read_csv(filepath)

    site_metadata = aDict()

    for index, row in raw_metadata.iterrows():
        site_name = row["location_name"].replace(" ", "").lower()
        site_data = site_metadata[site_name]

        site_data["site"] = site_name
        site_data["pod_id"] = row["pod_id_location"]
        site_data["start_date"] = is_date(row["start_date_UTC"])
        site_data["end_date"] = is_date(row["end_date_UTC"])
        site_data["relocate_date"] = is_date(row["relocate_date_UTC"])
        site_data["long_name"] = row["location_name"]
        site_data["borough"] = row["Borough"]
        site_data["site_type"] = row["Type"]
        site_data["in_ulez"] = row["ULEZ"]
        site_data["latitude"] = row["Latitude"]
        site_data["longitude"] = row["Longitude"]
        site_data["inlet"] = row["Height"]
        site_data["network"] = "aqmesh_glasgow"
        site_data["sampling_period"] = "NA"

    site_metadata = site_metadata.to_dict()

    return site_metadata
