from unittest.mock import patch

from gather.glasgowpicarro import process_pipeline
from helpers import get_datapath, mock_uuid


@patch("uuid.uuid4", mock_uuid().__next__)
def test_process_pipeline():
    datapath = get_datapath(filename="glasgow-picarro.csv", network="glasgowpicarro")
    results = process_pipeline(filepath=datapath)

    expected = {
        "glasgow-picarro.csv": {
            "processed": {
                "glasgow-picarro.csv": {"co2": "test-uuid-1", "ch4": "test-uuid-2"}
            }
        }
    }

    assert results == expected
