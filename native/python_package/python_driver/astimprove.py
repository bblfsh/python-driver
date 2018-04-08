"""
Improve the basic AST, taken in dictionary form as exported
from the import pydetector module.
"""

import token as token_module
import tokenize
from ast import literal_eval
from codecs import encode
from copy import deepcopy
from io import BytesIO
from typing import Iterable, List, Dict, Tuple, Any, Union, \
        Set, cast, Optional

__all__ = ["AstImprover"]

NOOP_TOKENS_LINE = {'COMMENT', 'INDENT', 'NL', 'NEWLINE'}

Pos = Tuple[int, int]
Node = Dict[str, Any]
AstDict = Dict[Any, Any]
VisitResult = Union[Node, List[Node]]


class TokenPos():
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col


class Token():
    def __init__(self, type_: int, value: str, start: Tuple[int, int],
            end: Tuple[int, int], rawvalue: str) -> None:
        self.type = type_
        self.name = token_module.tok_name[type_]
        self.value = value
        self.start = TokenPos(*start)
        self.end = TokenPos(*end)
        self.rawvalue = rawvalue

    def __str__(self) -> str:
        s = '%s, %s, %s' % (self.type, self.name, self.value)
        s += '\n%d %d' % (self.start.row, self.start.col)
        s += '\n%d %d' % (self.end.row, self.end.col)
        return s


def _create_tokenized_lines(codestr: str, tokens: Iterable[Token]) -> List[List[Token]]:
    lines = codestr.splitlines() if codestr else []
    result: List[List[Token]] = []
    for i in range(0, len(lines) + 1):
        result.append([])

    for token in tokens:
        # Save noops in the line of the starting row except for strings where
        # we save it in the last line (because they can be multiline)
        if token.name == 'STRING':
            line = token.end.row - 1
        else:
            line = token.start.row - 1
        result[line].append(token)
    assert len(lines) + 1 == len(result), len(result)
    return result


class TokenNotFoundException(Exception):
    pass


class LocationFixer(object):
    """
    For every line, get the exact position of every token. This will be used by the
    visitor to fix the position of some nodes that the Python's AST doesn't give or give
    in a questionable way (sys.stdout.write -> gives the same column for the three).
    """

    def __init__(self, codestr: str, token_lines: List[List[Token]]) -> None:
        self._current_line = -1

        # _lines will initially hold the same list of tokens per line as received (in a
        # dict so speed lookups), but the tokens inside will be removed as they're found
        # by the visitor (so we still can infer real positions for several tokens with the
        # same name on the same line)
        self._lines = {idx: val for idx, val in enumerate(token_lines)}

    def _pop_token(self, lineno: int, token_value: str) -> Token:
        tokensline = self._lines[lineno - 1]

        # Pop the first token with the same name in the same line
        for t in tokensline:

            if t.name != 'STRING':
                line_value = t.value
            else:
                if t.value[0] == 'f' and t.value[1] in ('"', "'"):
                    # fstring: token identify as STRING but they parse into the AST as a
                    # collection of nodes so the token_value is  different. To find the
                    # real token position we'll search  inside the fstring token value.
                    tok_subpos = t.value.find(str(token_value))
                    if tok_subpos != -1:

                        # We don't remove the fstring token from the line in this case; other
                        # nodes could match different parts of it
                        newtok = deepcopy(t)
                        newtok.start.col = t.start.col + tok_subpos
                        return newtok

                    raise TokenNotFoundException("Could not find token '{}' inside f-string '{}'"
                            .format(token_value, t.value))
                else:
                    # normal string; they include the single or double quotes so we liteval
                    line_value = literal_eval(t.value)

            if str(line_value) == str(token_value):
                tokensline.remove(t)
                return t

        raise TokenNotFoundException("Token named '{}' not found in line {}"
                .format(token_value, lineno))

    def sync_node_pos(self, nodedict: Node) -> None:
        """
        Check the column position, updating the column if needed (this changes the
        nodedict argument). Some Nodes have questionable column positions in the Python
        given AST (e.g. all items in sys.stdout.write have column 1). This fixes if the
        linenumber is right, using the more exact position given by the tokenizer.

        When a node is checked, it's removed from its line list, so the next token with
        the same name will not consume that token again (except for fstrings that are
        a special case of a token mapping to several possible AST nodes).
        """
        node_line = nodedict.get('lineno')
        if node_line is None:
            return

        # We take these node properties as token name if they exists
        # (same used in the Bblfsh Python driver parser.go):
        node_keyset = set(nodedict.keys())
        token_keys = list(node_keyset.intersection(_TOKEN_KEYS))

        if token_keys:
            node_token = nodedict[token_keys[0]]
        else:
            node_token = _SYNTHETIC_TOKENS.get(nodedict["ast_type"])
            if not node_token:
                return  # token not found
        try:
            # Pop the fist token with the same name in the same line.
            token = self._pop_token(node_line, node_token)
        except TokenNotFoundException:
            # Only happens with multiline string and the original
            # position in that case is fine (uses the last line in that case)
            return

        if nodedict['ast_type'] != 'ImportFrom':
            # ImportFrom takes the module as token, we don't want that position, default
            # is fine
            nodedict["lineno"] = token.start.row
            nodedict["col_offset"] = token.start.col
        nodedict["end_lineno"] = token.end.row
        nodedict["end_col_offset"] = token.end.col


