import token as token_module
from typing import List, Set, Optional, Dict, Tuple

from python_driver.base_token import Token
from python_driver.types import Node

NOOP_TOKENS_LINE = {'COMMENT', 'INDENT', 'NL', 'NEWLINE'}


class NoopExtractor():
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

        def new_noopline(s: str) -> Dict[str, str]:
            return {"ast_type": "NoopSameLine", "s": s}

        noop_lines = [new_noopline(i.value.strip()) for i in noops_sameline]

        if noops_sameline:
            node['noops_sameline'] = {
                "ast_type": "SameLineNoops",
                "lineno": node.get("lineno", 0),
                "col_offset": noops_sameline[0].start.col,
                "noop_lines": noop_lines,
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
