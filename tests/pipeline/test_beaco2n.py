import json
from types import MethodDescriptorType
from gather.pipeline import run_beaco2n
from pathlib import Path
from openghg.objectstore import get_local_bucket

import gather.pipeline._beaco2n as _beaco2n_pipeline


def test_beaco2n_pipeline(tmpdir, monkeypatch):
    def mock_scrape(metadata, download_path):
        return {m: f"/tmp/this/{m}" for m in metadata}

    def mock_process(filepaths, metadata):
        return None

    def mock_export(sites, selected_vars):
        return {
            "network": {
                "species": {
                    "hillparksecondaryschool": {
                        "data": {"2021-01-01": 432},
                        "metadata": {"location": "glasgow"},
                    }
                }
            }
        }

    monkeypatch.setattr(_beaco2n_pipeline, "scrape_data_pipeline", mock_scrape)
    monkeypatch.setattr(_beaco2n_pipeline, "process_beaco2n_pipeline", mock_process)
    monkeypatch.setattr(_beaco2n_pipeline, "export_pipeline", mock_export)

    download_directory = Path(str(tmpdir))

    json_data = run_beaco2n(selected_vars=["co2"], download_path=download_directory)

    expected = {
        "network": {
            "species": {
                "hillparksecondaryschool": {
                    "data": {"2021-01-01": 432},
                    "metadata": {
                        "location": "glasgow",
                        "deployed": "2021-07-28",
                        "id": 174,
                        "latitude": 55.815,
                        "long_name": "Hillpark Secondary School",
                        "longitude": -4.299,
                        "magl": "NA",
                        "masl": "NA",
                        "node_folder_id": 931,
                    },
                }
            }
        }
    }

    assert json_data == expected
