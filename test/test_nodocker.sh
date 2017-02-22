#!/bin/sh
time sh -c "./sendmsg.py --json /usr/lib/python2.7/*.py /usr/lib/python3.5/*.py|../bin/pyparser.py --json > /dev/null"

