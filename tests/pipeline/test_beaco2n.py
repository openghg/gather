from gather.pipeline import run_beaco2n
from pathlib import Path
from openghg.objectstore import get_local_bucket


def test_beaco2n_pipeline(beaco2n_intercept, tmpdir):
    get_local_bucket(empty=True)

    download_directory = Path(str(tmpdir))

    json_data = run_beaco2n(selected_vars=["co2"], download_path=download_directory)

    expected_data = {
        "beaco2n": {
            "co2": {
                "bellahoustonacademy": {
                    "data": {"co2": {"1635382800000": 447.6, "1635393600000": 476.6}},
                    "metadata": {
                        "units": "ppm",
                        "site": "bellahoustonacademy",
                        "species": "co2",
                        "inlet": "na",
                        "network": "beaco2n",
                        "sampling_period": "not_set",
                        "data_type": "timeseries",
                        "deployed": "2021-07-15",
                        "id": 175,
                        "latitude": 55.848,
                        "long_name": "Bellahouston Academy",
                        "longitude": -4.301,
                        "magl": "NA",
                        "masl": "NA",
                        "node_folder_id": 932,
                    },
                }
            }
        }
    }

    filenames = sorted([f.stem for f in download_directory.glob("*.csv")])

    assert filenames == [
        "156_killearnstirlingshireglasgows22002",
        "157_glasgows12002",
        "171_universityofstrathclyde",
        "172_stpaulshighschool",
        "174_hillparksecondaryschool",
        "175_bellahoustonacademy",
        "178_stthomasaquinasrcsecondaryschool",
        "179_johnpaulacademy",
        "193_knightswoodsecondary",
        "197_notredamehighschool",
    ]

    assert json_data == expected_data
