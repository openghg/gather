from typing import Dict
from gather.pipeline import run_crds


def crds(data: bytes) -> Dict:
    """ Handles the processing of the data from the Killearn Village Hall
    instrument.

    Args:
        data: Measurement data
    Return:
        Dict: Dictionary of processed data
    """
    glasgow_data = run_crds(data=data)

    # TODO - hacky - move this into the processing in OpenGHG
    location_data = {"latitude": 56.0451, "longitude": -4.3724}

    glasgow_data["cop26"]["co2"]["kvh"]["metadata"].update(location_data)
    glasgow_data["cop26"]["ch4"]["kvh"]["metadata"].update(location_data)

    return glasgow_data
