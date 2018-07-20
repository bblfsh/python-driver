import token as token_module
from typing import Tuple, Iterable, List


TOKEN_KEYS = set(
    ("module", "name", "id", "attr", "arg", "LiteralValue", "s", "n")
)

SYNTHETIC_TOKENS = {
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


def create_tokenized_lines(codestr: str, tokens: Iterable[Token]) -> List[List[Token]]:
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
