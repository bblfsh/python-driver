package normalizer

import "gopkg.in/bblfsh/sdk.v1/uast"

// ToNode is an instance of `uast.ObjectToNode`, defining how to transform an
// into a UAST (`uast.Node`).
//
// https://godoc.org/gopkg.in/bblfsh/sdk.v1/uast#ObjectToNode
var ToNode = &uast.ObjectToNode{
	InternalTypeKey: "ast_type",
	LineKey:         "lineno",
	EndLineKey:      "end_lineno",
	ColumnKey:       "col_offset",
	EndColumnKey:    "end_col_offset",

	TokenKeys: map[string]bool{
		"name": true,
		//"asname":          true, // Alias from ImportFrom
		"id":           true, // Name nodes
		"attr":         true, // something.attr
		"arg":          true, // function arguments
		"LiteralValue": true, // boolean/None literal
		"s":            true, // string/byte
		"n":            true, // numeric literal
		"noop_line":    true, // Comment/Noop (non significative whitespace)
	},
	SyntheticTokens: map[string]string{
		"Add":       "+",
		"Assert":    "assert",
		"AugAssign": "?=",
		"BitAnd":    "&",
		"BitOr":     "|",
		"BitXor":    "^",
		"Break":     "break",
		"Continue":  "continue",
		"Delete":    "delete",
		"Div":       "/",
		"Ellipsis":  "...",
		"Eq":        "==",
		"For":       "for",
		"FloorDiv":  "//",
		"Global":    "global",
		"Gt":        ">",
		"GtE":       ">=",
		"If":        "if",
		"In":        "in",
		"Invert":    "~",
		"Is":        "is",
		"IsNot":     "not is",
		"LShift":    "<<",
		"Lt":        "<",
		"LtE":       "<=",
		"Mod":       "%%",
		"Mult":      "*",
		"Nonlocal":  "nonlocal",
		"Not":       "!",
		"NotEq":     "!=",
		"NotIn":     "not in",
		"Pass":      "pass",
		"Pow":       "**",
		"Print":     "print",
		"Raise":     "raise",
		"Return":    "return",
		"RShift":    ">>",
		"Sub":       "-",
		"UAdd":      "+",
		"USub":      "-",
		"While":     "while",
		"With":      "with",
		"Yield":     "yield",
	},
	PromoteAllPropertyLists: false,
	PromotedPropertyLists: map[string]map[string]bool{
		"If":       {"body": true, "orelse": true},
		"For":      {"body": true, "orelse": true},
		"AsyncFor": {"body": true, "orelse": true},
		"While":    {"body": true, "orelse": true},
		"Compare":  {"comparators": true, "ops": true},
		// FIXME: check call.keywords
		//"Call"                    : { "args": true, "keywords": true},
		"With":        {"body": true, "items": true},
		"FunctionDef": {"body": true, "decorator_list": true},
		"Lambda":      {"body": true},
		"arguments":   {"defaults": true},
		"Try":         {"body": true, "orelse": true, "finalbody": true},
		"Raise":       {"args": true},
		"ClassDef":    {"body": true, "bases": true, "decorator_list": true, "keywords": true},
	},
	PromotedPropertyStrings: map[string]map[string]bool{
		"alias":         {"asname": true},
		"ImportFrom":    {"module": true},
		"ExceptHandler": {"name": true},
	},
	// FIXME: test[ast_type=Compare].comparators is a list?? (should be "right")
}
