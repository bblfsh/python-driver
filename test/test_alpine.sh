#!/bin/sh
time sh -c './sendmsg.py /usr/lib/python2.7/*.py | docker run -i --name pyparser --rm pyparser_alpine:latest > /dev/null'
