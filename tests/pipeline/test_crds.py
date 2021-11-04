from gather.pipeline import run_crds
from helpers import get_datapath
from openghg.objectstore import get_local_bucket


def test_crds_pipeline():
    get_local_bucket(empty=True)
    datapath = get_datapath(filename="kvh.picarro.hourly.30m.min.dat", network="crds")
    raw_data = datapath.read_bytes()

    json_data = run_crds(data=raw_data)

    expected = {
        "cop26": {
            "ch4": {
                "kvh": {
                    "data": {
                        "ch4": {"1634656950000": 1979.92, "1634667239000": 1973.73}
                    },
                    "metadata": {
                        "site": "kvh",
                        "instrument": "picarro",
                        "sampling_period": "3600",
                        "inlet": "30m",
                        "port": "0",
                        "type": "air",
                        "network": "cop26",
                        "species": "ch4",
                        "scale": "wmo-x2004a",
                        "long_name": "killearn village hall",
                        "data_type": "timeseries",
                    },
                }
            },
            "co2": {
                "kvh": {
                    "data": {"co2": {"1634656950000": 420.13, "1634667239000": 418.16}},
                    "metadata": {
                        "site": "kvh",
                        "instrument": "picarro",
                        "sampling_period": "3600",
                        "inlet": "30m",
                        "port": "0",
                        "type": "air",
                        "network": "cop26",
                        "species": "co2",
                        "scale": "wmo-x2007",
                        "long_name": "killearn village hall",
                        "data_type": "timeseries",
                    },
                }
            },
        }
    }

    assert json_data == expected
