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
import sys
import msgpack
import logging
logging.basicConfig(filename="sendmsg.log", level=logging.DEBUG)

files = sys.argv[1:]
d = {
    'action': 'ParseAST',
    'filepath': '',
    'content': '',
    'language': 'python',
}

for f in files:
    logging.info(f)

    for encoding in ('utf_8', 'iso8859_15', 'iso8859_15', 'gb2313',
            'cp1251', 'cp1252', 'cp1250', 'shift-jis', 'gbk', 'cp1256',
            'iso8859-2', 'euc_jp', 'big5', 'cp874', 'euc_kr', 'iso8859_7'
            'cp1255'):
        with open(f, encoding=encoding) as infile:
            try:
                content = infile.read()
                break
            except UnicodeDecodeError:
                continue

    content = content.encode() if isinstance(content, str) else content
    d.update({
        'filepath': f,
        'content': content,
    })

    msg = msgpack.packb(d)
    sys.stdout.buffer.write(msg)
    sys.stdout.buffer.flush()

sys.stdout.buffer.close()
