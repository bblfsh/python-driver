import re
import pydetector.ast_checks as achecks
import pydetector.regexp_checks as rchecks
from io import open
from pprint import pprint

__all__ = ['detect']

# TODO: unittests with python 2 and 3 stdlibs. Test code matching every regex
# TODO: conditional import of ujson as json if available

QUOTE_TRIPLE_SUBREGEX = re.compile(r'''\"{3}(.*?)\"{3}|'{3}(.*?)'{3}''', re.DOTALL)
# awesome:
QUOTE_SUBREGEX = re.compile(r"""(?![\\'])\"((?!\").)*(?!\\)\"(?!')|(?![\\\"])'((?!').)*(?!\\)'(?!\")""")
COMMENT_SUBREGEX = re.compile(r"#.*$", re.MULTILINE)

def remove_str_comments(code):
    """
    Remove all the comments in the code (from the # to EOL). Returns
    a new string with the comments removed. This improves the detection
    rates a lot removing most of the false positives.
    """
    # Empty strings
    newcode = QUOTE_TRIPLE_SUBREGEX.sub("''", code)
    newcode = QUOTE_SUBREGEX.sub("''", newcode)
    # Remove comments
    return COMMENT_SUBREGEX.sub("", newcode)


def detect(files=None, codestr=None, ast_checks=True, modules_checks=True,
        modsyms_checks=False, stop_on_ok_ast=False, modules_score=150,
        symbols_score=100, verbosity=0):
    """
    Try to detect if a source file is Python 2 or 3. It uses a combination of tests
    based on AST extraction and regular expressions.

    Args:
        files (List[str], optional): list of files
        codestr (str, optional): source code of a single module to parse
        ast_checks (bool): enable checking if the AST parses with both Python versions
        modules_checks (bool): enable checking version-specific module imports
        modsyms_checks (bool): enable checking version-specific module symbols. Please note
            that this test can be much slower than the others.
        stop_on_ok_ast (bool): if the first AST tested works, don't even try with the other
            version
        modules_score (int): score given to specific-module matches
        symbols_score (int): score given to symbol-specific matches
        verbosity (int): verbosity level from 0 (quiet) to 2

    Return:
        Dictionary where each key is the filename and the value another dictionary
        with the keys "py2ast" and "py3ast" that will hold the AST if sucessfully
        parser for that version or "None", "version" with the version number (2 or 3)
        or 6 is the module seems to be compatible with both versions, "matches" that
        will hold a list of the matched rules and scores and "py2_score/py3_score"
        with the specific score.
    """

    returndict = {}

    if not files:
        if not codestr:
            raise Exception('files or codestr parameters are required')
        files = ['<code_string>']

    for filename in files:
        returndict[filename] = {
            'py2ast': None,
            'py3ast': None,
            'version': 0,
            'matches': [],
            'py2_score': 0,
            'py3_score': 0
        }
        retdict = returndict[filename] # alias

        # helper for lazy bastards
        def apply_score(py2_score, py3_score):
            retdict['py2_score'] += py2_score
            retdict['py3_score'] += py3_score

        if verbosity:
            print('Checking file %s: ' % filename)

        input_code = None

        if filename == '<code_string>':
            input_code = codestr
        else:
            # this have problems if the file is not encoding in utf8 input_code = sys.stdin.read()
            # From most to  less common, this should cover 99.9% of the encodings used
            for encoding in ('utf_8', 'iso8859_15', 'iso8859_15', 'gb2313',
                    'cp1251', 'cp1252', 'cp1250', 'shift-jis', 'gbk', 'cp1256',
                    'iso8859-2', 'euc_jp', 'big5', 'cp874', 'euc_kr', 'iso8859_7'
                    'cp1255'):
                with open(filename, encoding=encoding) as infile:
                    try:
                        input_code = infile.read()
                        break
                    except UnicodeDecodeError:
                        continue
            else:
                raise Exception('Could not determine file encoding')

        if ast_checks:
            # Test the AST. This doesnt give points: either both pass, both fails
            # or one is correct and the other dont in which case we shortcircuit the return
            astversion, py2astroot, py3astroot = achecks.check_ast(
                        input_code, try_other_on_sucess=not stop_on_ok_ast,
                        verbosity=verbosity
            )
            retdict.update({
                'py2ast': py2astroot,
                'py3ast': py3astroot,
                'matches': [('PY%dASTOK' % astversion, ())]
            })

        # One parsed and the other didnt, no need to continue checking
        if astversion in (2, 3):
            retdict['version'] = astversion
            continue
        else:
            retdict['py2ast'] = py2astroot
            retdict['py3ast'] = py3astroot

        # Remove comments and emptyfy strings before doing the regex tests,
        # this will remove most fase positives
        cleaned_code = remove_str_comments(input_code)
        # print(cleaned_code); exit()

        if modules_checks:
            apply_score(*rchecks.check_syntax_regex(cleaned_code, retdict['matches']))
            apply_score(*rchecks.check_modules_regex(cleaned_code, retdict['matches'],
                match_score = modules_score))

        # This one is SLOOOOOW
        if modsyms_checks:
            apply_score(
                *rchecks.check_modulesymbols_regex(cleaned_code, retdict['matches'], symbols_score)
            )

        if retdict['py2_score'] > retdict['py3_score']:
            retdict['version'] = 2
        elif retdict['py3_score'] > retdict['py2_score']:
            retdict['version'] = 3
        else:
            retdict['version'] = 6

        if verbosity:
            print('Python 2 score: %d' % retdict['py2_score'])
            print('Python 3 score: %d' % retdict['py3_score'])
            print('\n')

    return returndict

