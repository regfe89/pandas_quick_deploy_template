#!/bin/bash
`python3 -m venv env`
source env/bin/activate
pip install -U pip
pip install  pandas
pip install  matplotlib
pip install  scipy
pip install  statsmodels
pip freeze -> requirements.txt
