import pytest
from gather.handlers import aqmesh
import gather.handlers._aqmesh as _aqmesh


def test_aqmesh_handler(monkeypatch):
    json_bytes = b'{"aqmesh": {"species": "co2", "selected_vars": ["co2"]}}'

    def mock_aqmesh(species, selected_vars, download_path, sites):
        return {"data": {"some": "data"}}

    monkeypatch.setattr(_aqmesh, "run_aqmesh", mock_aqmesh)

    result = aqmesh(args=json_bytes)

    assert result == {'data': {'some': 'data'}}

    json_bytes = b'123'

    with pytest.raises(TypeError):
        aqmesh(args=json_bytes)
