#!/bin/sh
docker stop pyparser
docker rm pyparser
docker build --tag pyparser .