class NoopExtractor(object):
    """
    Extract lines with tokens from the tokenized source that Python's AST generator ignore
    like blanks and comments.
    """

    def __init__(self, codestr: str, token_lines: List[List[Token]]) -> None:
        self._current_line = -1
        self._all_lines = tuple(token_lines)
        self.astmissing_lines = self._create_astmissing_lines()

        # This set is used to avoid adding the "same line-remainder noops" nodes as a child
        # of every "real" node to avoid having this node duplicated on all semantic
        # nodes in the same line, thus avoiding duplication. It will contain just the
        # line numbers of already added sameline_noops
        self._sameline_added_noops: Set[int] = set()

    def _create_astmissing_lines(self) -> List[Optional[Token]]:
        """
        Return a copy of line_tokens containing lines ignored by the AST
        (comments and blanks-only lines)
        """
        lines: List[Optional[Token]] = []
        nl_token = Token(token_module.NEWLINE, '\n', (0, 0), (0, 0), '\n')

        for i, linetokens in enumerate(self._all_lines):
            if len(linetokens) == 1 and linetokens[0].name == 'NL':
                lines.append(nl_token)
            else:
                for token in linetokens:
                    if token.name == 'COMMENT' and \
                            token.rawvalue.lstrip().startswith('#'):
                        lines.append(token)
                        break
                else:
                    lines.append(None)
        assert len(lines) == len(self._all_lines)

        for i, linetokens2 in enumerate(lines):
            if linetokens2:
                self._current_line = i
                break
        else:
            self._current_line = len(lines)
        return lines

    def add_noops(self, node: Node, isRoot: bool) -> None:
        if not isinstance(node, dict):
            return

        def _create_nooplines_list(startline: int, noops_previous: List[str]) -> List[Node]:
            nooplines: List[Node] = []
            curline = startline
            for noopline in noops_previous:
                if noopline != '\n':
                    if noopline.lstrip().startswith('#'):
                        noopline = noopline.lstrip()[1:]

                    nooplines.append({
                        "ast_type": "NoopLine",
                        "noop_line": noopline,
                        "lineno": curline,
                        "col_offset": 1,
                    })
                curline += 1
            return nooplines

        # Add all the noop (whitespace and comments) lines between the
        # last node and this one
        noops_previous, startline, endline, endcol = self.previous_nooplines(node)
        if noops_previous:
            node['noops_previous'] = {
                "ast_type": "PreviousNoops",
                "lineno": startline,
                "col_offset": 1,
                "end_lineno": endline,
                "end_col_offset": max(endcol, 1),
                "lines": _create_nooplines_list(startline, noops_previous)
            }

        # Other noops at the end of its significative line except the implicit
        # finishing newline
        noops_sameline: List[Token] = [i for i in self.sameline_remainder_noops(node) if i]

        joined_sameline = []
        for tok in noops_sameline:
            if tok.value.lstrip().startswith('\n'):
                joined_sameline.append(tok.value.lstrip()[1:])
            else:
                joined_sameline.append(tok.value)

        if noops_sameline:
            node['noops_sameline'] = {
                "ast_type": "SameLineNoops",
                "lineno": node.get("lineno", 0),
                "col_offset": noops_sameline[0].start.col,
                "noop_line": joined_sameline,
                "end_lineno": node.get("lineno", 0),
                "end_col_offset": max(noops_sameline[-1].end.col, 1)
            }

        # Finally, if this is the root node, add all noops after the last op node
        if isRoot:
            noops_remainder, startline, endline, endcol = self.remainder_noops()
            if noops_remainder:
                node['noops_remainder'] = {
                    "ast_type": "RemainderNoops",
                    "lineno": startline,
                    "col_offset": 1,
                    "end_lineno": endline,
                    "end_col_offset": max(endcol, 1),
                    "lines": _create_nooplines_list(startline, noops_remainder)
                    }

    def previous_nooplines(self, nodedict: Node) -> Tuple[List[str], int, int, int]:
        """Return a list of the preceding comment and blank lines"""
        previous = []
        first_lineno = -1
        lastline = -1
        lastcol = -1
        lineno = nodedict.get('lineno')

        if lineno and self.astmissing_lines:
            while self._current_line < lineno:
                token = self.astmissing_lines[self._current_line]
                if token:
                    s = token.rawvalue.rstrip() + '\n'
                    previous.append(s)

                    # take only the first line of the noops as the start and the last
                    # one (overwriteen every iteration)
                    if first_lineno == -1:
                        first_lineno = self._current_line + 1
                    lastline = self._current_line + 1
                    lastcol = token.end.col
                self._current_line += 1
        return previous, first_lineno, lastline, lastcol

    def sameline_remainder_noops(self, nodedict: Node) -> List[Token]:
        """
        Return a list containing the trailing (until EOL) noop Tokens for the
        node, if any. The ending newline is implicit and thus not returned
        """

        # Without a line number for the node we can't know
        lineno = nodedict.get("lineno")
        if not lineno:
            return []

        # Skip remainder comments already added to a node in this line to avoid every node
        # in the same line having it (which is not conceptually wrong, but not DRY)
        if lineno in self._sameline_added_noops:
            return []

        # Module nodes have the remaining comments but since we put their first line as "1"
        # any comment on the first line would wrongly show as sameline comment for the module
        if nodedict["ast_type"] == 'Module':
            return []

        tokens = self._all_lines[lineno - 1]
        trailing: List[Token] = []

        for token in tokens:
            if token.name not in NOOP_TOKENS_LINE:
                # restart
                trailing = []
            else:
                trailing.append(token)

        if not trailing:
            return []

        self._sameline_added_noops.add(lineno)
        nonewline_trailing = trailing[:-1] if trailing[-1].value == '\n' else trailing
        return nonewline_trailing

    def remainder_noops(self) -> Tuple[List[str], int, int, int]:
        """return any remaining ignored lines."""
        trailing: List[str] = []
        lastline = -1
        lastcol = 1

        i = self._current_line
        first_lineno = self._current_line + 1

        while i < len(self.astmissing_lines):
            token = self.astmissing_lines[i]
            i += 1
            if token:
                trailing.append(token.rawvalue)
                lastline = i
                lastcol = token.end.col
            else:
                lastcol = 1
        self._current_line = i
        return trailing, first_lineno, lastline, lastcol


