""" This file processes the files downloaded from the BEACO2N site using the get_data.py script

Usage:

$ python process_beaco2n.py data_folder/ glasgow_nodes_parsed.json

This processes all files in data_folder that have matching site names in glasgow_nodes_parsed.json

"""
import argparse
import json
from pathlib import Path
from typing import Dict, Union


pathType = Union[str, Path]

def process_beaco2n(data_path: pathType, json_path: pathType, extension: str = ".csv") -> Dict[str, Dict]:
    """ Helper function to process BEACO2N data scraped from their website.
    This expects data in a CSV format direct from the site. We also require
    a JSON file containing the metadata for each site (see https://github.com/openghg/web-scrape)
    
    """
    from openghg.modules import ObsSurface

    csv_paths = Path(data_path).glob(f"*{extension}")
    site_data = json.loads(Path(json_path).read_text())
    
    # We expect these to have the format 172_STPAULSHIGHSCHOOL.csv
    results = {}
    for filepath in csv_paths:
        filename = filepath.stem
        split = filename.split("_")
        
        site_id = str(split[0])
        site_name = split[1]
        
        # Lookup the site metadata
        site_metadata = site_data[site_name]
        
        site_id_meta = str(site_metadata["id"])
        inlet = site_metadata["magl"]
        # Instrument name taken from http://beacon.berkeley.edu/metadata/
        instrument = "shinyei"

        if site_id != site_id_meta:
            raise ValueError(f"Mismatch between read site ID ({site_id}) and metadata ID ({site_id_meta})")
            
        
        result = ObsSurface.read_file(filepath=filepath, data_type="BEACO2N", 
                                        site=site_name, network="BEACO2N", 
                                      inlet=inlet, instrument=instrument)
        
        results[filename] = result
        
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", help="path to data files", type=str)
    parser.add_argument("json_path", help="path to JSON metadata file", type=str)
    
    args = parser.parse_args()

    data_path = args.data_path
    json_path = args.json_path

    results = process_beaco2n(data_path=data_path, json_path=json_path)

    print(results)

