#!/bin/bash

mkdir logs
cd logs
touch website.log
cd ..
mkdir config

python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
deactivate
