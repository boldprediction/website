#!/bin/bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations auth
python manage.py migrate auth
python manage.py makemigrations boldpredict
python manage.py migrate boldpredict
deactivate
