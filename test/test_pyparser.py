import io
import sys
import msgpack
import unittest
# from pprint import pprint
from ast import literal_eval
from os.path import dirname, join

sys.path.append('../bin')
import pyparser # noqa: E402

def convert_bytes(data, to_bytes=False):
    """
    Both in normal operation and with this tests data comes trough a bytestream so this is needed to
    recursively convert the msgpack incoming data (the pprint data is converted just decoding and using
    literal_eval)
    """
    if type(data) in (list, tuple):
        newlist = []
        for item in data:
            newlist.append(convert_bytes(item), to_bytes)
        return newlist
    elif isinstance(data, dict):
        for key, value in data.items():
            newvalue = convert_bytes(value, to_bytes)
            newkey = convert_bytes(key, to_bytes)
            del data[key]
            data[newkey] = newvalue
        return data
    elif isinstance(data, bytes) and not to_bytes:
        return data.decode()
    elif isinstance(data, str) and to_bytes:
        return data.encode()
    return data


class TestPyParserBase(unittest.TestCase):
    def setUp(self):
        self._restart_data()

    def _restart_data(self):
        with open(join(dirname(__file__), 'data', 'helloworld.py')) as f:
            testcode = f.read()

        self.data = {
            'filepath': 'test.py',
            'action': 'ParseAST',
            'content': testcode,
            'language': 'python',
        }

        # This will mock the pyparser stdin
        self.sendbuffer = io.BytesIO()
        # This will mock the pyparser stdout
        self.recvbuffer = io.BytesIO()

    def _loadResults(self, format_):
        "Read all msgpacks from the recvbuffer"
        self.recvbuffer.seek(0)

        if format_ == pyparser.OutputType.PRINT:
            reply = self.recvbuffer.read().decode()
            if '}{' in reply:
                # if there are many results with OutputType.PRINT they are in the form
                # {dict}{dict}, insert a comma so literal_eval interprets them as a tuple
                reply = reply.replace('}{', '},{')
            reply = '[' + reply + ']'
            res = literal_eval(reply)

        elif format_ == pyparser.OutputType.MSGPACK:
            res = [convert_bytes(msg) for msg in msgpack.Unpacker(self.recvbuffer)]

        return res

