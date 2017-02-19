#!/usr/bin/env python3
"""
Script to help test and debug. It will create a babelfish message
with the code of the files passed as argument and output them
on stdout so you can pipe them to pyparser or the docker image like
this:

$ ./sendmsg.py [source_file.py]|./pyparser.py

Or with the Docker image:

$ ./sendmsg.py [source_file.py]|docker run -it --rm pyparser:latest
"""
import msgpack
import sys

files = sys.argv[1:]
for f in files:
    d = {
        'action': 'ParseAST',
        'content': open(f).read()
    }
    msg = msgpack.packb(d)
    sys.stdout.buffer.write(msg)
