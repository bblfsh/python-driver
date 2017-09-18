| Path | Action |
|------|--------|
| /self::\*\[not\(@InternalType='Module'\)\] | Error |
| /self::\*\[@InternalType='Module'\] | File |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\] | Expression, Binary |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='op'\] | Expression, Binary, Operator |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='left'\] | Expression, Binary, Left |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='right'\] | Expression, Binary, Right |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Eq'\] | Binary, Operator, Equal |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NotEq'\] | Binary, Operator, Equal, Not |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lt'\] | Binary, Operator, LessThan |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='LtE'\] | Binary, Operator, LessThanOrEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Gt'\] | Binary, Operator, GreaterThan |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='GtE'\] | Binary, Operator, GreaterThanOrEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Is'\] | Binary, Operator, Identical |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IsNot'\] | Binary, Operator, Identical, Not |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='In'\] | Binary, Operator, Contains |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NotIn'\] | Binary, Operator, Contains, Not |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Add'\] | Binary, Operator, Add |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Sub'\] | Binary, Operator, Substract |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Mult'\] | Binary, Operator, Multiply |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Div'\] | Binary, Operator, Divide |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Mod'\] | Binary, Operator, Modulo |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FloorDiv'\] | Binary, Operator, Divide, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Pow'\] | Binary, Operator, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='MatMult'\] | Binary, Operator, Multiply, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='LShift'\] | Binary, Operator, Bitwise, LeftShift |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RShift'\] | Binary, Operator, Bitwise, RightShift |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitOr'\] | Binary, Operator, Bitwise, Or |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitXor'\] | Binary, Operator, Bitwise, Xor |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitAnd'\] | Binary, Operator, Bitwise, And |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='And'\] | Binary, Operator, Boolean, And |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Or'\] | Binary, Operator, Boolean, Or |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Not'\] | Binary, Operator, Boolean, Not |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='UnaryOp'\] | Binary, Operator, Unary, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Invert'\] | Operator, Unary, Bitwise, Not |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='UAdd'\] | Operator, Unary, Positive |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='USub'\] | Operator, Unary, Negative |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Str'\] | Literal, String, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='StringLiteral'\] | Literal, String, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Bytes'\] | Literal, ByteString, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Num'\] | Literal, Number, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Num'\]/\*\[@internalRole\]\[@internalRole='n'\] | Literal, Number, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BoolLiteral'\] | Literal, Boolean, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='JoinedStr'\] | Literal, String, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='JoinedStr'\]/\*\[@InternalType='FormattedValue'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NoneLiteral'\] | Literal, Null, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Set'\] | Literal, Set, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='List'\] | Literal, List, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\] | Literal, Map, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\]/\*\[@internalRole\]\[@internalRole='keys'\] | Map, Key |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\]/\*\[@internalRole\]\[@internalRole='values'\] | Map, Value |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Tuple'\] | Literal, Tuple, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef'\] | Function, Declaration, Name, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFunctionDef'\] | Function, Declaration, Name, Identifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef\.decorator\_list'\] | Function, Declaration, Call, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef\.body'\] | Function, Declaration, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='arguments'\] | Function, Declaration, Argument, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='args'\] | Function, Declaration, Argument, Name, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='vararg'\] | Function, Declaration, Argument, ArgsList, Name, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='kwarg'\] | Function, Declaration, Argument, ArgsList, Map, Name, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='kwonlyargs'\] | Function, Declaration, Argument, ArgsList, Map, Name, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments\.defaults'\] | Function, Declaration, Argument, Value, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFunctionDef\.decorator\_list'\] | Function, Declaration, Call, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFunctionDef\.body'\] | Function, Declaration, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\] | Function, Declaration, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='Lambda\.body'\] | Function, Declaration, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Attribute'\] | Identifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Attribute'\]/\*\[@InternalType='Name'\] | Identifier, Qualified |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\] | Function, Call, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='args'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='keywords'\] | Call, Argument, Name |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='keywords'\]/\*\[@internalRole\]\[@internalRole='value'\] | Call, Argument, Value |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Name'\] | Call, Callee |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Attribute'\] | Call, Callee |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Attribute'\]/\*\[@internalRole\]\[@internalRole='value'\] | Call, Receiver |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\] | Binary, Assignment, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\]/\*\[@internalRole\]\[@internalRole='targets'\] | Left |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\]/\*\[@internalRole\]\[@internalRole='value'\] | Right |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\] | Operator, Binary, Assignment, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='op'\] | Operator, Binary |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='target'\] | Left |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='value'\] | Right |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Expression'\] | Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Expr'\] | Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Name'\] | Identifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='SameLineNoops'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='PreviousNoops'\] | Whitespace |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='PreviousNoops'\]/\*\[@internalRole\]\[@internalRole='lines'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RemainderNoops'\] | Whitespace |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RemainderNoops'\]/\*\[@internalRole\]\[@internalRole='lines'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Constant'\] | Identifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\] | Try, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.body'\] | Try, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.finalbody'\] | Try, Finally |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.handlers'\] | Try, Catch |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.orelse'\] | Try, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='TryExcept'\] | Try, Catch, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ExceptHandler'\] | Try, Catch, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ExceptHandler\.name'\] | Try, Catch, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='TryFinally'\] | Try, Finally, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Raise'\] | Throw, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With'\] | Block, Scope, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With\.body'\] | Block, Scope, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With\.items'\] | Identifier, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncWith'\] | Block, Scope, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='withitem'\] | Identifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Return'\] | Return, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Break'\] | Break, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Continue'\] | Continue, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\] | Expression, Binary |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\]/\*\[@InternalType='Compare\.ops'\] | Expression, Binary, Operator |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\]/\*\[@internalRole\]\[@internalRole='left'\] | Expression, Binary, Left |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare\.comparators'\] | Expression, Binary, Right |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\] | If, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@InternalType='If\.body'\] | If, Body, Then |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@internalRole\]\[@internalRole='test'\] | If, Condition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@InternalType='If\.orelse'\] | If, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\] | If, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='body'\] | If, Body, Then |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='test'\] | If, Condition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='orelse'\] | If, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Import'\] | Import, Declaration, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='alias'\] | Import, Pathname, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ImportFrom\.module'\] | Import, Pathname, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='alias\.asname'\] | Import, Alias, Identifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ImportFrom'\] | Import, Declaration, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\] | Type, Declaration, Identifier, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.decorator\_list'\] | Type, Call, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.body'\] | Type, Declaration, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.bases'\] | Type, Declaration, Base |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.keywords'\] | Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.keywords'\]/\*\[@InternalType='keyword'\] | Identifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\] | For, Iterator, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@InternalType='For\.body'\] | For, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@internalRole\]\[@internalRole='iter'\] | For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@internalRole\]\[@internalRole='target'\] | For, Update |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@InternalType='For\.orelse'\] | For, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\] | For, Iterator, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@InternalType='AsyncFor\.body'\] | For, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@internalRole\]\[@internalRole='iter'\] | For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@internalRole\]\[@internalRole='target'\] | For, Update |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@InternalType='AsyncFor\.orelse'\] | For, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\] | While, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@InternalType='While\.body'\] | While, Body |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@internalRole\]\[@internalRole='test'\] | While, Condition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@InternalType='While\.orelse'\] | While, Body, Else |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Pass'\] | Noop, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assert'\] | Assert, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\] | Function, Call, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='body'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='globals'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='locals'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\] | Function, Call, Callee, Identifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='dest'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='nl'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='values'\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='values'\]/\*\[\*\] | Call, Argument, Positional |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AnnAssign'\] | Operator, Binary, Assignment, Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='annotation'\] | Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='returns'\] | Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Ellipsis'\] | Identifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ListComp'\] | List, For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='DictComp'\] | Map, For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='SetComp'\] | Set, For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\] | For, Iterator, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@internalRole\]\[@internalRole='iter'\] | For, Update, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@internalRole\]\[@internalRole='target'\] | For, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\] | If, Condition, Expression, Binary |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\]/\*\[@InternalType='Compare\.ops'\] | Expression, Binary, Operator |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\]/\*\[@internalRole\]\[@internalRole='left'\] | Expression, Binary, Left |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Delete'\] | Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Await'\] | Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Global'\] | Statement, Visibility, World, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Nonlocal'\] | Statement, Visibility, Module, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Yield'\] | Return, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='YieldFrom'\] | Return, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Yield'\] | Literal, List, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Subscript'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Index'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Slice'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ExtSlice'\] | Expression, Incomplete |
