from pathlib import Path
from typing import Dict
from webscrape.glasgowpicarro import export_pipeline, process_pipeline


def run_glasgow_picarro(data: bytes, args: Dict) -> Dict:
    """Process the Glasgow Picarro data

    Args:
        data: Binary data
        args: Dictionary of arguments
    Returns:
        dict: Dictionary of combined data
    """
    datapath = Path("/tmp/temp_glasgow_data/latest_data.csv").write_bytes(data)

    process_pipeline(filepath=datapath)
    return export_pipeline()
