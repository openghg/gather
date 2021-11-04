from gather.beaco2n import parse_metadata
from pathlib import Path
import pytest


def test_metadata():
    test_data_folder = Path(__file__).parent.parent.joinpath("data/beaco2n")
    test_metadata_path = test_data_folder.joinpath("test_metadata.csv")

    parsed = parse_metadata(metadata_filepath=test_metadata_path)

    expected = {
        "killearnstirlingshireglasgows22002": {
            "long_name": "Killearn Stirlingshire GlasgowS22002",
            "id": 156,
            "latitude": 56.043,
            "longitude": -4.381,
            "magl": "NA",
            "masl": "NA",
            "deployed": "2020-03-26",
            "node_folder_id": 873,
        },
        "glasgows12002": {
            "long_name": "GlasgowS12002",
            "id": 157,
            "latitude": 55.826,
            "longitude": -4.226,
            "magl": "NA",
            "masl": "NA",
            "deployed": "2021-01-20",
            "node_folder_id": 872,
        },
    }

    assert parsed == expected

    incorrect_metadata = test_data_folder.joinpath("incorrect_metadata.csv")

    with pytest.raises(ValueError):
        parse_metadata(incorrect_metadata)
