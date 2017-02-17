import sys
import time
import msgpack
import pydetector.pydetector as detector
from pprint import pprint
from traceback import format_exc

def main():
    while True:
        try:
            try:
                request = msgpack.load(sys.stdin.buffer)
            except msgpack.exceptions.UnpackValueError:
                # finished kludge
                # FIXME
                exit()

            assert b'content' in request and request[b'content']
            if b'language' in request:
                assert request['language'].lower() == 'python'
            if b'language_version' in request:
                assert str(request[b'language_version'])[0] in ('1', '2', '3')

            code = request[b'content']
            status = 'ok'
            errors = []

            try:
                resdict = detector.detect(codestr = code, stop_on_ok_ast=True)
            except:
                status = 'error'
                errors.append('Exception trying to get the AST: {}'.format(format_exc()))
            else:
                codeinfo = resdict['<code_string>']
                if int(codeinfo['version']) in (3, 6):
                    ast = codeinfo['py3ast']
                elif codeinfo['version'] == 2:
                    ast = codeinfo['py2ast']
                else:
                    status = 'error'
                    errors.append('Could not determine Python version')

                if not ast:
                    status = 'error'
                    errors.append('Empty AST generated')

            outdict = {
                'status': status,
                'language': 'python',
                'language_version': str(codeinfo['version']),
                'driver': 'python23:1.0',
                'ast': ast,
            }
            # print(msgpack.dumps(outdict))
            sys.stdout.buffer.write(msgpack.dumps(outdict))
            sys.stdout.flush()
        except Exception as e:
            # XXX log the error
            outdict = {
                'status': 'fatal',
                'driver': 'python23:1.0',
                'errors': [format_exc()],
            }
            sys.stdout.buffer.write(msgpack.dumps(outdict))
            sys.stdout.flush()

            print(format_exc())
            time.sleep(0.3)


if __name__ == '__main__':
    main()
