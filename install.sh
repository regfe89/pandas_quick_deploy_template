#!/bin/bash
`python3 -m venv env`
source env/bin/activate
pip install -U pip
pip install  pandas
pip install fastapi
pip install uvicorn
pip install jinja2
pip install scipy
pip install  matplotlib
pip install aiofiles
pip freeze -> requirements.txt
