from pathlib import Path
from gather.pipeline import run_aqmesh
from typing import Dict
import json


def aqmesh(args: bytes) -> Dict:
    """Download and process the AQMesh data

    Args:
        data: Arguments as JSON data
    Returns:
        dict: Dictionary of processed data
    """
    args = json.loads(args)

    aqmesh_args = args["aqmesh"]
    species = aqmesh_args["species"]
    selected_vars = aqmesh_args["selected_vars"]

    download_path = Path("/tmp/aqmesh_download")
    download_path.mkdir(parents=True, exist_ok=True)

    sites = aqmesh_args.get("sites")

    aqmesh_data: Dict = run_aqmesh(
        species=species,
        selected_vars=selected_vars,
        download_path=download_path,
        sites=sites,
    )

    return aqmesh_data
