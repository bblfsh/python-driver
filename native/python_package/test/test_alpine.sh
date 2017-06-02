#!/bin/sh
# Alpine 3.6:
time sh -c './sendmsg.py /usr/lib/python2.7/*.py | docker run -i --name python_driver --rm 1edcc008c3f6 /opt/driver/bin/native > /dev/null'