# class Test10ProcessRequestFunc(TestPyParserBase):
    # def _add_to_buffer(self, count):
        # "Add count test msgpacks to the sendbuffer"
        # for i in range(count):
            # self.sendbuffer.write(msgpack.dumps(self.data))
        # self.sendbuffer.flush()


    # def _send_receive(self, nummsgs, outformat = pyparser.OutputType.MSGPACK, dataupdate=None):
        # if dataupdate:
            # self.data.update(dataupdate)

        # self._add_to_buffer(nummsgs)
        # self.sendbuffer.seek(0)
        # pyparser.process_requests(self.sendbuffer, self.recvbuffer,
                # outformat=outformat)
        # return self._loadResults(outformat)

    # def _check_reply_dict(self, reply, check_ast=True, has_errors = False):
        # self.assertIsInstance(reply, dict)
        # self.assertEqual(reply.get('driver'), 'python23:{}'.format(pyparser.__version__))
        # status = reply.get('status')

        # if has_errors:
            # assert status in ('ok', 'fatal')
            # errors = reply.get('errors', list)
            # self.assertIsInstance(errors, list)
            # self.assertGreater(len(errors), 0)
        # else:
            # self.assertEqual(reply.get('language'), 'python')
            # self.assertEqual(status, 'ok')
            # self._check_AST_dict(reply)
            # language_version = reply.get('language_version', -1)
            # assert str(language_version) in ('2', '3')

    # def _check_AST_dict(self, reply):
        # self.assertIsNotNone(reply)
        # assert 'ast' in reply
        # self.assertIsInstance(reply['ast'], dict)

        # for key in ('ast_type', 'body'):
            # assert key in reply['ast']

        # self.assertIsInstance(reply['ast']['body'], list)

        # for item in reply['ast']['body']:
            # for key in ('ast_type', 'lineno', 'col_offset'):
                # assert key in item

    # def test_normal_print(self):
        # replies = self._send_receive(1, pyparser.OutputType.PRINT)
        # self.assertEqual(len(replies), 1)
        # self._check_reply_dict(replies[0])

    # def test_normal_msgpack(self):
        # replies = self._send_receive(1, pyparser.OutputType.MSGPACK)
        # self.assertEqual(len(replies), 1)
        # self._check_reply_dict(replies[0])

    # def test_normal_print_many(self):
        # replies = self._send_receive(100, pyparser.OutputType.PRINT)
        # self.assertEqual(len(replies), 100)
        # for reply in replies:
            # self._check_reply_dict(reply)

    # def test_normal_msgpack_many(self):
        # replies = self._send_receive(100, pyparser.OutputType.MSGPACK)
        # self.assertEqual(len(replies), 100)
        # for reply in replies:
            # self._check_reply_dict(reply)

    # def test_error_print(self):
        # wrongcode = 'wtf lol'

        # replies = self._send_receive(1, pyparser.OutputType.PRINT, {'content': wrongcode})
        # self.assertEqual(len(replies), 1)
        # ast = replies[0].get('ast')
        # self.assertIsNone(ast)
        # self._check_reply_dict(replies[0], has_errors=True)

        # # Check that it still alive
        # self._restart_data()
        # replies = self._send_receive(1, pyparser.OutputType.PRINT)
        # self.assertEqual(len(replies), 1)

    # def test_error_msgpack(self):
        # wrongcode = 'wtf lol'

        # replies = self._send_receive(1, pyparser.OutputType.MSGPACK, {'content': wrongcode})
        # self.assertEqual(len(replies), 1)
        # ast = replies[0].get('ast')
        # self.assertIsNone(ast)
        # self._check_reply_dict(replies[0], has_errors=True)

        # # Check that it still alive
        # self._restart_data()
        # replies = self._send_receive(1, pyparser.OutputType.PRINT)
        # self.assertEqual(len(replies), 1)

    # def test_broken_msgpack(self):
        # brokendata = msgpack.dumps(self.data)[:-60]
        # self.sendbuffer.write(brokendata)
        # self.sendbuffer.flush()
        # reply = self._send_receive(1, pyparser.OutputType.MSGPACK)[0]
        # self.assertEqual(reply['status'], 'fatal')
        # self.assertEqual(len(reply['errors']), 1)


class Test20ReqProcMethods(TestPyParserBase):
    def test_check_input(self):
        brequest = convert_bytes(self.data, to_bytes=True)
        processor = pyparser.RequestProcessor(self.recvbuffer, pyparser.OutputType.MSGPACK)
        res = processor._check_input_request(brequest)
        self.assertEqual(res[1], 'test.py')

    def test_check_input_bad(self):
        del self.data['content']
        brequest = convert_bytes(self.data, to_bytes=True)
        processor = pyparser.RequestProcessor(self.recvbuffer, pyparser.OutputType.MSGPACK)
        with self.assertRaises(pyparser.RequestCheckException) as _: # noqa: F841
            processor._check_input_request(brequest)

    def test_send_response_msgpack(self):
        processor = pyparser.RequestProcessor(self.recvbuffer, pyparser.OutputType.MSGPACK)
        processor._send_response(self.data)
        res = self._loadResults(pyparser.OutputType.MSGPACK)
        self.assertEqual(len(res), 1)
        self.assertDictEqual(self.data, res[0])

    def test_send_response_print(self):
        processor = pyparser.RequestProcessor(self.recvbuffer, pyparser.OutputType.PRINT)
        processor._send_response(self.data)
        res = self._loadResults(pyparser.OutputType.PRINT)
        self.assertEqual(len(res), 1)
        self.assertDictEqual(self.data, res[0])

    # process request already tested with TetPyParserBase

    def test_return_error(self):
        processor = pyparser.RequestProcessor(self.recvbuffer, pyparser.OutputType.PRINT)
        processor.errors = ['test error']
        processor._return_error('test.py', 'fatal')
        res = self._loadResults(pyparser.OutputType.PRINT)
        self.assertEqual(len(res), 1)
        self.assertDictEqual(res[0] , {'driver': 'python23:1.0',
                                       'errors': ['test error'],
                                       'filepath': 'test.py',
                                       'status': 'fatal'})


if __name__ == '__main__':
    unittest.main()
