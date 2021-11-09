import hashlib


def test_scrape(beaco2n_scraper_setup, tmpdir):
    filepaths = beaco2n_scraper_setup

    for node_id, filepath in filepaths.items():
        md5 = hashlib.md5(filepath.read_bytes()).hexdigest()
        assert md5 == "b62cdb3234e6afb87fc3de8605ae1b09"

    assert sorted(filepaths.keys()) == ["157", "174", "175"]
