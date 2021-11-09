from pathlib import Path
from gather.pipeline import run_beaco2n
from typing import Dict
import json


def beaco2n(args: bytes) -> Dict:
    """Handle BEACO2N scrape calls

    Args:
        args: Arguents as JSON data
    Returns:
        dict: Dictionary of processed data
    """
    args = json.loads(args)

    beaco2n_args = args["beaco2n"]
    selected_vars = beaco2n_args["selected_vars"]
    download_path = Path("/tmp/beaco2n_download")
    download_path.mkdir(parents=True, exist_ok=True)

    beaco2n_data: Dict = run_beaco2n(selected_vars=selected_vars, download_path=download_path)

    return beaco2n_data
