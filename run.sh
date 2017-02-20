#!/bin/sh

docker stop pyparser
docker rm pyparser
docker run -i --name pyparser --rm pyparser:latest 
