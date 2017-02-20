#!/bin/sh
docker stop pyparser
docker rm pyparser
docker rmi pyparser:latest
cp Dockerfile.ubuntu Dockerfile
docker build --tag pyparser_ubuntu .
