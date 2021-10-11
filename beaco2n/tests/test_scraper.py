import pytest
import requests_mock
import requests
from requests_mock import ANY
from beaco2n import scrape_data


# @requests_mock.Mocker()
# ... def test_func(m):
# ...     m.get('http://test.com', text='data')
# ...     return requests.get('http://test.com').text

def test_scraper(requests_mock):
    # m.get(ANY, text='data')
    requests_mock.get('http://test.com', text='data')
    assert 'data' == requests.get('http://test.com').text

    


    # First we need to get some metadata
    # Then mock the requests
    # Mock data for requests to return
    # Make sure the data is written to the correct path

