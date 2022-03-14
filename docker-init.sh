#! /bin/bash

docker-compose build --build-arg PYTHON_IMAGE=$PYTHON_IMAGE
docker-compose up -d
