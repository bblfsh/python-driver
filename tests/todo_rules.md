=== General issues:

- Some nodes with "Col:0": arguments, all operators, all whitespace

- Body (IfBody, ForBody, etc) elements have the role xBody but not a parent
  xBody node grouping them.

- "a.b" has the native role "Attribute", should be QualifiedIdentifier

- The integration tests should probably check for nodes in the UAST 
  that doesn't have assigned Roles.

=== AritmeticOps (missing UAST nodes)

- BinOp doesn't have a rule. It could have the role Expr or add
  a new BinOp UAST role.
- "left" and "right" operators should have a Role.

=== Assert (sorting)
- Redo tests with the message and without parens
- The third line with the assertmsg: it puts the message string before
  the boolean (should be the boolean and then the message).

=== AugAssign (not OK)

- a +=: "a" should be AssignmentVariable (only has SimpleIdentifier, it has the
  "target" property in the native AST). Check after the merge?

=== Bitwise (missing UAST, sorting)

- Same as BinaryOpt. Also left, right and the operator are unsorted.

=== BooleanOp (rule problems, missing UAST)

- The "Compare" parent doesn't have a rule (child of Expression).
- UnaryOp ("not a") doesn't have a rule.

=== ClassDef (test again with new FunctionDeclaration rules, improve test)

- The arguments doesn't have roles (test again when the FunctionDef PR
  has been defined). 

- Find a way or feature request so we can add a rule that can add the 
  parent ClassDef node as FunctionDeclarationReceiver.

- @Properties or decorator are not marked. It is rightly inside the FunctionDef,
  but it has the role "SimpleIdentifier" if they don't have a callee or Attribute
  if they have. Should have some UAST role (annotation, etc).

- "a.setter" generates the nodes:
    Attribute(a)
        Childs:
            SimpleIdentifier(setter)
  
  In the Python AST is:
    Attribute (setter)
        value:
            Name (a)

  Probably dotted/arrowed attribute access receivers (not always function calls)
  should have a Receiver (maybe we could use that receiver for CallReceiver and
  FunctionDeclarationReceiver?).

- The assignments at the end, contrary to what happens with AugAssign and 
  the assignments inside the methods, have their AssignmentVariable role
  correctly set.

- Need to add staticmember and classmember decorators for methods, metaclass
  assignment in the style of Python2 and Python3 and class members.
  
=== Comments (OK)

- Ok

=== For (rule problems, sorting)

- Elements in the list have the right order but childs of the ForEach
  node have not.

- Elements in the body has the ForBody but not a parent node (this
  also happens with IfBody and other bodies).

=== FuncDefDefParams (test again)

- Check once the FunctionDeclaration roles have been added.

=== FunctionCalls (rule problems, sorting)

- The "a.bitlength()" call has the form:
  Call -> bitlength:Attribute:CallCalle -> 
      [a:SimpleIdentifier] 

  it should be:

  Call -> Attribute -> [a:CallReceiver, bitlength:CallCallee]

  or maybe:

  Call -> Attribute:CallCallee -> [a: CallReceiver, bitlength:SimpleIdentifier]

  The children of call are also unsorted.

=== FunctionDef (test again)

- Check once the FunctionDeclaration roles have been added


=== FunctionDefArgs (test again)

- Check once the FunctionDeclaration roles have been added

=== Hello (OK)

- Ok

=== If (rule problems, tree problems)

- There is no parent IfBody node, instead all the expressions in the body
  have the additional rule IfBody. I would prefer to have a parent IfBody node.

- The "elif" (with Roles If+Elseif, nice!) is a children of the If node and the
  "else" is a children of that "elif". This is how Python AST works for ifs but
  we've to see if in the UAST we want to reparent the elses to the first If node.

- The compare in this case rightly have the "IfCondition" node (unlike what 
  happens in the BooleanOp test).

=== IfExpression (a = val if sometest else otherval) (rule problems)

- The If node is a child of the Assignment and has also the AssignmentValue
  role, which is nice.

- The compare child of the If doesn't have the IfCondition role.

- The isn't an ElseIf node (it should have the "otherval" as a child).

=== Import (OK)

- Ok. The way to distinguist "import os" from "from os import path" is that
  in the first case the ImportDeclaration doesn't have a Token and it the second
  case it as the "os" token, which I think is enough. In both cases the childs
  ("os" in the first case and "path" in the second) have the ImportPath role.

=== LineComment (Col: 0)

- Column on comments is 0

=== LiteralsAssign (sorting)

- Sorting

=== LiteralsAssign (missing UAST)

- Ordering is fine when inside List/Tuple/Dict literals

- Dict literals (MapLiteral) on the AST would need MapKey and MapValue
  roles for the elements. 

- Ordering is also fine for the two binary expressions at the end (could be 
  random chance).

=== LoopIf (else for for/while loops) (rule problems)

- The "else" part of the ForEach has just the "Expression" role. It should be
  "IfElse" or "Expression, IfElse".

=== Pass (Col:0 for comments

- The line-trailing comment doesn't have the column (Col:0)

=== Print (Ok)

- Ok

=== Expr (Ok)

- Ok, but it puts the Expr Call under and Expression node while in the Print
  test it doesn't (but is the Python AST that does it that way so we 
  probably can do much to unify this).

=== SameLine (expr; expr) (Ok)

- Ok. The native AST or UAST doesn't make a distintion because of the ";"  
  but since both expressions are children of the "File" node and the column
  numbers are correctly set it can be inferred.

=== Unary (missing UAST)

- Python UnaryOp node doesn't have any role; should probably have the 
  UAST role "UnaryExpression". 


=== While (rule problems)

- The WhileBody nodes should be under a WhileBody parent.

- The native Compare has the UAST WhileCompare, which is Ok (but could be 
  useful to debug the un-roled Compare of BooleanOps).

- If we add BinaryExpression to the UAST the comparison should probably have
  a BinaryExpression parent, but the Python's AST doesn't generate the 
  BinOp...

- In this case the "else" of the while statement is transformed into a "IfElse"
  UAST node which is Ok, but could help debug the LoopIf test where that 
  didn't happen.

=== With (missing UAST)

- BlockScope.withitem (the "a" in "with a:") doesn't have a role 
  (PR #58 would add them).
