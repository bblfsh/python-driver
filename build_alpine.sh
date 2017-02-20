#!/bin/sh
docker stop pyparser
docker rm pyparser
docker rmi pyparser:latest
cp Dockerfile.alpine Dockerfile
docker build --tag pyparser_alpine .
