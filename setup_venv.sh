#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt -r requirements-dev.txt
python setup.py develop
