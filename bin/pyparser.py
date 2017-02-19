import sys
import msgpack
import pydetector.detector as detector
from traceback import format_exc

# TODO: modify the AST adding comments, use tokenizer?
# TODO: detect the end of the stdin in a less kludgy way
# TODO: command line option to export JSON or just pprint
# the output for debugging (to sys.stdout, unbuffered)

__version__ = '1.0'

class RequestCheckException(Exception): pass

def check_input_request(request, errors):

    with_error = False
    if b'content' not in request or not request[b'content']:
        errors.append('Bad input message, missing content')
        with_error = True

    if b'language' in request and request[b'language'].lower() != b"python":
        errors.append('Bad language requested for the Python driver: "%s"'
                      % request[b'language'].decode('utf-8'))
        with_error = True

    if b'language_version' in request and \
            request[b'language_version'][0] not in (b'1', b'2', b'3'):
        errors.append('Bad language version requested, Python driver only '
                      'supports versions 1, 2 and 3')
        with_error = True

    if with_error:
        raise RequestCheckException()


def return_error(status='error', errors=''):
    outdict = {
            'status': status,
            'errors': errors[0] if isinstance(errors, str) else errors,
            'driver': 'python23:%s' % __version__,
    }
    sys.stdout.buffer.write(msgpack.dumps(outdict))
    sys.stdout.flush()


def main():
    while True:
        errors = []

        try:
            try:
                request = msgpack.load(sys.stdin.buffer)
            except msgpack.exceptions.UnpackValueError:
                # finished kludge
                # FIXME
                exit()

            check_input_request(request, errors)

            code = request[b'content']
            status = 'ok'
            version = 0
            ast = ''

            resdict = detector.detect(codestr = code.decode('utf-8'), stop_on_ok_ast=True)
            codeinfo = resdict['<code_string>']
            version = codeinfo['version']

            if version in (3, 6):
                ast = codeinfo['py3ast']
            elif version == 2:
                ast = codeinfo['py2ast']
            else:
                raise Exception('Could not determine Python version')

            if not ast:
                raise Exception('Empty AST generated')

            outdict = {
                'status': status,
                'errors': errors,
                'language': 'python',
                'language_version': version,
                'driver': 'python23:1.0',
                'ast': ast,
            }
            sys.stdout.buffer.write(msgpack.dumps(outdict))
            sys.stdout.flush()

        except:
            return_error(status='fatal', errors=[format_exc()])


if __name__ == '__main__':
    main()
