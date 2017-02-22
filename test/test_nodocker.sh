#!/bin/sh
time sh -c "./sendmsg.py /usr/lib/python2.7/*.py /usr/lib/python2.7/*.py|../bin/pyparser.py > /dev/null"

