from pathlib import Path
from typing import Dict
from gather.glasgowpicarro import process_pipeline
from gather.utils import export_pipeline


def run_glasgow_picarro(data: bytes) -> Dict:
    """Process the Glasgow Picarro data

    Args:
        data: Binary data
    Returns:
        dict: Dictionary of combined data
    """
    # TODO - we should just be able to put the bytes into an io buffer and pass that to
    # through really, for now we'll just write to a temporary file
    datapath = Path("/tmp/glasgow_picarro_latest.csv")
    datapath.write_bytes(data)

    process_pipeline(filepath=datapath)
    processed_data = export_pipeline(species=["co2", "ch4"], sites=["gst"])

    return processed_data
