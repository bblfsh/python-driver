#!/bin/bash

docker stop pyparser
docker rm pyparser
docker run -it --name pyparser --rm pyparser:latest 
