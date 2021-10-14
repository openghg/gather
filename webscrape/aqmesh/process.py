from openghg.modules import ObsSurface

def process_pipeline(extracted_files: Dict):
    """ Process the files downloaded and extracted to the download folder

    Args:
        extracted_files: Dictionary of extracted files for each species
    ???
    """
    results = {}

    for species, filepaths in extracted_files.items():
        data_file = filepaths["data"]
        metadata_file = filepaths["metadata"]

        result = ObsSurface.read_multisite_aqmesh(data_filepath=data_file, metadata_filepath=metadata_file)

        results[species] = result

    return results