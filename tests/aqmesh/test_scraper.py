from webscrape.aqmesh import scrape_data
from requests_mock import ANY
# from pandas import Timestamp
from pathlib import Path

@pytest.fixture(scope="session")
def mock_return():
    return {"some": "json"}

def test_retrieve_met(requests_mock):
    test_data_path = Path("../data/aqmesh/test_data.zip")
    binary_data = test_data_path.read_bytes()

    requests_mock.get(ANY, content=binary_data, status_code=200)

    scrape_data()