#!/bin/bash
mkdir logs
cd logs
touch website.log
cd ..
mkdir config
cd config 
touch config.ini
cd ..
pip install -r requirements.txt

cd ..

mkdir uwsgi
cd uwsgi 
touch uwsgi.ini
cd ..


# # installation
# if ! [ -x "$(command -v memcached)" ]; then
#   echo "Error: memcached is not installed."
#   sudo apt-get install memcached
# fi


# # start
# ps -fe|grep memcached |grep -v grep
# if [ $? -ne 0 ]
# then
# memcached &
# echo "start memcached....."
# else
# echo "memcached is runing....."
# fi
