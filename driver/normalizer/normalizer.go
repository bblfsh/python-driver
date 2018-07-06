package normalizer

import (
	"gopkg.in/bblfsh/sdk.v2/uast"
	"gopkg.in/bblfsh/sdk.v2/uast/role"
	. "gopkg.in/bblfsh/sdk.v2/uast/transformer"
)

var Preprocess = Transformers([][]Transformer{
	{Mappings(Preprocessors...)},
}...)

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

var Normalizers = []Mapping{
	MapSemantic("Str", uast.String{}, MapObj(
		Obj{
			"s": Var("val"),
		},
		Obj{
			"Value":  Var("val"),
			"Format": String(""),
		},
	)),

	MapSemantic("Bytes", uast.String{}, MapObj(
		Obj{
			"s": Var("val"),
		},
		Obj{
			"Value":  Var("val"),
			"Format": String(""),
		},
	)),

	MapSemantic("StringLiteral", uast.String{}, MapObj(
		Obj{
			"s": Var("val"),
		},
		Obj{
			"Value":  Var("val"),
			"Format": String(""),
		},
	)),

	MapSemantic("Name", uast.Identifier{}, MapObj(
		Obj{"id": Var("name")},
		Obj{"Name": Var("name")},
	)),

	MapSemantic("Attribute", uast.Identifier{}, MapObj(
		Obj{"attr": Var("name")},
		Obj{"Name": Var("name")},
	)),

	MapSemantic("alias", uast.Alias{}, MapObj(
		Obj{
			"name":   Var("name"),
			"asname": Var("aliased"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
			"Node": UASTType(uast.Identifier{}, Obj{
				"Name": Var("aliased"),
			}),
		},
	)),

	MapSemantic("Name", uast.Identifier{}, MapObj(
		Obj{"attr": Var("name")},
		Obj{"Name": Var("name")},
	)),

	MapSemantic("NoopLine", uast.Comment{}, MapObj(
		Obj{"noop_line": CommentText([2]string{}, "comm")},
		CommentNode(false, "comm", nil),
	)),

	MapSemantic("NoopSameLine", uast.Comment{}, MapObj(
		Obj{"s": CommentText([2]string{}, "comm")},
		CommentNode(false, "comm", nil),
	)),

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
			"Init": Var("init"),
		},
	)),

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
		},
	)),

	MapSemantic("kwonly_arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
			"Init": Var("init"),
		},
	)),

	MapSemantic("vararg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
			"Variadic": Bool(true),
		},
	)),

	MapSemantic("kwarg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
		},
		Obj{
			"Name": UASTType(uast.Identifier{}, Obj{
				"Name": Var("name"),
			}),
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

	// FIXME: what to do with levels? convert to ../../... in Path?
	// FIXME: "import * from x": check the * and set "All" to true
	//MapSemantic("ImportFrom", uast.RuntimeImport{}, MapObj(
	//	Obj{
	//		"names":  Check(Is(Arr(Any))),
	//		"module": Var("module"),
	//	},
	//	Obj{
	//		"All": Bool(true),
	//		"Path": UASTType(uast.Identifier{}, Obj{
	//			"Name":  Var("module"),
	//		}),
	//	},
	//)),
	MapSemantic("ImportFrom", uast.RuntimeImport{}, MapObj(
		Obj{
			"names":  Var("names"),
			"module": Var("module"),
		},
		Obj{
			"Names": Var("names"),
			"Path": UASTType(uast.Identifier{}, Obj{
				"Name":  Var("module"),
			}),
		},
	)),
}
