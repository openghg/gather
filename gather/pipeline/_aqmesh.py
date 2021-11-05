from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Union, Set

from gather.aqmesh import scrape_data, process_pipeline
from gather.utils import export_pipeline

pathType = Union[str, Path]

__all__ = ["run_aqmesh"]


def run_aqmesh(
    species: Union[str, List],
    selected_vars: List = None,
    download_path: pathType = None,
    sites: List = None,
) -> Dict:
    """Run the whole processing pipeline

    Args:
        species: List of species to process
        selected_vars: Variables from data we want to export
        export_filepath: Path to write dashboard data
        download_path: Output directory for processed
        sites: List of sites to export
    Returns:
        dict: Dictionary of network data
    """
    if not isinstance(species, list):
        species = [species]

    if selected_vars is None:
        selected_vars = species

    if download_path is None:
        tmpdir = TemporaryDirectory()
        download_path = tmpdir.name

    file_list = scrape_data(species=species, download_path=download_path)
    processing_results = process_pipeline(extracted_files=file_list)

    # Not all sites might have measurements for each species
    all_sites: Set = set()
    for species, site_data in processing_results.items():
        all_sites.update(site_data.keys())

    if sites is not None:
        sites = [s.lower() for s in sites]
        all_sites = all_sites.intersection(sites)

    site_list = list(all_sites)

    json_data: Dict = export_pipeline(
        species=species, selected_vars=selected_vars, sites=site_list
    )

    try:
        tmpdir.cleanup()
    except (NameError, AttributeError):
        pass

    return json_data
