from pathlib import Path


def test_scrape(scraper_setup, tmpdir):
    data = Path(scraper_setup["co2"]["data"])
    metadata = Path(scraper_setup["co2"]["metadata"])

    assert data.exists()
    assert metadata.exists()

    assert data.name == "20210515_20211024_CO2_AQMesh_Scaled_Dataset_PPM.csv"
    assert metadata.name == "20210515_20211024_CO2_pod_metadata.csv"