_TOKEN_KEYS = set(
    ("module", "name", "id", "attr", "arg", "LiteralValue", "s", "n")
)

_SYNTHETIC_TOKENS = {
    "Add": "+",
    "Assert": "assert",
    "AugAssign": "+=",
    "BitAnd": "&",
    "BitOr": "|",
    "BitXor": "^",
    "Break": "break",
    "ClassDef": "class",
    "Continue": "continue",
    "Delete": "del",
    "Div": "/",
    "Ellipsis": "...",
    "ExceptHandler": "except",
    "Eq": "==",
    "False": "False",
    "For": "for",
    "FloorDiv": "//",
    "Global": "global",
    "Gt": ">",
    "GtE": ">=",
    "If": "if",
    "In": "in",
    "Invert": "~",
    "Is": "is",
    "IsNot": "not is",
    "Lambda": "lambda",
    "LShift": "<<",
    "Lt": "<",
    "LtE": "<=",
    "Mod": "%%",
    "Mult": "*",
    "None": "None",
    "Nonlocal": "nonlocal",
    "Not": "not",
    "NotEq": "!=",
    "NotIn": "not in",
    "Pass": "pass",
    "Pow": "**",
    "Print": "print",
    "Raise": "raise",
    "Return": "return",
    "RShift": ">>",
    "Sub": "-",
    "True": "true",
    "Try": "try",
    "UAdd": "+",
    "USub": "-",
    "While": "while",
    "With": "with",
    "Yield": "yield",
}