def parse_args():
    # TODO: add arguments for python executables
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", type=int, default=0,
            help="increase output verbosity (0 to 2)")

    parser.add_argument("-d", "--defaultversion", type=int, default=0,
            help="Python version to return if there is a match. If not used "
                 "it will be just reported as a match (default=report matches)")

    parser.add_argument("-a", "--testast", action="store_true", default=True,
            help="Do the AST extraction test (default=enabled)")

    parser.add_argument("-o", "--asttestboth", dest='asttestboth', action='store_true',
            help="Do the AST test with the other version even if the first one works"
                 "(default=enabled)")
    parser.add_argument("-n", "--no-asttestboth", dest='asttestboth', action='store_false',
            help="Do the AST test with the other version even if the first one works"
                 "(default=enabled)")

    parser.add_argument("-m", "--testmodules", action="store_true", default=True,
            help="Test for version-specific modules (default=enabled)")

    parser.add_argument("-s", "--testmodulesyms", action="store_true", default=False,
            help="Test for version-specific module symbols (WARNING: SLOW!) (default=disabled)")

    parser.add_argument("files", nargs=argparse.REMAINDER, help="Files to parse")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    returndict = detect(
            args.files,
            ast_checks=args.testast,
            modules_checks=args.testmodules,
            modsyms_checks=args.testmodulesyms,
            stop_on_ok_ast=not args.asttestboth,
            verbosity=args.verbosity
            )
    for fdata in returndict:
        del returndict[fdata]['py2ast'] # not json serializable in the current form
        del returndict[fdata]['py3ast'] # not json serializable in the current form

    pprint(returndict)

    if args.verbosity:
        py2_count = py3_count = pyany_count = 0
        for key in returndict:
            version = returndict[key]['version']

            if version == 2 or (version == 6 and args.defaultversion == 2):
                py2_count += 1
            elif version == 3 or (version == 6 and args.defaultversion == 3):
                py3_count += 1
            else:
                pyany_count += 1

        print('%d files parsed, py2: %d, py3: %d any: %d' %
                (len(returndict), py2_count, py3_count, pyany_count))
