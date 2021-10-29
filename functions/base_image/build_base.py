import shutil
import subprocess


try:
    # Copy webscrape to this directory
    shutil.copytree("../../webscrape", "webscrape/")
except FileExistsError:
    pass

try:
    tag = "openghg/pipeline-base:latest"
    cmd_str = f"docker build --tag {tag} ."
    subprocess.check_call(cmd_str.split())
except Exception:
    raise
finally:
    shutil.rmtree("webscrape")
