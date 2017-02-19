#!/bin/sh
bin/sendmsg.py bin/pyparser.py | docker run -i --name pyparser --rm pyparser:latest 
