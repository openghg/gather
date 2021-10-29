import argparse
import shutil
import subprocess


def cleanup():
    shutil.rmtree("./base_image/webscrape")


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
    # Copy webscrape to this directory
    shutil.copytree("../webscrape", "./base_image/webscrape")
except FileExistsError:
    pass

# A tag for the image
tag = args.tag
tag_str = ":".join(("openghg/pipeline-base", tag))

# build the file
cmd_str = f"docker build --tag {tag_str} ."
scrape_cmd_str = "docker build --tag openghg/scrape-fn:latest ."
picarro_cmd_str = "docker build --tag openghg/picarro-fn:latest ."

if args.nocache:
    cmd_str += " --no-cache"

base_cmd_list = cmd_str.split()
scrape_cmd_list = scrape_cmd_str.split()
picarro_cmd_list = picarro_cmd_str.split()

try:
    # Build the base image first
    subprocess.check_call(base_cmd_list, cwd="./base_image")
    subprocess.check_call(scrape_cmd_list, cwd="./scrape")
    subprocess.check_call(picarro_cmd_list, cwd="./picarro")

    print("\nDeploying Fn functions...\n")

    app_name = "openghg_pipeline"
    # Make sure we have an app calld openghg
    subprocess.run(["fn", "create", "app", app_name])

    deploy_cmd = ["fn", "--verbose", "deploy", "--app", app_name, "--local"]

    subprocess.check_call(deploy_cmd, cwd="./scrape")
    subprocess.check_call(deploy_cmd, cwd="./picarro")
except subprocess.CalledProcessError as e:
    print(f"Error - {str(e)}")
finally:
    cleanup()
