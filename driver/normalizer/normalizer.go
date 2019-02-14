package normalizer

import (
	"gopkg.in/bblfsh/sdk.v2/uast"
	"gopkg.in/bblfsh/sdk.v2/uast/role"
	. "gopkg.in/bblfsh/sdk.v2/uast/transformer"
)

var Preprocess = Transformers([][]Transformer{
	{Mappings(Preprocessors...)},
}...)

var PreprocessCode = []CodeTransformer{}

var Preprocessors = []Mapping{
	ObjectToNode{
		InternalTypeKey: "ast_type",
		LineKey:         "lineno",
		ColumnKey:       "col_offset",
		EndLineKey:      "end_lineno",
		EndColumnKey:    "end_col_offset",
	}.Mapping(),
}

var Normalize = Transformers([][]Transformer{
	{Mappings(Normalizers...)},
}...)

func funcDefMap(typ string, async bool) Mapping {
	return MapSemantic(typ, uast.FunctionGroup{}, MapObj(
		Obj{
			"body": Var("body"),
			"name": Var("name"),
			// Arguments should be converted by the uast.Arguments normalization
			"args": Obj{
				"args":       Var("arguments"),
				uast.KeyPos:  Var("_pos"),
				uast.KeyType: Var("_type"),
			},
		},
		Obj{
			"Nodes": Arr(
				Obj{
					// FIXME: generator=true if it uses yield anywhere in the body
					"async": Bool(async),
				},
				UASTType(uast.Alias{}, Obj{
					// FIXME: can't call identifierWithPos because it would take the position of the
					// function node that is not exactly the same as the position of the function name
					"Name": UASTType(uast.Identifier{}, Obj{
						"Name": Var("name"),
					}),
					"Node": UASTType(uast.Function{}, Obj{
						"Type": UASTType(uast.FunctionType{}, Obj{
							"Arguments": Var("arguments"),
						}),
						"Body": UASTType(uast.Block{}, Obj{
							"Statements": Var("body"),
						}),
					}),
				}),
			),
		},
	))
}

func identifierWithPos(nameVar string) ObjectOp {
	return UASTType(uast.Identifier{}, Obj{
		uast.KeyPos: UASTType(uast.Positions{}, Obj{
			uast.KeyStart: Var(uast.KeyStart),
			uast.KeyEnd:   Var(uast.KeyEnd),
		}),
		"Name": Var(nameVar),
	})
}

