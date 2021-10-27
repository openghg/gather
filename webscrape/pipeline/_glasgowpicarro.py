from pathlib import Path
from typing import Dict
from webscrape.glasgowpicarro import export_pipeline, process_pipeline


def run_glasgow_picarro(data: bytes) -> Dict:
    """Process the Glasgow Picarro data

    Args:
        data: Binary data
    Returns:
        dict: Dictionary of combined data
    """
    # TODO - we should just be able to put the bytes into an io buffer and pass that to
    # through really, for now we'll just write to a temporary file
    datapath = Path("/tmp/temp_glasgow_data/latest_data.csv")
    datapath.write_bytes(data)

    process_pipeline(filepath=datapath)
    processed_data = export_pipeline()

    return processed_data
