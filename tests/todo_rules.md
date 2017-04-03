=== AritmeticOps

- BinOp doesn't have a rule. It could have the role Expr or add
  a new BinOp UAST role.
- "left" and "right" operators should have a Role.

=== Assert
- Redo tests with the message and without parens
- The third line with the assertmsg: it puts the message string before
  the boolean (should be the boolean and then the message).

=== AugAssign

- a +=: "a" should be AssignmentVariable (only has SimpleIdentifier, it has the
  "target" property in the native AST). Check after the merge?

=== Bitwise

- Same as BinaryOpt. Also left, right and the operator are unsorted.

=== BooleanOp

- The "Compare" parent doesn't have a rule (child of Expression).
- UnaryOp ("not a") doesn't have a rule.

=== ClassDef

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
  
=== Comments

- Check in the new test with two comments above and below the ordering of 
  the line nodes in the comments above and below.

=== For

- Elements in the list have the right order but childs of the ForEach
  node have not.

=== FuncDefDefParams

- Check once the FunctionDeclaration roles have been added.

== FunctionCalls
