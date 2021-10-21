from io import BytesIO
from fdk.context import InvokeContext
from fdk.response import Response
from importlib import import_module
from typing import Dict
from traceback import format_exc
from webscrape.pipeline import run_aqmesh, run_beaco2n
from datetime import datetime
import json
from pathlib import Path


async def handle_invocation(ctx: InvokeContext, data: BytesIO) -> Response:
    """The endpoint for the function. This handles the POST request and passes it through
    to the handler

    Note: this handler should only be used for testing purposes. All function calls
    in a production system should go though Acquire so that data is encrypted in transit.

    Args:
        ctx: Invoke context. This is passed by Fn to the function
        data: Data passed to the function by the user
    Returns:
        dict: Dictionary of return data
    """

    try:
        post_data = json.loads(data.getvalue())
    except Exception:
        error_str = str(format_exc())
        return Response(ctx=ctx, response_data=error_str)

    result = {}

    try:
        aqmesh_args = post_data["aqmesh"]
        species = aqmesh_args["species"]
        selected_vars = aqmesh_args["selected_vars"]

        download_path = Path("/tmp/aqmesh_download")
        download_path.mkdir(parents=True, exist_ok=True)
        export_filepath = download_path.joinpath("aqmesh_data.json")

        sites = aqmesh_args.get("sites")

        run_aqmesh(
            species=species,
            selected_vars=selected_vars,
            export_filepath=export_filepath,
            download_path=download_path,
            sites=sites,
        )

        json_data = Path(export_filepath).read_text()

        # Do something with the exported data
        result["aqmesh"] = json_data
    except Exception:
        error_str = str(format_exc())
        result["aqmesh"] = f"Did not run - {error_str}"

    try:
        beaco2n_args = post_data["beaco2n"]

        selected_vars = beaco2n_args["selected_vars"]
        export_filepath = "beaco2n_data.json"

        run_beaco2n(selected_vars=selected_vars, export_filepath=export_filepath)
        # Do something with the exported data
        result["beaco2n"] = datas
    except Exception:
        error_str = str(format_exc())
        result["beaco2n"] = f"Did not run - {error_str}"

    # Now we combine the data and push to the repo
    

    headers = {"Content-Type": "application/octet-stream"}
    return Response(ctx=ctx, response_data=result, headers=headers)
