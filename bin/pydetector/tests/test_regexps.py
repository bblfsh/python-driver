import unittest
import sys
from textwrap import dedent
sys.path.append('..')
from regexp_checks import check_modules_regex, check_syntax_regex # noqa: E402



class RegexpTestCase(unittest.TestCase):
    # me quedo en has_key
    def do_regexp_test(self, testdata, checkmethod):
        matches = []
        ret = checkmethod(testdata[0], matches)
        print(ret)
        self.assertEqual(ret[0], testdata[1])
        self.assertEqual(ret[1], testdata[2])
        self.assertEqual(len(matches), testdata[3])


class TestSyntaxRegex(RegexpTestCase):
    def test_exceptions_nonlocal(self):
        code = (dedent("""
            if something:
                nonlocal var
                raise SomeException() from None
            """), 0, 200, 2)
        self.do_regexp_test(code, check_syntax_regex)

    def test_raise_except(self):
        code = (dedent("""
            try:
                someargo.thing()
                raise SomeException, stuff
            except SomeException, e
            """), 200, 0, 2)
        self.do_regexp_test(code, check_syntax_regex)

    def test_old_print(self):
        code = (dedent("""
            print "im old"
            print("im not so old")
            """), 100, 0, 1)
        self.do_regexp_test(code, check_syntax_regex)

    def test_rawinput(self):
        code = (dedent("""
            var = raw_input("tell me something:")
            """), 100, 0,  1)
        self.do_regexp_test(code, check_syntax_regex)


if __name__ == '__main__':
    unittest.main()
