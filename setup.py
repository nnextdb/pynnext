# #!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright 2022, NNext, Co."

import os
from m2r import parse_from_file
from setuptools import find_packages, setup

long_description = parse_from_file('README.rst')

setup(
    name="nnext",
    description="Python client library for the NNext. A ⚡ blazingly fast, 🔍 nearest-neighbors vector search engine for building delightful ML apps",
    long_description=long_description,
    version="0.0.36",
    install_requires=[
        'grpcio >= 1.44.0; python_version >= "3.6"',
        'protobuf >= 3.20.0; python_version >= "3.6"'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={},
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={},
    license='Apache 2.0',
    author="NNext, co",
    author_email="team@nnext.ai",
    url="https://nnext.ai",
)
