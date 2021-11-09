from gather.beaco2n import process_beaco2n_pipeline
from unittest.mock import patch
from helpers import load_json, mock_uuid


@patch("uuid.uuid4", mock_uuid().__next__)
def test_process_pipeline(beaco2n_scraper_setup):
    filepaths = beaco2n_scraper_setup

    metadata = load_json(filename="parsed_metadata.json", network="beaco2n")

    results = process_beaco2n_pipeline(filepaths=filepaths, metadata=metadata)

    expected = {
        "175_bellahoustonacademy": {
            "processed": {
                "175_bellahoustonacademy.csv": {
                    "pm": "test-uuid-1",
                    "co": "test-uuid-2",
                    "co2": "test-uuid-3",
                }
            }
        },
        "157_glasgows12002": "No change to data",
        "174_hillparksecondaryschool": "No change to data",
    }

    assert expected == dict(results)
