from typing import Dict
from openghg.modules import ObsSurface


def process_pipeline(extracted_files: Dict) -> Dict[str, Dict]:
    """Process the files downloaded and extracted to the download folder

    Args:
        extracted_files: Dictionary of extracted files for each species
    Returns:
        dict: Dictionary of processing results
    """
    results = {}

    for species, filepaths in extracted_files.items():
        data_file = filepaths["data"]
        metadata_file = filepaths["metadata"]

        result = ObsSurface.read_multisite_aqmesh(
            data_filepath=data_file, metadata_filepath=metadata_file, overwrite=True
        )

        results[species] = result

    return results
