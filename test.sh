#!/bin/sh
bin/sendmsg.py /usr/lib/python2.7/*.py | docker run -i --name pyparser --rm pyparser:latest 
