from git import Repo
from typing import List

def deploy(filenames: List) -> None:
    """ Deploy data to the data repo

        Args:
            filenames: Filepaths to add to commit and deploy
        Returns:
            None
    """
    repo_url = "git@github.com:openghg/dashboard_data.git"
    to_path = "/tmp"
    try:
        Repo.clone_from("git@github.com:openghg/dashboard_data.git", to_path=to_path)





PATH_OF_GIT_REPO = r'path\to\your\project\folder\.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'comment from python script'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()

