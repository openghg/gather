import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

__all__ = ["download"]


def download(url: str, silent: bool = False) -> bytes:
    """Download the data at the given URL. This function tries to be polite
    and tries not to hammer the remote server with requests.

    Args:
        url: URL to csv file
        silent: Print to screen if False
    Returns:
        bytes: Returned content from http request
    """
    if not silent:
        print(f"\nDownloading file from {url}")

    # If we get any of these codes we'll try again
    retriable_status_codes = [
        requests.codes.internal_server_error,
        requests.codes.bad_gateway,
        requests.codes.service_unavailable,
        requests.codes.gateway_timeout,
        requests.codes.too_many_requests,
        requests.codes.request_timeout,
    ]

    retry_strategy = Retry(
        total=3,
        status_forcelist=retriable_status_codes,
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    timeout = 20  # seconds
    data: bytes = http.get(url, timeout=timeout).content

    return data
