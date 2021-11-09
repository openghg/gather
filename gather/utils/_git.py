from pathlib import Path
from git import Repo
import os
import json
import tempfile
from typing import Dict


def git_commit(repo_url: str, processed_data: Dict, commit_msg: str) -> None:
    """Commit the newly processed data to the repository

    Args:
        repo_path: Repository hostname i.e. github.com/openghg/dashboard_data
        processed_data: Data to commit
        commit_msg: Commit message
    Returns:
        None
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo and read in the data, this means we'll just update
        # the data that's processed correctly.
        repo_path = Path(tmpdir.name)
        repo_url = "github.com/openghg/dashboard_data"

        git_token = os.environ["GIT_TOKEN"]
        remote_url = f"https://{git_token}:x-oauth-basic@{repo_url}"
        repo = Repo.clone_from(remote_url, repo_path, branch="main")

        # Read and load the old data so we can just update it if one of the
        # pipelines below fails
        combined_data_path = repo_path.joinpath("combined_data.json")
        old_combined_data = json.loads(combined_data_path.read_text())

        # Update the old data with the newly processed data
        old_combined_data.update(processed_data)

        # Write the file for commit
        export_filepath = repo_path.joinpath("combined_data.json")
        export_filepath.write_text(json.dumps(old_combined_data))

        # The list of files we want to add in this commit
        file_list = [str(export_filepath)]

        changed_files = [item.a_path for item in repo.index.diff(None)]
        # Check if anything has changed
        if changed_files:
            repo.index.add(file_list)
            repo.index.commit(commit_msg)
            origin = repo.remote("origin")
            origin.push()
