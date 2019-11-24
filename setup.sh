#!/bin/bash
mkdir logs
cd logs
touch website.log
cd ..
mkdir config
mkdir uwsgi
cd config 
touch config.ini
touch uwsgi-config.ini
cd ..


python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
deactivate

# installation
if ! [ -x "$(command -v memcached)" ]; then
  echo "Error: memcached is not installed."
  sudo apt-get install memcached
fi


# start
ps -fe|grep memcached |grep -v grep
if [ $? -ne 0 ]
then
memcached &
echo "start memcached....."
else
echo "memcached is runing....."
fi
