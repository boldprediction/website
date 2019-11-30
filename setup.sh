#!/bin/bash
pip install -r requirements.txt


mkdir logs
cd logs
touch website.log

cd ..
cd ..
mkdir config
cd config 
touch config.ini

cd ..
mkdir uwsgi
cd uwsgi 
touch uwsgi.ini
cd ..
