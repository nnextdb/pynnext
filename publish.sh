#!/usr/bin/env bash

if [ -d "./dist" ]
then
    echo "Directory /path/to/dir exists."
    rm -rf dist/*
else
    echo "Error: Directory /path/to/dir does not exists."
fi

python3 setup.py bdist_wheel --universal
twine upload dist/*
