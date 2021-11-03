from requests_mock import ANY
from pathlib import Path
import pytest
import os
import tempfile
import shutil

from gather.aqmesh import scrape_data


def pytest_sessionstart(session):
    """Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    # Save the old OpenGHG object store environment variable if there is one
    old_path = os.environ.get("OPENGHG_PATH")

    if old_path is not None:
        os.environ["OPENGHG_PATH_BAK"] = old_path

    os.environ["OPENGHG_PATH"] = str(tempfile.TemporaryDirectory().name)


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished, right before
    returning the exit status to the system.
    """
    temp_path = os.environ["OPENGHG_PATH"]
    # Delete the testing object store
    try:
        shutil.rmtree(temp_path)
    except FileNotFoundError:
        pass

    # Set the environment variable back
    try:
        os.environ["OPENGHG_PATH"] = os.environ["OPENGHG_PATH_BAK"]
        del os.environ["OPENGHG_PATH_BAK"]
    except KeyError:
        pass


@pytest.fixture()
def aqmesh_co2_intercept(requests_mock):
    test_data_path = Path(__file__).parent.parent.joinpath("data/aqmesh/test_data.zip")
    binary_data = test_data_path.read_bytes()

    requests_mock.get(ANY, content=binary_data, status_code=200)


@pytest.fixture
def scraper_setup(aqmesh_co2_intercept, tmpdir):
    download_path = str(tmpdir)

    species = ["co2"]
    return scrape_data(species=species, download_path=download_path)
