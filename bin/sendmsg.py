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
