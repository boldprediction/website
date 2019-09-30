#!/bin/bash

mkdir logs
cd logs
touch website.log
cd ..
mkdir config

python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations auth
python manage.py migrate auth
python manage.py makemigrations boldpredict
python manage.py migrate boldpredict
deactivate
