"""
This script extracts the site data available in the CSV located at
http://beacon.berkeley.edu/get_latest_nodes/csv/

To use:

$ python extract_site_data.py get_latest_nodes.csv

Will create a file called

get_latest_nodes_parsed.json

Or for other files with the same schema

$ python extract_site_data.py <filepath_to_csv>

"""
import json
import pandas as pd
from collections import defaultdict
import math
import argparse
import numpy as np
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="path of file to parse", type=str)
args = parser.parse_args()

filepath = Path(args.filepath)
output_filepath = f"{str(filepath.stem)}_parsed.json"

site_data = pd.read_csv(filepath)


def date_or_not(date):
    """Functional but pretty limited"""
    try:
        d = pd.Timestamp(date)
        if pd.isnull(d):
            return "NA"

        return date
    except ValueError:
        return "NA"


def nan_or_not(data):
    try:
        if math.isnan(data):
            return "NA"
        else:
            return round(data, 3)
    except TypeError as e:
        print(data, e)


site_dict = defaultdict(dict)

for index, row in site_data.iterrows():
    node_name = row["node_name_long"].upper().replace(" ", "")

    site_dict[node_name]["long_name"] = row["node_name_long"]
    site_dict[node_name]["id"] = row["id"]
    site_dict[node_name]["latitude"] = round(row["lat"], 5)
    site_dict[node_name]["longitude"] = round(row["lng"], 5)
    site_dict[node_name]["magl"] = nan_or_not(row["height_above_ground"])
    site_dict[node_name]["masl"] = nan_or_not(row["height_above_sea"])
    site_dict[node_name]["deployed"] = date_or_not(row["deployed"])
    site_dict[node_name]["node_folder_id"] = row["node_folder_id"]


with open(output_filepath, "w") as f:
    json.dump(site_dict, f, sort_keys=True, indent=4)
