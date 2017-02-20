#!/bin/sh
docker stop pyparser
docker rm pyparser
docker rmi pyparser:latest
docker build --tag pyparser .
