import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="gather",
    version="0.0.1",
    author="Gareth Jones",
    author_email="gareth@openghg.org",
    description="A collection of tools we use to gather data from our data providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openghg/gather",
    project_urls={
        "Bug Tracker": "https://github.com/openghg/gather/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    include_package_data=True,
    package_data={"": ["data/*"]},
    package_dir={"": "."},
    packages=setuptools.find_packages(include=["gather", "gather.*"]),
    python_requires=">=3.7",
)
