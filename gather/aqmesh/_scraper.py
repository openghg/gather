from pathlib import Path
from typing import DefaultDict, Dict, List, Union
from tqdm import tqdm
import zipfile
from io import BytesIO
from collections import defaultdict

from gather.utils import download, load_json

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

    if not download_path.exists():
        raise FileNotFoundError(
            f"Download folder {download_path} does not exist, please create it."
        )

    url_data = load_json("aqmesh_urls.json")
    # Extract only the URLs we want to download
    selected_urls = {k.upper(): url_data[k.upper()] for k in species}

    extracted_files: DefaultDict = defaultdict(dict)
    # Here we're download zip files
    for sp, url in tqdm(selected_urls.items()):
        zip_bytes = download(url=url)
        # Open the zip file in memory
        zip_file = zipfile.ZipFile(BytesIO(zip_bytes))
        filenames = zip_file.namelist()
        print(f"\nExtracting {filenames} to {download_path}")
        zip_file.extractall(download_path)

        # Extract the data and the metadata filepaths so we can process them more easily
        datafile: str = next((s for s in filenames if "dataset" in s.lower()))
        metadata_file: str = next((s for s in filenames if "metadata" in s.lower()))

        species_lower = sp.lower()
        extracted_files[species_lower]["data"] = download_path.joinpath(datafile)
        extracted_files[species_lower]["metadata"] = download_path.joinpath(metadata_file)

    return extracted_files
