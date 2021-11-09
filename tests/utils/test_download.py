from gather.utils import download
import hashlib
from helpers import get_datapath


def test_download(requests_mock):
    beaco2n_data = get_datapath(filename="test_data.csv", network="beaco2n")
    binary_data = beaco2n_data.read_bytes()

    mock_url = "https://example.com/some_csv.txt"
    requests_mock.get(
        mock_url,
        content=binary_data,
        status_code=200,
    )

    data = download(url=mock_url)

    md5 = hashlib.md5(data).hexdigest()
    assert md5 == "b62cdb3234e6afb87fc3de8605ae1b09"

    requests_mock.get(
        mock_url,
        status_code=404,
    )

    data = download(url=mock_url)

    assert not data

    requests_mock.get(
        mock_url,
        status_code=666,
    )

    data = download(url=mock_url)

    assert not data
