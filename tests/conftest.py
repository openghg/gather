import sys
import os
import shutil
import tempfile
import pytest
from requests_mock import ANY
from pathlib import Path


from gather.aqmesh import scrape_data as aqmesh_scraper
from gather.beaco2n import scrape_data_pipeline as beaco2n_scraper

sys.path.insert(0, "..")


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


#  Fixtures used around the test suite


@pytest.fixture()
def aqmesh_co2_intercept(requests_mock):
    test_data_path = Path(__file__).parent.joinpath("data/aqmesh/test_data.zip")
    binary_data = test_data_path.read_bytes()

    requests_mock.get(
        "https://breathelondon.net/data/NERCBreatheLondonContinuation/Glasgow_AQmesh_CO2.zip",
        content=binary_data,
        status_code=200,
    )


@pytest.fixture
def aqmesh_scraper_setup(aqmesh_co2_intercept, tmpdir):
    download_path = str(tmpdir)

    species = ["co2"]
    return aqmesh_scraper(species=species, download_path=download_path)


@pytest.fixture
def beaco2n_intercept(requests_mock):
    test_data_folder = Path(__file__).parent.joinpath("data/beaco2n")
    test_data_path = test_data_folder.joinpath("test_data.csv")
    binary_data = test_data_path.read_bytes()

    requests_mock.get(
        ANY,
        content=binary_data,
        status_code=200,
    )

@pytest.fixture
def beaco2n_scraper_setup(beaco2n_intercept, tmpdir):
    download_path = str(tmpdir)

    test_data_folder = Path(__file__).parent.joinpath("data/beaco2n")
    metadata_filepath = test_data_folder.joinpath("test_metadata.csv")

    return beaco2n_scraper(metadata=metadata_filepath, download_path=download_path)
