from pathlib import Path
import json
from typing import Dict, List, Union
from tqdm import tqdm
import zipfile
from io import BytesIO
from collections import defaultdict

from utils.download import download


pathType = Union[str, Path]

__all__ = ["scrape_data"]


def scrape_data(species: List[str], download_path: pathType) -> Dict[str, List]:
    """Download and extract the AQMesh data from their site

    Args:
        species: List of species to download
        download_path
    Returns:
        dict: Dictionary of files extracted for each species
    """
    download_path = Path(download_path).resolve()
    url_data = json.loads(Path("urls.json").read_text())
    # Extract only the URLs we want to download
    selected_urls = {k: v for k, v in url_data.items() if k.upper() in species}

    extracted_files = defaultdict(dict)
    # Here we're download zip files
    for species, url in tqdm(selected_urls.items()):
        zip_bytes = download(url=url)
        # Open the zip file in memory
        zip_file = zipfile.ZipFile(BytesIO(zip_bytes))
        filenames = zip_file.namelist()
        print(f"\nExtracting {filenames} to {download_path}")
        zip_file.extractall(download_path)

        # Extract the data and the metadata filepaths so we can process them more easily
        datafile = next((s for s in filenames if "dataset" in s.lower()), None)
        metadata_file = next((s for s in filenames if "metadata" in s.lower()), None)

        extracted_files[species]["data"] = download_path.joinpath(datafile)
        extracted_files[species]["metadata"] = download_path.joinpath(metadata_file)

    return extracted_files
