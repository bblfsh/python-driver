package normalizer

import (
	"errors"

	"gopkg.in/bblfsh/sdk.v2/uast"
	"gopkg.in/bblfsh/sdk.v2/uast/nodes"
	"gopkg.in/bblfsh/sdk.v2/uast/role"
	. "gopkg.in/bblfsh/sdk.v2/uast/transformer"
)

var Preprocess = Transformers([][]Transformer{
	{Mappings(
		// Move the Leading/TrailingTrivia outside of nodes.
		//
		// This cannot be inside Normalizers because it should precede any
		// other transformation.
		Map(
			opMoveCommentsAnns{Var("group")},
			Check(Has{uast.KeyType: String(typeGroup)}, Var("group")),
		),
	)},
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
			// Will be filled only if there is a Python3 type annotation
			"returns":        Var("returns"),
			"decorator_list": Var("func_decorators"),
		},
		Obj{
			"Nodes": Arr(
				Obj{
					// FIXME: generator=true if it uses yield anywhere in the body
					"async": Bool(async),
				},
				Obj{
					"decorators": Var("func_decorators"),
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
							"Returns":   Var("returns"),
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
			})},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
	)
}

var (
	typeGroup     = uast.TypeOf(uast.Group{})
	typeFuncGroup = uast.TypeOf(uast.FunctionGroup{})
)

// Similar (but not equal) to:
// https://github.com/bblfsh/csharp-driver/blob/master/driver/normalizer/normalizer.go#L827
// Should be removed once we have some generic solution in the SDK
type opMoveCommentsAnns struct {
	sub Op
}

func (op opMoveCommentsAnns) Kinds() nodes.Kind {
	return nodes.KindObject
}

func (op opMoveCommentsAnns) Check(st *State, n nodes.Node) (bool, error) {
	obj, ok := n.(nodes.Object)
	if !ok {
		return false, nil
	}
	modified := false
	noops_prevs, ok1 := obj["noops_previous"].(nodes.Array)
	noops_same, ok2 := obj["noops_sameline"].(nodes.Array)
	//decorators, ok3 := obj["decorator_list"].(nodes.Array)

	if ok1 || ok2 {
		// we saved the comments and decorators, remove from them from this node
		obj = obj.CloneObject()
		modified = true
		delete(obj, "noops_previous")
		delete(obj, "noops_sameline")
		//delete(obj, "decorator_list")
	}

	if len(noops_prevs) == 0 || len(noops_same) == 0 {
		if !modified {
			return false, nil
		}
		return op.sub.Check(st, obj)
	}

	arr := make(nodes.Array, 0, len(noops_prevs) + 1 + len(noops_same))
	arr = append(arr, noops_prevs...)
	arr = append(arr, obj)
	arr = append(arr, noops_same)
	group, err := uast.ToNode(uast.Group{})
	if err != nil {
		return false, err
	}

	obj = group.(nodes.Object)
	obj["Nodes"] = arr
	return op.sub.Check(st, obj)
}

func (op opMoveCommentsAnns) Construct(st *State, n nodes.Node) (nodes.Node, error) {
	// TODO(dennwc): implement when we will need a reversal
	//				 see https://github.com/bblfsh/sdk/issues/355
	return op.sub.Construct(st, n)
}

// opMergeGroups finds the uast:Group nodes and merges them into a child
// uast:FunctionGroup, if it exists.
//
// This transform is necessary because opMoveTrivias will wrap all nodes that contain trivia
// into a Group node, and the same will happen with MethodDeclaration nodes. But according
// to a UAST schema defined in SDK, the comments (trivia) should be directly inside the
// FunctionGroup node that wraps functions in Semantic mode.
type opMergeGroups struct {
	sub Op
}

func (op opMergeGroups) Kinds() nodes.Kind {
	return nodes.KindObject
}


// firstWithType returns an index of the first node type of which matches the filter function.
func firstWithType(arr nodes.Array, fnc func(typ string) bool) int {
	for i, sub := range arr {
		if fnc(uast.TypeOf(sub)) {
			return i
		}
	}
	return -1
}

