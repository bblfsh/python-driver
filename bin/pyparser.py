#!/usr/bin/env python3
import sys
import signal
import logging
import msgpack
import pydetector.detector as detector
from pprint import pformat
from traceback import format_exc

logging.basicConfig(filename="pyparser.log", level=logging.ERROR)

# TODO: modify the AST adding comments, use tokenizer?
# TODO; benchmark this with compression

__version__ = '1.0'

# Gracefully handle control c without adding another try-except on top of the loop
def ctrlc_signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, ctrlc_signal_handler)


class OutputType():
    MSGPACK = 1
    PRINT   = 2

class RequestCheckException(Exception): pass

class RequestProcessor():
    def __init__(self, outbuffer, output_format=OutputType.MSGPACK):
        self.outformat = output_format
        self.outbuffer = outbuffer

    def _check_input_request(self, request):
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

        code = request.get(b'content', b'').decode()
        if not code:
            raise RequestCheckException('Bad input message, missing content')

        language = request.get(b'language', b'').decode()
        if language.lower() != 'python':
            raise RequestCheckException('Bad language requested for the Python driver: "%s"'
                          % language)

        language_version = request.get(b'language_version', b'')
        if language_version not in (b'', b'1', b'2', b'3'):
            raise RequestCheckException('Bad language version requested, Python driver only '
                          'supports versions 1, 2 and 3')

        return code, request.get(b'filepath', b'').decode()

    def _send_response(self, response):
        if self.outformat == OutputType.PRINT:
            prettyoutput_bytes = pformat(response).encode('utf-8')
            self.outbuffer.write(prettyoutput_bytes)
        else:
            self.outbuffer.write(msgpack.dumps(response))
        self.outbuffer.flush()

    def _return_error(self, filepath, status='error'):
        """
        Build and send to stdout and error response. Also log
        the errors to the pyparser.log.
        """

        logging.error('Filepath: {}, Errors: {}'.format(filepath, self.errors))
        response = {
                'status': status,
                'errors': self.errors,
                'driver': 'python23:%s' % __version__,
        }
        if filepath:
            response['filepath'] = filepath
        self._send_response(response)

    def process_request(self, request):
        filepath    = ''
        ast         = None
        self.errors = []

        try:
            code, filepath = self._check_input_request(request)

            # We want the code detection to be fast and we prefer Python3 AST so using
            # the stop_on_ok_ast will avoid running a Python2 subprocess to check the
            # AST with Python2 if the Python3 version (which is a better AST anyway) worked
            resdict  = detector.detect(codestr=code, stop_on_ok_ast=True)
            codeinfo = resdict['<code_string>']
            version  = codeinfo['version']

            if version in (3, 6) and codeinfo['py3ast']:
                ast = codeinfo['py3ast']
            elif version in (1, 2) and codeinfo['py2ast']:
                ast = codeinfo['py2ast']
            else:
                raise Exception('Could not determine Python version')

            if not ast:
                raise Exception('Empty AST generated')

            response = {
                'status'           : 'ok',
                'errors'           : self.errors,
                'language'         : 'python',
                'language_version' : version,
                'driver'           : 'python23:1.0',
                'ast'              : ast,
            }
            if filepath:
                response['filepath'] = filepath

            self._send_response(response)

        except:
            status = 'fatal' if ast is None else 'error'
            self.errors.append(format_exc())
            self._return_error(filepath, status=status)


def process_requests(inbuffer, outbuffer, outformat=OutputType.MSGPACK):
    """
    Main loop. It will read msgpack incoming requests from inbuffer using
    the msgpack lib stream unpacker. In case of error it will generate
    an error reply, also in msgpack format. The replies will be printed
    in stdout using bytes.
    """
    # Instantiated out of the loop to avoid the object-creation cost
    processor = RequestProcessor(outbuffer, outformat)
    for request in msgpack.Unpacker(inbuffer):
        processor.process_request(request)

def main():
    """
    If you pass the --print command line parameter the replies will be
    printed using pprint without wrapping them in the msgpack format which
    can be handy when debugging.
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--print':
        outformat = OutputType.PRINT
    else:
        outformat = OutputType.MSGPACK
    process_requests(sys.stdin.buffer, sys.stdout.buffer, outformat)


if __name__ == '__main__':
    main()
