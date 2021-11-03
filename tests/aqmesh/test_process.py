from gather.aqmesh import process_pipeline
import pytest
import uuid


@pytest.fixture
def mock_uuid(monkeypatch):
    def mock_uuid():
        return "123-123-123"

    monkeypatch.setattr(uuid, "uuid4", mock_uuid)


def test_process(scraper_setup, tmpdir, mock_uuid):
    datapaths = scraper_setup

    res = process_pipeline(extracted_files=datapaths)

    expected = {'co2': {'briarroadclydebank': {'briarroadclydebank': '123-123-123'}}}

    assert res == expected
