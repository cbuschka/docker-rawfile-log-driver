#!/bin/bash

mkdir -p /run/docker/plugins/
cd /docker-rawfile-log-driver
export PYTHONPATH=$PYTHONPATH:/docker-rawfile-log-driver
exec uwsgi --ini /docker-rawfile-log-driver/uwsgi.ini

