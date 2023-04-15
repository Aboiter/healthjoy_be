#!/bin/bash

pip3 install virtualenv

python3 -m virtualenv venv

source ./venv/bin/activate

python3 -m pip install -r requirements.txt
python3 -m pip install -e .