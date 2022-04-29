#!/usr/bin/env bash

if [ -d "./dist" ]
then
    echo "Removing existing ./dist."
    rm -rf dist/*
else
    echo "Error: ./dist."
fi

python3 setup.py bdist_wheel --universal
twine upload dist/*