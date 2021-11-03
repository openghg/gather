import hashlib


def test_scrape(beaco2n_scraper_setup, tmpdir):
    filepaths = beaco2n_scraper_setup

    bellahouston_filepath = filepaths["175"]
    filename = bellahouston_filepath.name

    assert filename == "175_bellahoustonacademy.csv"

    md5 = hashlib.md5(bellahouston_filepath.read_bytes()).hexdigest()

    assert md5 == "b62cdb3234e6afb87fc3de8605ae1b09"
