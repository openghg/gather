import json
from gather.pipeline import run_aqmesh
from pathlib import Path

import gather.pipeline._aqmesh as _aqmesh_pipeline


def test_aqmesh_pipeline(monkeypatch, tmpdir):
    def mock_scrape(species, download_path):
        return {m: f"/tmp/this/{m}" for m in range(4)}

    def mock_process(extracted_files):
        sites = [f"glasgow_{n}" for n in range(4)]
        spec = {"co2": "uuid-123"}
        return {s: spec for s in sites}

    def mock_export(species, selected_vars, sites):
        return {
            "network": {
                "species": {
                    "glasgow_1": {
                        "data": {"2021-01-01": 432},
                        "metadata": {"location": "glasgow"},
                    }
                }
            }
        }

    monkeypatch.setattr(_aqmesh_pipeline, "scrape_data", mock_scrape)
    monkeypatch.setattr(_aqmesh_pipeline, "process_pipeline", mock_process)
    monkeypatch.setattr(_aqmesh_pipeline, "export_pipeline", mock_export)

    download_directory = Path(str(tmpdir))

    json_data = run_aqmesh(
        species="co2", selected_vars="co2", download_path=download_directory
    )

    expected = {
        "network": {
            "species": {
                "glasgow_1": {
                    "data": {"2021-01-01": 432},
                    "metadata": {"location": "glasgow"},
                }
            }
        }
    }

    assert json_data == expected

    print(json_data)

    return

    expected = {
        "aqmesh_glasgow": {
            "co2": {
                "briarroadclydebank": {
                    "data": {
                        "co2": {
                            "1623805200000": 413.76,
                            "1623816000000": 413.37,
                            "1623826800000": 405.4,
                        }
                    },
                    "metadata": {
                        "site": "briarroadclydebank",
                        "pod_id": 11245,
                        "start_date": "2021-06-16 01:00:00",
                        "end_date": "2021-10-25 00:59:00",
                        "relocate_date": "na",
                        "long_name": "briar road clydebank",
                        "borough": "glasgow",
                        "site_type": "roadside",
                        "in_ulez": "no",
                        "latitude": 55.91796,
                        "longitude": -4.406231,
                        "inlet": 1,
                        "network": "aqmesh_glasgow",
                        "sampling_period": "na",
                        "species": "co2",
                        "units": "ppm",
                        "data_type": "timeseries",
                    },
                }
            }
        }
    }

    filenames = sorted([f.stem for f in download_directory.glob("*.csv")])

    assert filenames == [
        "20210515_20211024_CO2_AQMesh_Scaled_Dataset_PPM",
        "20210515_20211024_CO2_pod_metadata",
    ]

    assert json_data == expected
