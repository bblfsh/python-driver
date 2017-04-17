## Integrations tests to add:

- Different string and string interpolation types (fstrings, format, %, 
  triple-quoted, double/single quoted).

## Driver/SDK bugs:

- PythonDrivers#6: Some nodes with "Col:0": 
    - arguments (parent node, arguments and annotations are fine)

    - triple quoted strings (docstrings) and their parent expression

    - whitespace/comments: PreviousNoops (and their NoopLine children), 
      SameLineNoops, RemainderNoops (and NoopLine).

    - Binary/boolean operators (example: aritmeticopts). The native AST as 
      exported has Line but not column so the problem lies there.

- The integration tests should probably check for nodes in the UAST 
  that doesn't have assigned Roles.

## Missing UAST nodes

### Pending/need research PRs:

- #81: ListComprehension, MapComprehension, SetComprehension
- #79: FunctionDeclarationArguments parent node
- #63: FunctionAnnotation (D UDA, Python property, Java annotation), 
       FunctionDeclarationVarArgsMap, LambdaFunctionDeclaration
- #59: IndexOperators
- #58: BlockScopeResourceExpr, BlockScopeResourceAlias, BlockScopeBody
- #57: ListExpansion, MapExpansion
- #56: Yield, Yield From 

### No PR done:

- Currently none.

## Rule problems

- Currently none.

## Missing SDK features

- Moving nodes,  examples: 
    - Default argument values must be put under their FunctionDeclarationArgument
    node. In Python they're on a separate parent node.

    - Boolean expressions in Python are anidated if there are more than 2 nodes,
      in the UAST they should be a plain list of operators OR anidated boolean
      binaryExpressions (like Nim and C++ AST do).

    - Attributes like a.b.c.d are anidated (a(b(c(d)))) in Python but in the 
      UAST should be a list of nodes under a QualifiedIdentifier parent.

## Tests with problems

### BooleanOp / Compare (needs SDK::normalizer changes, missing UAST)

Thi is an odd case. They're not BinaryExpressions but a "Compare" node that
has a "left" node (the first element), a "comparators" node whose childs are
the other expressions/literals. The operators are grouped under a parrent
node "operators" that, like default values, must be interpolated.

So for a == b < c we would have something like:

compare {
   left: a
   comparators: [b, c]
   operators: LessThan, Equal

So for this, and the function default valuies, we would need a rule 
"Interpolate" or something like that that can take that and do:

BooleanExpresion {
    Childs: [a, lessthan, b, equal, c]
}

- UnaryOp ("not a") doesn't have a rule.

### ClassDef (needs SDK::normalizer changes)

- Methods have the same issues as FunctionDef plus class decorators would need
some TypeDefinitionAnnotation or something like that.

### ClassDefMetaClassPy3 (missing UAST roles)

- the "X=Y" inside the class parenthesis  is inside a "keywords" group. This has
  "keyword" nodes and for every node, in our UAST the "X" is this group
  Token (Ok) and has a child "Y" of type SimpleIdentifier (also Ok, I think).
  We would need some way to represent those class keywords and the grouper 
  node (internal types ClassDef.keywords and keyword currently) -> these can
  use TypeDeclarationAnnotation if added.

### QualifiedIdentifier (rules? maybe need SDK feature)

For a given expression with the form:

a.b.c

Python generates an "Attribute" node with the field "attr" set to the 
last element ("c") and a child which also have "Attribute" type and attr "b" 
which recursively has a child Attribute.attr = "a". In the generated
UAST these have the QualifiedIdentifier roles (except the last one which has
SimpleIdentifier), but the UAST specifies that a QualifiedIdentifier should
have its member as Childrens of type SimpleIdentifier. 
  
### FunctionCalls (rule problems)

- Need UAST nodes for ListExpansion (native AST = starred) and MapExpansion
  (native AST != keyword, usually "name", inside keywords).

### FunctionDefAnnotated (missing UAST nodes)

- Annotated parameters (type: annotation) without correct role (but is 
  already a children of the argument which is very nice).

- Annotated return value (type: returns) without correct role.

- Argument grouper waiting for the FunctionDeclarationArguments role to be
  merged.


### FunctionDefDecorated (missing UAST nodes)

- The decorators need an additional role. 

### FunctionDefDefaultparams (semantic language specific problem, missing UAST
nodes)

- The function has a FunctionDef.defaults child node which has the default
  arguments but those are not children of the arguments itself (you have
  to match them aligning the normal non-vararg non-kwarg arguments to the 
  right).

- The parent has the role FunctionDefArgDefaultValue but a plural version 
  with the individual default values using the the singular version would
  be better.

### FunctionDefKwarg (missing UAST nodes)

- The kwargs are using the role FunctionDeclarationVarArgsList while the 
  PR for the FunctionDeclarationMap is pending.

### FunctionDefSimple (missing UAST nodes)

- FunctionDeclarationArguments and Yield need UAST roles.

### FunctionDefVarArg (missing UAST nodes)

- Same as FunctionDefSimple. Missing UAST role "FunctionDeclarationArguments".

### IfExpression (a = val if sometest else otherval) (rule problems)

- The test (IfCondition) has the same problems as the other boolean expressions
  in Python (odd layout of elements).


### Pass (Col:0 for comments)

- The line-trailing comment doesn't have the column (Col:0)

### With (missing UAST)

- with.body doesn't have UAST (BlockScopeBody)

- The "item" in "with item as s" should have BlockScopeObject and the 
  "s" BlockScopeObjectAlias.

### Comments (Col: 0, rule problems)

- All comments and lines have col:0

## Clean tests

- FunctionDefDocstring: The docstring shows as an
  Func.Body.Expression.StringLiteral but the Python AST doesn't add any other role
  either so its Ok.

- Hello

- Import: Ok. The way to distinguist "import os" from "from os import path" is that
  in the first case the ImportDeclaration doesn't have a Token and it the second
  case it as the "os" token, which I think is enough. In both cases the childs
  ("os" in the first case and "path" in the second) have the ImportPath role.

- Print

- Expr: but it puts the Expr Call under and Expression node while in the Print
  test it doesn't (but is the Python AST that does it that way so we 
  probably can do much to unify this).

- SameLine (expr; expr): The native AST or UAST doesn't make a distintion because
  of the ";"  but since both expressions are children of the "File" node and the
  column numbers are correctly set it can be inferred.

- Assert (OK) Very minor: assert with and without parenthesis produce the same AST.

- AugAssign

- ClassDefMetaClassPy2 (just a normal assignment inside the class body)

- For

- If 

- LineComment

- While

- LoopIf

- UnaryExpr

- Ellipsis: Ok (it's a very odd token that doesn't reserve an UAST node until we
  find more instances in other languages; gets the SimpleIdentifier role with the 
  "PythonEllipsisOperator" token). Could be changed to NotImplemented if added.

- LiteralsAssign

- Bitwise

- AritmeticOps

- ClassDefInheritance
