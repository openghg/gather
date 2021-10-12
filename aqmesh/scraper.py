from pathlib import Path
import json
from typing import Dict, List, Union

pathType = Union[str, Path]

def scrape_data(species: List[str], download_path: pathType):
    """

    """
    url_data = json.loads(Path("urls.json").read_text())
    download_urls = {k: url_data[k.upper()] for k in url_data}

    # Download, extract and pass CO2 : filepath of extracted data
    # for processing by ObsSurface

    return NotImplementedError()


    


