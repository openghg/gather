__all__ = ["handler"]

from typing import Dict
from pathlib import Path
from pandas import Timestamp
from git import Repo
from traceback import format_exc
import os
import json


def handler(args: Dict):
    """Handles the calling of the pipeline functions

    Args:
        args: Dictionary of arguments
    Returns:
        Dict: Dictionary of results of processing
    """
    from webscrape.pipeline import run_aqmesh, run_beaco2n, run_glasgow_picarro

    # Clone the repo and read in the data, this means we'll just update
    # the data that's processed correctly.
    repo_path = Path("/tmp/dashboard_data")
    repo_path.mkdir()

    git_token = os.environ["GIT_TOKEN"]
    remote_url = f"https://{git_token}:x-oauth-basic@github.com/openghg/dashboard_data"
    repo = Repo.clone_from(remote_url, repo_path, branch="main")

    # Read and load the old data so we can just update it if one of the
    # pipelines below fails
    combined_data_path = repo_path.joinpath("combined_data.json")
    old_combined_data = json.loads(combined_data_path.read_text())

    result = {}
    successes = {}
    combined_data = {}
    try:
        aqmesh_args = args["aqmesh"]
        species = aqmesh_args["species"]
        selected_vars = aqmesh_args["selected_vars"]

        download_path = Path("/tmp/aqmesh_download")
        download_path.mkdir(parents=True, exist_ok=True)

        sites = aqmesh_args.get("sites")

        aqmesh_data = run_aqmesh(
            species=species,
            selected_vars=selected_vars,
            download_path=download_path,
            sites=sites,
        )

        combined_data.update(aqmesh_data)

        # Do something with the exported data
        now_str = str(Timestamp.now())
        result["aqmesh"] = f"AQMesh run success at - {now_str}"
        successes["aqmesh"] = True
    except Exception:
        error_str = str(format_exc())
        result["aqmesh"] = f"Did not run - {error_str}"
        successes["aqmesh"] = False

    try:
        beaco2n_args = args["beaco2n"]
        selected_vars = beaco2n_args["selected_vars"]
        download_path = Path("/tmp/beaco2n_download")
        download_path.mkdir(parents=True, exist_ok=True)

        beaco2n_data = run_beaco2n(
            selected_vars=selected_vars, download_path=download_path
        )
        combined_data.update(beaco2n_data)
        # Do something with the exported data
        now_str = str(Timestamp.now())
        result["beaco2n"] = f"BEACO2N run success at - {now_str}"
        successes["beaco2n"] = True
    except Exception:
        error_str = str(format_exc())
        result["beaco2n"] = f"Did not run - {error_str}"
        successes["beaco2n"] = False

    # Glasgow Science Tower Picarro
    try:
        glasgow_args = args["glasgow_picarro"]
        # Binary (?) data
        raw_data = glasgow_args["data"]

        glasgow_data = run_glasgow_picarro(data=raw_data, args={})
        combined_data.update(glasgow_data)

        now_str = str(Timestamp.now())
        result["glasgow_picarro"] = f"Glasgow Picarro run success at - {now_str}"
    except Exception:
        error_str = str(format_exc())
        result["glasgow_picarro"] = f"Did not run - {error_str}"
        successes["glasgow_picarro"] = False

    # Update the old data with the newly processed data
    old_combined_data.update(combined_data)

    # Write the file for commit
    export_filepath = repo_path.joinpath("combined_data.json")
    export_filepath.write_text(json.dumps(old_combined_data))

    # The list of files we want to add in this commit
    file_list = [str(export_filepath)]

    # Now we do the commit
    commit_str = ", ".join([n for n, v in successes.items() if v])
    commit_time = str(Timestamp.now())
    commit_message = f"Automated commit of {commit_str} data at {commit_time}"

    try:
        repo.index.add(file_list)
        repo.index.commit(commit_message)
        origin = repo.remote("origin")
        origin.push()
        result["commit"] = commit_message
    except Exception:
        result["commit"] = str(format_exc())

    return result
