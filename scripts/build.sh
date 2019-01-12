#!/bin/bash

PROJECT_DIR=$(cd `dirname $0`/.. && pwd)

sudo rm -rf $PROJECT_DIR/rootfs
mkdir -p $PROJECT_DIR/rootfs

docker build -t rawfile-build -f $PROJECT_DIR/Dockerfile.build $PROJECT_DIR
docker rm -f rawfile-container
ID=$(docker create --name rawfile-container rawfile-build true)
docker export $ID | sudo tar -x -C $PROJECT_DIR/rootfs
docker plugin disable rawfile
docker plugin rm -f rawfile
sudo docker plugin create --compress=false rawfile $PROJECT_DIR
docker plugin ls
docker plugin enable rawfile
docker plugin ls

