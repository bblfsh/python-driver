package normalizer

import (
	"github.com/bblfsh/sdk/uast"
)

var NativeToNoder = &uast.BaseToNoder{
	InternalTypeKey: "ast_type",
	LineKey:         "lineno",
	ColumnKey:       "col_offset",

	TokenKeys: map[string]bool{
		"module":            true, // Module on ImportFrom
		"name":              true,
		//"asname":            true, // Alias from ImportFrom
		"id":                true, // Name nodes
		"attr":              true, // something.attr
		"arg":               true, // function arguments
		"LiteralValue":      true, // string/num/byte/constant literal
		"noop_line":         true, // Comment/Noop (non significative whitespace)
	},
	SyntheticTokens: map[string]string{
		"Print":              "print",
	},
}