// mapStr factorizes the common annotation for string types (Byte, Str, StrLiteral)
func mapStr(nativeType string) Mapping {
	return Map(
		Part("_", Fields{
			{Name: uast.KeyType, Op: String(nativeType)},
			{Name: uast.KeyPos, Op: Var("pos_")},
			{Name: "s", Op: Var("s")},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("Boxed" + nativeType)},
			{Name: "boxed_value", Op: UASTType(uast.String{}, Obj{
				uast.KeyPos: Var("pos_"),
				"Value":     Var("s"),
				//"Format":    String(""),
			})},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
	)
}

var Normalizers = []Mapping{

	// Box Names, Strings, and Bools into a "BoxedFoo" moving the real node to the
	// "value" property and keeping the comments in the parent (if not, comments would be lost
	// when promoting the objects)
	Map(
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("Name")},
			{Name: uast.KeyPos, Op: Var("pos_")},
			{Name: "id", Op: Var("id")},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoxedName")},
			{Name: "boxed_value", Op: UASTType(uast.Identifier{}, Obj{
				uast.KeyPos: Var("pos_"),
				"Name":      Var("id"),
			})},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
	),

	// TODO: uncomment after SDK 2.13.x update
	//  (upgrade currently blocked by: https://github.com/bblfsh/sdk/issues/353)
	Map(
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoolLiteral")},
			{Name: uast.KeyPos, Op: Var("pos_")},
			//{Name: "LiteralValue", Op: Var("lv")},
			{Name: "value", Op: Var("lv")},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoxedBoolLiteral")},
			{Name: "boxed_value", Op: UASTType(uast.Bool{}, Obj{
				uast.KeyPos: Var("pos_"),
				"Value":     Var("lv"),
			})},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
	),

	mapStr("Bytes"),
	mapStr("Str"),
	mapStr("StringLiteral"),

	MapSemantic("NoopLine", uast.Comment{}, MapObj(
		Obj{
			"noop_line": CommentTextTrimmed([2]string{"#", ""}, "comm"),
		},
		CommentNode(false, "comm", nil),
	)),

	MapSemantic("NoopSameLine", uast.Comment{}, MapObj(
		Obj{
			"s": CommentText([2]string{"#", ""}, "comm"),
		},
		CommentNode(false, "comm", nil),
	)),

	// FIXME: no positions for keywords in the native AST
	AnnotateType("keyword", MapObj(
		Fields{
			{Name: "arg", Op: Var("name")},
		},
		Fields{
			{Name: "arg",
				Op: UASTType(uast.Identifier{}, Obj{
					"Name": Var("name"),
				})},
		}),
		role.Name),

	MapSemantic("Attribute", uast.Identifier{}, MapObj(
		Obj{"attr": Var("name")},
		Obj{"Name": Var("name")},
	)),

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
		},
		Obj{
			"Name": identifierWithPos("name"),
			"Init": Var("init"),
		},
	)),

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name": identifierWithPos("name"),
		},
	)),

	MapSemantic("kwonly_arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
		},
		Obj{
			"Init": Var("init"),
			"Name": identifierWithPos("name"),
		},
	)),

	MapSemantic("vararg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name":     identifierWithPos("name"),
			"Variadic": Bool(true),
		},
	)),

	MapSemantic("kwarg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name": identifierWithPos("name"),
		    "MapVariadic": Bool(true),
		},
	)),

	funcDefMap("FunctionDef", false),
	funcDefMap("AsyncFunctionDef", true),

	AnnotateType("Import", MapObj(
		Obj{
			"names": Each("vals", Var("name")),
		},
		Obj{
			"names": Each("vals", UASTType(uast.RuntimeImport{},
				Obj{
					"Path": Var("name"),
				})),
		},
	), role.Import, role.Declaration, role.Statement),

	// FIXME: aliases doesn't have a position (can't be currently fixed by the tokenizer
	// because they don't even have a line in the native AST)
	MapSemantic("alias", uast.Alias{}, MapObj(
		Obj{
			"name": Var("name"),
			"asname": Cases("case_alias",
				Check(Is(nil), Var("nilalias")),
				Check(Not(Is(nil)), Var("alias")),
			),
		},
		CasesObj("case_alias",
			Obj{
				"Name": UASTType(uast.Identifier{}, Obj{
					"Name": Var("name"),
				}),
			},
			Objs{
				{"Node": Obj{}},
				{
					"Node": UASTType(uast.Identifier{}, Obj{"Name": Var("alias")}),
				}},
		))),

	// Star imports
	MapSemantic("ImportFrom", uast.RuntimeImport{}, MapObj(
		Obj{
			"names": Arr(
				Obj{
					uast.KeyType: String("uast:Alias"),
					uast.KeyPos:  Var("pos"),
					"Name": Obj{
						uast.KeyType: String("uast:Identifier"),
						"Name":       String("*"),
					},
					"Node": Obj{},
				},
			),
			"level":  Var("level"),
			"module": Var("module"),
		},
		Obj{
			"All": Bool(true),
			"Path": UASTType(uast.Identifier{}, Obj{
				"Name": OpPrependPath{
					// FIXME: no position for the module (path) in the native AST, only when the import starts
					numLevel: Var("level"),
					path:     Var("module"),
					joined:   Var("joined"),
					prefix:   "../",
				},
			}),
		},
	)),

	MapSemantic("ImportFrom", uast.RuntimeImport{}, MapObj(
		Obj{
			"names":  Var("names"),
			"module": Var("module"),
			"level":  Var("level"),
		},
		Obj{
			"Names": Var("names"),
			"Path": UASTType(uast.Identifier{}, Obj{
				"Name": OpPrependPath{
					numLevel: Var("level"),
					path:     Var("module"),
					joined:   Var("joined"),
					prefix:   "../",
				},
			}),
		},
	)),
}