class AstImprover(object):

    def __init__(self, codestr: str, astdict: AstDict) -> None:
        self._astdict = astdict
        # Tokenize and create the noop extractor and the position fixer
        self._tokens: List[Token] = [Token(*i) for i in tokenize.tokenize(BytesIO(codestr.encode('utf-8')).readline)]
        token_lines = _create_tokenized_lines(codestr, self._tokens)
        self.noops_sync = NoopExtractor(codestr, token_lines)
        self.pos_sync   = LocationFixer(codestr, token_lines)
        self.codestr    = codestr

        # This will store a dict of nodes to end positions, it will be filled
        # on parse()
        self._node2endpos = None

        self.visit_Global = self.visit_Nonlocal = self._promote_names

    def parse(self) -> VisitResult:
        res = self.visit(self._astdict, root=True)
        return res

    def visit(self, node: Node, root: bool=False) -> VisitResult:
        # the ctx property always has a "Load"/"Store"/etc dictionary that
        # can be perfectly converted to a string value since they don't
        # hold anything more than the name
        if isinstance(node, dict):
            node_type = node["ast_type"]
            if "ctx" in node:
                node["ctx"] = node["ctx"]["ast_type"]
        else:
            node_type = node.__class__.__name__

        meth = getattr(self, "visit_" + node_type, self.visit_other)
        visit_result = meth(node)
        self.noops_sync.add_noops(node, root)
        self.pos_sync.sync_node_pos(visit_result)

        if not self.codestr:
            # empty files are the only case where 0-indexes are allowed
            visit_result["col_offset"] = visit_result["end_col_offset"] = \
                    visit_result["lineno"] = visit_result["end_lineno"] = 0
        else:
            # Python AST gives a 0 based column for the starting col, bblfsh uses 1-based
            if "col_offset" in visit_result:
                visit_result["col_offset"] = max(visit_result.get("col_offset", 1) + 1, 1)

            if "end_col_offset" in visit_result:
                visit_result["end_col_offset"] = max(visit_result["end_col_offset"], 1)

        visit_result.pop('_fields', None)
        visit_result.pop('_attributes', None)

        return visit_result

    def visit_str(self, node: Node) -> str:
        """
        This visits str fields inside nodes (which are represented as keys
        in the node dictionary), not Str AST nodes
        """
        return str(node)

    def visit_Bytes(self, node: Node) -> VisitResult:
        try:
            s = node["s"].decode()
            encoding = 'utf8'
        except UnicodeDecodeError:
            # try with base64
            s = encode(node["s"], 'base64').decode().strip()
            encoding = 'base64'

        node.update({"s": s, "encoding": encoding})
        return node

    def _promote_names(self, node: Node) -> VisitResult:
        # Python AST by default stores global and nonlocal variable names
        # in a "names" array of strings. That breaks the structure of everything
        # else in the AST (dictionaries, properties or list of objects) so we
        # convert those names to Name objects
        names_as_nodes = [self.visit({"ast_type": "Name",
                                      "id": i,
                                      "lineno": node["lineno"]})
                          for i in node["names"]]

        node["names"] = names_as_nodes
        return node

    def visit_NameConstant(self, node: Node) -> Node:
        if "value" in node:
            repr_val = repr(node["value"])
            if repr_val in ("True", "False"):
                node.update({"LiteralValue": "True" if node["value"] else "False",
                             "ast_type": "BoolLiteral"})
            elif repr_val == "None":
                node = self.visit_NoneType(node)
        else:
            node["ast_type"] = "NameConstant"
        return node

    def visit_Num(self, node: Node) -> Node:
        # complex objects are not json-serializable
        if isinstance(node["n"], complex):
            node.update({"n": {"real": node["n"].real,
                               "imag": node["n"].imag}})
        return node

    def visit_NoneType(self, node: Node) -> Node:
        ret = node if node else {}
        ret.update({"LiteralValue": "None",
                    "ast_type": "NoneLiteral"})
        return ret

    def visit_other(self, node: Node) -> VisitResult:
        for field in node.get("_fields", []):
            meth = getattr(self, "visit_" + node["ast_type"], self.visit_other_field)
            node[field] = meth(node[field])
        return node

    def visit_other_field(self, node: Node) -> VisitResult:
        if isinstance(node, dict):
            return self.visit(node)
        elif isinstance(node, list) or isinstance(node, tuple):
            return [self.visit(x) for x in node]
        else:
            # string attribute
            return node


if __name__ == '__main__':
    import sys
    import importlib.util
    from pprint import pprint

    if len(sys.argv) > 1:
        from pydetector.ast2dict import ast2dict
        codestr = open(sys.argv[1]).read()
        testdict = ast2dict(codestr)
    else:
        codestr = open("../test/fixtures/detector.py").read()
        spec = importlib.util.spec_from_file_location("module.testmod",
                                                      "../test/fixtures/exported_dict.py")
        testmod = importlib.util.module_from_spec(spec)

        if spec.loader:
            spec.loader.exec_module(testmod)
            testdict = testmod.testdict  # type: ignore

    pprint(AstImprover(codestr, testdict).parse())
