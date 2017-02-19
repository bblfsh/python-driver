import sys
import msgpack
import pydetector.detector as detector
from pprint import pprint
from traceback import format_exc

# TODO: modify the AST adding comments, use tokenizer?
# and use dependency injection to pass a custom ast module that extract
# comments to pydetector

__version__ = '1.0'

class RequestCheckException(Exception): pass

def check_input_request(request, errors):
    """
    Check the incoming request package and validate that the 'content' and
    'language' keys are not missing and that 'language' and 'language_version'
    are the right ones for this driver.

    Args:
        request (bytes, messagepack): The incoming request in messagepack format
            as bytes.

        errors (List[str]): the list of errors. New errors will be added to it in place.
    Raises:
        RequestCheckException if the request failed to validate.
    """

    with_error = False
    if b'content' not in request or not request[b'content']:
        errors.append('Bad input message, missing content')
        with_error = True

    if b'language' in request and request[b'language'].lower() != b'python':
        errors.append('Bad language requested for the Python driver: "%s"'
                      % request[b'language'].decode('utf-8'))
        with_error = True

    if 'language_version' in request and \
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
    """
    Main loop. It will read msgpack incoming requests from stdin using
    the msgpack lib stream unpacker. In case of error it will generate
    an error reply, also in msgpack format. The replies will be printed
    in stdout using bytes.

    If you pass the --print command line parameter the replies will be
    printed using pprint without wrapping them in the msgpack format which
    can be handy when debugging.
    """
    # TODO: check what errors are fatal and what to do with them

    if len(sys.argv) > 1 and sys.argv[1] == '--print':
        outformat = 'print'
    else:
        outformat = 'msgpack'

    while True:
        errors = []

        try:
            for request in msgpack.Unpacker(sys.stdin.buffer):

                check_input_request(request, errors)
                code     = request[b'content']
                # We want the code detection to be fast and we prefer Python3 AST so using
                # the stop_on_ok_ast will avoid running a Python2 subprocess to check the
                # AST with Python2 if the Python3 version (which is a better AST anyway) worked
                resdict  = detector.detect(codestr=code, stop_on_ok_ast=True)
                codeinfo = resdict['<code_string>']
                version  = codeinfo['version']

                if version in (3, 6):
                    ast = codeinfo['py3ast']
                elif version in (1, 2):
                    ast = codeinfo['py2ast']
                else:
                    raise Exception('Could not determine Python version')

                if not ast:
                    raise Exception('Empty AST generated')

                outdict = {
                    'status': 'ok',
                    'errors': errors,
                    'language': 'python',
                    'language_version': version,
                    'driver': 'python23:1.0',
                    'ast': ast,
                }

                if outformat == 'print':
                    pprint(outdict)
                else:
                    # sys.stdout.buffer is the byte stream and since msgpack generates
                    # byte-typed data on Python3 is the one we need to use
                    sys.stdout.buffer.write(msgpack.dumps(outdict))

                sys.stdout.flush()

        except KeyboardInterrupt:
            exit(1)

        except:
            return_error(status='error', errors=[format_exc()])


if __name__ == '__main__':
    main()
