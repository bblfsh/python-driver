package normalizer

import (
	"gopkg.in/bblfsh/sdk.v2/uast"
	"gopkg.in/bblfsh/sdk.v2/uast/nodes"
	. "gopkg.in/bblfsh/sdk.v2/uast/transformer"
)

var Preprocess = Transformers([][]Transformer{
	{Mappings(Preprocessors...)},
}...)

var Preprocessors = []Mapping{
	ObjectToNode{
		InternalTypeKey: "ast_type",
		// FIXME: restore once positions are working again
		// LineKey:         "lineno",
		// ColumnKey:       "col_offset",
		// EndLineKey:      "end_lineno",
		// EndColumnKey:    "end_col_offset",
	}.Mapping(),
}

var Normalize = Transformers([][]Transformer{
	{Mappings(Normalizers...)},
}...)

type opFuncArguments struct {
	args Op
}

func (op opFuncArguments) Kinds() nodes.Kind {
	return nodes.KindArray
}

func (op opFuncArguments) Check(st *State, n nodes.Node) (bool, error) {
	v, ok := n.(nodes.Array)
	if !ok {
		return false, nil
	}

	return op.args.Check(st, v)
}

func (op opFuncArguments) Construct(st *State, n nodes.Node) (nodes.Node, error) {
	// Iterate over n.args constructing Arguments. Set the arg.Init to the values
	// in n.defaults. Do the same for kwonlyargs/kw_defaults. Finally add vararg
	// and kwargs if they are set
	n, err := op.args.Construct(st, n)

	if err != nil {
		return nil, err
	}

	// FIXME: implement

	return n, nil
}

// FIXME: decorators? (annotations/tags)
// FIXME: in Python, an argument being variadic or not depends on being on
// args.[kwonlyargs|args] or plain "args" not on any property of the argument
// nodes themselves. Check with @dennys about how to map this.
func funcDefMap(typ string, async bool) Mapping {
	return MapSemantic(typ, uast.FunctionGroup{}, MapObj(
		Obj{
			"body": Var("body"),
			"name": Var("name"),
			"args": Obj{
				"args": Each("normal_args", Var("normal_arg_name")),
				"kwonlyargs": Each("kw_args",
					Obj{
						"arg":   Var("kwarg_name"),
						"value": Var("kwarg_default"),
					}),
				"varargs": Var("varargs"),
			},
		},
		Obj{
			"Nodes": Arr(
				Obj{
					// FIXME: generator=true if it uses yield anywhere in the body
					"async": Bool(async),
				},
				UASTType(uast.Alias{}, Obj{
					"Name": Var("name"),
					"Node": UASTType(uast.Function{}, Obj{
						"Type": UASTType(uast.FunctionType{}, Obj{
							"Arguments": Var("args"),
						}),
						"Body": Var("body"),
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

	// FIXME: check that the identifiers are in the right order
	MapSemantic("Attribute", uast.QualifiedIdentifier{}, MapObj(
		Obj{"value": Var("identifiers")},
		Obj{"Names": Var("identifiers")},
	)),

	MapSemantic("NoopLine", uast.Comment{}, MapObj(
		Obj{"noop_line": CommentText([2]string{"#", ""}, "comm")},
		CommentNode(false, "comm", nil),
	)),

	MapSemantic("NoopSameLine", uast.Comment{}, MapObj(
		Obj{"s": CommentText([2]string{"#", ""}, "comm")},
		CommentNode(false, "comm", nil),
	)),

	funcDefMap("FunctionDef", false),
	funcDefMap("AsyncFunctionDef", true),

	MapSemantic("Import", uast.RuntimeImport{}, MapObj(
		Obj{
			"names": Var("names"),
		},
		Obj{
			"Names": Var("names"),
		},
	)),

	// FIXME: what to do with levels? convert to ../../... in Path?
	// FIXME: Import rename (import x as y)
	// FIXME: "import * from x": check the * and set "All" to true
	MapSemantic("ImportFrom", uast.RuntimeImport{}, MapObj(
		Obj{
			"names":  Var("names"),
			"module": Var("module"),
		},
		Obj{
			"Names": Var("names"),
			"Path":  Var("module"),
		},
	)),
}
