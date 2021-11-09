from gather.pipeline import run_glasgow_picarro
from helpers import get_datapath
from openghg.objectstore import get_local_bucket


def test_glasgow_pipeline():
    get_local_bucket(empty=True)

    datapath = get_datapath(filename="glasgow-picarro.csv", network="glasgowpicarro")
    raw_data = datapath.read_bytes()

    json_data = run_glasgow_picarro(data=raw_data)

    expected = {
        "npl_picarro": {
            "co2": {
                "gst": {
                    "data": {
                        "co2": {
                            "1633738739000": 417.769,
                            "1633742341000": 415.96,
                            "1633745939000": 416.213,
                        }
                    },
                    "metadata": {
                        "species": "co2",
                        "long_name": "glasgow science centre tower",
                        "latitude": 55.859238,
                        "longitude": -4.29618,
                        "network": "npl_picarro",
                        "inlet": "124m",
                        "sampling_period": "na",
                        "site": "gst",
                        "instrument": "picarro",
                        "units": "ppm",
                        "data_type": "timeseries",
                    },
                }
            },
            "ch4": {
                "gst": {
                    "data": {
                        "ch4": {
                            "1633738739000": 1987.207,
                            "1633742341000": 1973.731,
                            "1633745939000": 1972.547,
                        }
                    },
                    "metadata": {
                        "species": "ch4",
                        "long_name": "glasgow science centre tower",
                        "latitude": 55.859238,
                        "longitude": -4.29618,
                        "network": "npl_picarro",
                        "inlet": "124m",
                        "sampling_period": "na",
                        "site": "gst",
                        "instrument": "picarro",
                        "units": "ppb",
                        "data_type": "timeseries",
                    },
                }
            },
        }
    }

    assert json_data == expected
