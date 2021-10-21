from git import Repo
from typing import List

def deploy(filenames: List) -> None:
    """ Deploy data to the data repo

        Args:
            filenames: Filepaths to add to commit and deploy
        Returns:
            None
    """
    # Read the personal token from the secret environment variable
    # Store it to .git-credentials ?
    # Get git config emial 

    # From https://www.appveyor.com/docs/how-to/git-push/
    #       - git config --global credential.helper store
    #   - ps: Set-Content -Path "$HOME\.git-credentials" -Value "https://$($env:access_token):x-oauth-basic@github.com`n" -NoNewline
    #   - git config --global user.email "Your email"
    #   - git config --global user.name "Your Name"
    #   - git commit ...
    #   - git push ...

    # Can we sue GitPython for this?
