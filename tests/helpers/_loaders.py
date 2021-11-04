from pathlib import Path
import json


def get_datapath(filename: str, network: str):
    return Path(__file__).parent.parent.joinpath(f"data/{network}/{filename}")


def load_json(filename: str, network: str):
    test_path = get_datapath(filename=filename, network=network)

    with open(test_path, "r") as f:
        data = json.load(f)

    return data
