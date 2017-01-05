#!/bin/bash

docker build -t my-boot2docker-img .
docker run --rm my-boot2docker-img > boot2docker.iso
