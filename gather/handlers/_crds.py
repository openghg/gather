from typing import Dict
from pathlib import Path
from pandas import Timestamp
from git import Repo
from traceback import format_exc
import os
import json

from gather.pipeline import run_crds

__all__ = ["crds_handler"]


def crds_handler(data: bytes) -> Dict:
    """Handle binary data being curled to our endpoint"""
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

    combined_data = {}
    result = {}
    # Glasgow Science Tower Picarro
    try:
        # We just expect Glasgow data for now
        glasgow_data = run_crds(data=data)

        # TODO - hacky - move this into the processing
        location_data = {"latitude": 56.0451, "longitude": -4.3724}

        glasgow_data["cop26"]["co2"]["kvh"]["metadata"].update(location_data)
        glasgow_data["cop26"]["ch4"]["kvh"]["metadata"].update(location_data)

        combined_data.update(glasgow_data)

        now_str = str(Timestamp.now())
        result["glasgow_picarro"] = f"KVH run success at - {now_str}"
    except Exception:
        error_str = str(format_exc())
        result["glasgow_picarro"] = f"Did not run - {error_str}"

    # Update the old data with the newly processed data
    old_combined_data.update(combined_data)

    # Write the file for commit
    export_filepath = repo_path.joinpath("combined_data.json")
    export_filepath.write_text(json.dumps(old_combined_data))

    # The list of files we want to add in this commit
    file_list = [str(export_filepath)]

    # Now we do the commit
    commit_time = str(Timestamp.now())
    commit_message = (
        f"Automated commit of Killearn Village Hall data at {commit_time}"
    )

    try:
        repo.index.add(file_list)
        repo.index.commit(commit_message)
        origin = repo.remote("origin")
        origin.push()
        result["commit"] = commit_message
    except Exception:
        result["commit"] = str(format_exc())

    return result