// Check tests if the current node is uast:Group and if it contains a uast:FunctionGroup
// node, it will remove the current node and merge other children into the FunctionGroup.
func (op opMergeGroups) Check(st *State, n nodes.Node) (bool, error) {
	group, ok := n.(nodes.Object)
	if !ok || uast.TypeOf(group) != typeGroup {
		return false, nil
	}
	arr, ok := group["Nodes"].(nodes.Array)
	if !ok {
		return false, errors.New("expected an array in Group.Nodes")
	}
	ind := firstWithType(arr, func(typ string) bool {
		return typ == typeFuncGroup
	})
	if ind < 0 {
		return false, nil
	}
	leading := arr[:ind]
	fgroup := arr[ind].(nodes.Object)
	trailing := arr[ind+1:]

	arr, ok = fgroup["Nodes"].(nodes.Array)
	if !ok {
		return false, errors.New("expected an array in Group.Nodes")
	}
	out := make(nodes.Array, 0, len(leading)+len(arr)+len(trailing))
	out = append(out, leading...)
	out = append(out, arr...)
	out = append(out, trailing...)

	fgroup = fgroup.CloneObject()
	fgroup["Nodes"] = out

	return op.sub.Check(st, fgroup)
}

func (op opMergeGroups) Construct(st *State, n nodes.Node) (nodes.Node, error) {
	// TODO(dennwc): implement when we will need a reversal
	//				 see https://github.com/bblfsh/sdk/issues/355
	return op.sub.Construct(st, n)
}

var Normalizers = []Mapping{

	// Box Names, Strings, Attributes, ImportFroms and Bools into a "BoxedFoo" moving the real node to the
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

	Map(
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoolLiteral")},
			{Name: uast.KeyPos, Op: Var("pos_")},
			{Name: "value", Op: Var("lv")},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoxedBoolLiteral")},
			{Name: "boxed_value", Op: UASTType(uast.Bool{}, Obj{
				uast.KeyPos: Var("pos_"),
<<<<<<< HEAD
				"Value":     Var("lv"),
||||||| merged common ancestors
				"Value": Var("lv"),
=======
				"Value":     Var("lv"),
			})},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
	),

	Map(
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("Attribute")},
			{Name: uast.KeyPos, Op: Var("pos_")},
			{Name: "attr", Op: Var("aname")},
			{Name: "ctx", Op: Any()},
			{Name: "noops_previous", Optional: "np_opt", Op: Var("noops_previous")},
			{Name: "noops_sameline", Optional: "ns_opt", Op: Var("noops_sameline")},
		}),
		Part("_", Fields{
			{Name: uast.KeyType, Op: String("BoxedAttribute")},
			{Name: "boxed_value", Op: UASTType(uast.Identifier{}, Obj{
				uast.KeyPos: Var("pos_"),
				"Name":      Var("aname"),
>>>>>>> Checkpoint with the C# like transform
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

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
			"ctx":         Any(),
		},
		Obj{
			"Name": identifierWithPos("name"),
			"Init": Var("init"),
		},
	)),

	MapSemantic("arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"ctx":         Any(),
		},
		Obj{
			"Name": identifierWithPos("name"),
		},
	)),

	MapSemantic("kwonly_arg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			"default":     Var("init"),
			// TODO: change this once we've a way to store other nodes on semantic objects
			"annotation": Any(),
		},
		Obj{
			"Init": Var("init"),
			"Name": identifierWithPos("name"),
		},
	)),

	MapSemantic("vararg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			// TODO: change this once we've a way to store other nodes on semantic objects
			"annotation": Any(),
		},
		Obj{
			"Name":     identifierWithPos("name"),
			"Variadic": Bool(true),
		},
	)),

	MapSemantic("kwarg", uast.Argument{}, MapObj(
		Obj{
			uast.KeyToken: Var("name"),
			// TODO: change this once we've a way to store other nodes on semantic objects
			"annotation": Any(),
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

	// Merge uast:Group with uast:FunctionGroup.
	Map(
		opMergeGroups{Var("group")},
		Check(Has{uast.KeyType: String(uast.TypeOf(uast.FunctionGroup{}))}, Var("group")),
	),
}
