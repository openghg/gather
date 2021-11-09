from gather.aqmesh import parse_metadata
from pathlib import Path


def test_metadata():
    metadata_path = Path(__file__).parent.parent.joinpath(
        "data/aqmesh/test_metadata.csv"
    )

    metadata = parse_metadata(filepath=metadata_path)

    assert metadata["briarroadclydebank"] == {
        "site": "briarroadclydebank",
        "pod_id": 11245,
        "start_date": "2021-06-16 01:00:00",
        "end_date": "2021-10-31 23:59:00",
        "relocate_date": "NA",
        "long_name": "Briar Road Clydebank",
        "borough": "Glasgow",
        "site_type": "Roadside",
        "in_ulez": "No",
        "latitude": 55.91796,
        "longitude": -4.406231,
        "inlet": 1,
        "network": "aqmesh_glasgow",
        "sampling_period": "NA",
    }

    assert sorted(metadata.keys()) == [
        "briarroadclydebank",
        "dumbartonroad",
        "stpatricksschool",
        "waulkmillglen",
    ]
