import argparse
import os
import shutil
import subprocess

def cleanup():
    shutil.rmtree("webscrape")


parser = argparse.ArgumentParser(description="Build the base Docker image and optionally push to DockerHub")
parser.add_argument(
    "--tag",
    dest="tag",
    default="latest",
    type=str,
    help="tag name/number, examples: 1.0 or latest. Not full tag name such as openghg/openghg-complete:latest. Default: latest",
)
parser.add_argument(
    "--push", dest="push", action="store_true", default=False, help="push the image to DockerHub"
)
parser.add_argument(
    "--build",
    dest="build",
    action="store_true",
    default=False,
    help="build the docker image. Disables Fn deploy.",
)
parser.add_argument(
    "--deploy",
    dest="deploy",
    action="store_false",
    default=True,
    help="buid image and deploy the Fn functions",
)

parser.add_argument("--nocache", help="build image without using the cache", action="store_true")

args = parser.parse_args()


try:
    # Copy webscrape to this directory
    shutil.copytree("../webscrape", "webscrape")
except FileExistsError:
    pass

# A tag for the image
tag = args.tag
tag_str = ":".join(("openghg/openghg-pipeline", tag))

# build the file
cmd_str = f"docker build --tag {tag_str} ."

if args.nocache:
    cmd_str += " --no-cache"

cmd_list = cmd_str.split()

try:
    subprocess.check_call(cmd_list)
    print("\nDeploying Fn functions...\n")
    # Make sure we have an app calld openghg
    subprocess.run(["fn", "create", "app", "openghg_pipeline"])
    subprocess.check_call(["fn", "--verbose", "deploy", "--local"])
except subprocess.CalledProcessError:
    cleanup()
    raise

cleanup()