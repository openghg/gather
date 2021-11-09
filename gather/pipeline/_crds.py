from pathlib import Path
from typing import Dict
from gather.crds import process_pipeline
from gather.utils import export_pipeline


__all__ = ["run_crds"]


def run_crds(data: bytes) -> Dict:
    """Process the Glasgow Picarro data

    Args:
        data: Binary data
    Returns:
        dict: Dictionary of combined data
    """
    # TODO - we should just be able to put the bytes into an io buffer and pass that to
    # through really, for now we'll just write to a temporary file
    datapath = Path("/tmp/kvh.picarro.hourly.30m.dat")
    datapath.write_bytes(data)

    process_pipeline(filepath=datapath)
    processed_data = export_pipeline(species=["ch4", "co2"], sites=["kvh"])

    return processed_data
