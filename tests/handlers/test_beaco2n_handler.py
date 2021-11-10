import pytest
from gather.handlers import beaco2n
import gather.handlers._beaco2n as _beaco2n


def test_aqmesh_handler(monkeypatch):
    json_bytes = b'{"beaco2n": {"selected_vars": ["co2"]}}'

    def mock_beaco2n(selected_vars, download_path):
        return {"data": {"some": "data"}}

    monkeypatch.setattr(_beaco2n, "run_beaco2n", mock_beaco2n)

    result = beaco2n(args=json_bytes)

    assert result == {'data': {'some': 'data'}}

    json_bytes = b'123'

    with pytest.raises(TypeError):
        beaco2n(args=json_bytes)
