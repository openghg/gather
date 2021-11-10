import pytest
from gather.handlers import crds
from addict import Dict as aDict
import gather.handlers._crds as _crds


def test_crds_handler(monkeypatch):
    def mock_crds(data):
        d = aDict()
        d["cop26"]["co2"]["kvh"] = {"data": 123, "metadata": {"site": "kvh"}}
        d["cop26"]["ch4"]["kvh"] = {"data": 123, "metadata": {"site": "kvh"}}

        return d.to_dict()

    monkeypatch.setattr(_crds, "run_crds", mock_crds)

    result = crds(data="data")

    expected = {
        "cop26": {
            "co2": {
                "kvh": {
                    "data": 123,
                    "metadata": {
                        "site": "kvh",
                        "latitude": 56.0451,
                        "longitude": -4.3724,
                    },
                }
            },
            "ch4": {
                "kvh": {
                    "data": 123,
                    "metadata": {
                        "site": "kvh",
                        "latitude": 56.0451,
                        "longitude": -4.3724,
                    },
                }
            },
        }
    }

    assert result == expected

