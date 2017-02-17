import msgpack
import sys
from subprocess import *

# p = Popen(["python3", "pyparser.py"], stdin=PIPE, stdout=PIPE)

files = sys.argv[1:]
for f in files:
    d = {
        'action': 'ParseAST',
        'content': open(f).read()
    }
    msg = msgpack.packb(d)
    # p.stdin.b
    # print(msg.decode(errors='ignore'))
    sys.stdout.buffer.write(msg)
