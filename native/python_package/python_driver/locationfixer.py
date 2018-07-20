from ast import literal_eval
from copy import deepcopy
from typing import List

from python_driver.base_token import Token, TOKEN_KEYS, SYNTHETIC_TOKENS
from python_driver.types import Node


class TokenNotFoundException(Exception):
    pass


class LocationFixer:
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
                    line_value = literal_eval(t.value[1:])
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
        token_keys = list(node_keyset.intersection(TOKEN_KEYS))

        if token_keys:
            node_token = nodedict[token_keys[0]]
        else:
            node_token = SYNTHETIC_TOKENS.get(nodedict["ast_type"])
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

