from unittest.mock import patch

from gather.crds import process_pipeline
from helpers import get_datapath, mock_uuid


@patch("uuid.uuid4", mock_uuid().__next__)
def test_process_pipeline():
    datapath = get_datapath(filename="kvh.picarro.hourly.30m.min.dat", network="crds")
    results = process_pipeline(filepath=datapath)

    expected = {
        "kvh.picarro.hourly.30m.min.dat": {
            "processed": {
                "kvh.picarro.hourly.30m.min.dat": {
                    "ch4": "test-uuid-1",
                    "co2": "test-uuid-2",
                    "co": "test-uuid-3",
                }
            }
        }
    }

    assert results == expected
