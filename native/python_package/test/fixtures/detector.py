import re

from io import open
from pydetector.ast_checks import check_ast
from pydetector.regexp_checks import check_syntax_regex, check_modules_regex,\
        check_modulesymbols_regex

__all__ = ['detect']

QUOTE_TRIPLE_SUBREGEX = re.compile(r'''\"{3}(.*?)\"{3}|'{3}(.*?)'{3}''', re.DOTALL)
QUOTE_SUBREGEX = re.compile(
    r'''(?<!(\\|'))\".*(?<!\\)\"''' +
    '|' +
    r"""(?<!(\\|\"))'.*(?<!\\)'"""
)
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
        Try to detect if a source file is Python 2 or 3. It uses a combination of
    tests based on AST extraction and regular expressions.

    Args: files (List[str], optional): list of files. You can omit this parameter
    if you pass codestr.

        codestr (str, optional): source code of a single module to parse. You can
        omit this parameter if you pass "files".

        ast_checks (bool): enable checking if the AST parses with both Python
        versions

        modules_checks (bool): enable checking version-specific module imports

        modsyms_checks (bool): enable checking version-specific module symbols.
        Please note that this test can be much slower than the others.

        stop_on_ok_ast (bool): if the first AST tested works, don't even try with
        the other version

        modules_score (int): score given to specific-module matches

        symbols_score (int): score given to symbol-specific matches

        verbosity (int): verbosity level from 0 (quiet) to 2

    Return:
        Dictionary where each key is the filename and the value another dictionary
        with the keys "py2ast" and "py3ast" that will hold the AST if sucessfully
        parser for that version or "None", "version" with the version number (2 or
        3) or 6 is the module seems to be compatible with both versions, "matches"
        that will hold a list of the matched rules and scores and
        "py2_score/py3_score" with the specific score.
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
            'py3_score': 0,
            'py2_ast_errors': [],
            'py3_ast_errors': [],
        }
        retdict = returndict[filename]  # alias

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
            for encoding in ('utf_8', 'iso8859_15', 'iso8859_1', 'gb2313',
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
            astversion, py2astroot, py3astroot, py2_err, py3_err = check_ast(
                        input_code, try_other_on_sucess=not stop_on_ok_ast,
                        verbosity=verbosity
            )
            retdict.update({
                # 'py2ast': {'PY2AST': py2astroot if py2astroot is not None else None},
                # 'py3ast': {'PY3AST': py3astroot if py2astroot is not None else None},
                'py2ast': {'PY2AST': py2astroot} if py2astroot else None,
                'py3ast': {'PY3AST': py3astroot} if py3astroot else None,
                'matches': [('PY%dASTOK' % astversion, ())]
            })
            if py2_err:
                retdict['py2_ast_errors'].append(py2_err)
            if py3_err:
                retdict['py3_ast_errors'].append(py3_err)

            # One parsed and the other didnt, no need to continue checking
            if astversion in (2, 3):
                retdict['version'] = astversion
                continue

        # Remove comments and emptyfy strings before doing the regex tests,
        # this will remove most fase positives
        cleaned_code = remove_str_comments(input_code)

        if modules_checks:
            apply_score(*check_syntax_regex(cleaned_code, retdict['matches']))
            apply_score(*check_modules_regex(cleaned_code, retdict['matches'],
                match_score = modules_score))

        # This one is SLOOOOOW
        if modsyms_checks:
            apply_score(
                *check_modulesymbols_regex(cleaned_code, retdict['matches'], symbols_score)
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


if __name__ == '__main__':
    from pprint import pprint
    with open('detector.py') as f:
        code = f.read()
    pprint(detect(codestr=code, stop_on_ok_ast=False))
