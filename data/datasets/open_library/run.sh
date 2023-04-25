#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# this is as far as I got
python3 download.py
