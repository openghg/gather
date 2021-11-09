from gather.aqmesh import process_pipeline, scrape_data
from gather.utils import export_pipeline
from openghg.objectstore import get_local_bucket


def test_export(aqmesh_co2_intercept, tmpdir):
    get_local_bucket(empty=True)

    download_path = str(tmpdir)

    species = ["co2"]
    filepaths = scrape_data(species=species, download_path=download_path)
    process_pipeline(extracted_files=filepaths)

    exported_data = export_pipeline(species=["co2"], selected_vars=["co2"])

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

    assert exported_data == expected
