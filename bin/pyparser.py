#!/usr/bin/env python3
__version__ = '1.0'

import io
import abc
import sys
import json
import signal
import logging
import msgpack
import pydetector.detector as detector
from pprint import pformat, pprint
from traceback import format_exc
logging.basicConfig(filename="pyparser.log", level=logging.WARNING)

class RequestInstantiationException(Exception): pass
class RequestCheckException(Exception): pass

# Gracefully handle control c without adding another try-except on top of the loop
def ctrlc_signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, ctrlc_signal_handler)


def asstr(txt):
    """
    Decode a byte string if it really is an intance of bytes
    """
    if isinstance(txt, bytes):
        return txt.decode()
    return txt


class RequestProcessor(metaclass=abc.ABCMeta):
    def __init__(self, outbuffer):
        self.outbuffer = outbuffer

    @staticmethod
    @abc.abstractmethod
    def _prepare_dict(d):
        pass

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
        request = self._prepare_dict(request)
        code = asstr(request.get('content', ''))

        if not code:
            raise RequestCheckException('Bad input message, missing content')

        language = asstr(request.get('language', ''))
        if language.lower() != 'python':
            raise RequestCheckException('Bad language requested for the Python driver: "%s"'
                                        % language)

        language_version = asstr(request.get('language_version', ''))
        if language_version not in ('', '1', '2', '3'):
            raise RequestCheckException('Bad language version requested, Python driver only '
                                        'supports versions 1, 2 and 3')

        return code, asstr(request.get('filepath', ''))

    @abc.abstractmethod
    def _send_response(self, response):
        pass

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


class RequestProcessorJSON(RequestProcessor):

    JSONEndMark = '@@----@@\n'

    def _send_response(self, response):
        self.outbuffer.write(json.dumps(response, ensure_ascii=False))
        self.outbuffer.write('\n@@----@@\n')
        self.outbuffer.flush()

    @staticmethod
    def _prepare_dict(d):
        """
        JSON already comes encoded as str so no need to lose time reencoding
        anything
        """
        return d

    def _extract_docs(self, inbuffer):
        """
        This generator will read the inbuffer yielding the JSON
        docs when it finds the ending mark
        """
        strio = io.StringIO()

        for line in inbuffer.readlines():
            try:
                if line == RequestProcessorJSON.JSONEndMark:
                    yield json.loads(strio.getvalue())
                    strio.seek(0)
                    strio = io.StringIO()
                else:
                    strio.write(line)
            except:
                self.errors = ['error decoding JSON from input: {}'.format(strio.getvalue())]
                self._return_error(filepath='<jsonstream>', status='fatal')


    def process_requests(self, inbuffer):
        for doc in self._extract_docs(inbuffer):
            self.process_request(doc)


class RequestProcessorMSGPack(RequestProcessor):
    def _send_response(self, response):
        self.outbuffer.write(msgpack.dumps(response))
        self.outbuffer.flush()

    @staticmethod
    def _prepare_dict(d):
        """
        Convert all byte-string keys and values to normal strings (non recursively since
        we only have one level)
        """
        newdict = {}
        for key, value in d.items():
            if isinstance(value, bytes):
                value = value.decode()

            if isinstance(key, bytes):
                key = key.decode()

            newdict[key] = value
        return newdict

    def process_requests(self, inbuffer):
        for request in msgpack.Unpacker(inbuffer):
            self.process_request(request)


ProcessorConfigs = {
        'json': {
            'class': RequestProcessorJSON,
            'inbuffer': sys.stdin,
            'outbuffer': sys.stdout
        },

        'msgpack': {
            'class': RequestProcessorMSGPack,
            'inbuffer': sys.stdin.buffer,
            'outbuffer': sys.stdout.buffer
        }
}


def getRequestProcessorInstance(format_, custom_inbuffer=None, custom_outbuffer=None):
    conf = ProcessorConfigs.get(format_)
    if not conf:
        raise RequestInstantiationException('No RequestProcessor found for format {}'
                .format(format_))

    outbuffer = custom_outbuffer if custom_outbuffer else conf['outbuffer']
    inbuffer = custom_inbuffer if custom_inbuffer else conf['inbuffer']

    instance = conf['class'](outbuffer)
    return instance, inbuffer


def main():
    """
    If you pass the --print command line parameter the replies will be
    printed using pprint without wrapping them in the msgpack format which
    can be handy when debugging.
    """

    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        format_ = 'json'
    else:
        format_ = 'msgpack'

    processor, inbuffer = getRequestProcessorInstance(format_)
    processor.process_requests(inbuffer)


if __name__ == '__main__':
    main()
