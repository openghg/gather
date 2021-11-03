import shutil
import subprocess


try:
    # Copy gather to this directory
    shutil.copytree("../../gather", "gather/")
except FileExistsError:
    pass

try:
    tag = "openghg/pipeline-base:latest"
    cmd_str = f"docker build --tag {tag} ."
    subprocess.check_call(cmd_str.split())
except Exception:
    raise
finally:
    shutil.rmtree("gather")
