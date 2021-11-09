import argparse
import shutil
import subprocess


def cleanup():
    shutil.rmtree("./base_image/gather")


parser = argparse.ArgumentParser(
    description="Build the base Docker image and optionally push to DockerHub"
)
parser.add_argument(
    "--tag",
    dest="tag",
    default="latest",
    type=str,
    help="tag name/number, examples: 1.0 or latest. Not full tag name such as openghg/openghg-complete:latest. Default: latest",
)
parser.add_argument(
    "--push",
    dest="push",
    action="store_true",
    default=False,
    help="push the image to DockerHub",
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

parser.add_argument(
    "--nocache", help="build image without using the cache", action="store_true"
)

args = parser.parse_args()


try:
    # Copy gather to this directory
    shutil.copytree("../gather", "./base_image/gather")
except FileExistsError:
    pass

# A tag for the image
tag = args.tag

# build the file
base_cmd = f"docker build --tag openghg/pipeline-base:{tag} ."

# The functions we want to setup
functions = ["aqmesh", "beaco2n", "picarro", "crds"]

if args.nocache:
    base_cmd += " --no-cache"

try:
    # Build the base image first
    subprocess.check_call(base_cmd.split(), cwd="./base_image")

    for func in functions:
        cmd = f"docker build --tag openghg/{func}-fn:{tag} ."
        subprocess.check_call(cmd.split(), cwd="./{function}")

    print("\nDeploying Fn functions...\n")

    app_name = "openghg_pipeline"

    # Make sure we have an app called openghg
    subprocess.run(["fn", "create", "app", app_name])

    deploy_cmd = ["fn", "--verbose", "deploy", "--app", app_name, "--local"]

    for func in functions:
        subprocess.check_call(deploy_cmd, cwd=f"./{func}")

except subprocess.CalledProcessError as e:
    print(f"Error - {str(e)}")
finally:
    cleanup()
