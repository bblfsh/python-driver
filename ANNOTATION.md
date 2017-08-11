| Path | Action |
|------|--------|
| /self::\*\[not\(@InternalType='Module'\)\] | Error |
| /self::\*\[@InternalType='Module'\] | File |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\] | BinaryExpression, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='op'\] | BinaryExpressionOp |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='left'\] | BinaryExpressionLeft |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BinOp'\]/\*\[@internalRole\]\[@internalRole='right'\] | BinaryExpressionRight |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Eq'\] | OpEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NotEq'\] | OpNotEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lt'\] | OpLessThan |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='LtE'\] | OpLessThanEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Gt'\] | OpGreaterThan |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='GtE'\] | OpGreaterThanEqual |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Is'\] | OpSame |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IsNot'\] | OpNotSame |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='In'\] | OpContains |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NotIn'\] | OpNotContains |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Add'\] | OpAdd |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Sub'\] | OpSubstract |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Mult'\] | OpMultiply |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Div'\] | OpDivide |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Mod'\] | OpMod |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FloorDiv'\] | OpDivide, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Pow'\] | Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='MatMult'\] | OpMultiply, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='LShift'\] | OpBitwiseLeftShift |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RShift'\] | OpBitwiseRightShift |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitOr'\] | OpBitwiseOr |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitXor'\] | OpBitwiseXor |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BitAnd'\] | OpBitwiseAnd |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='And'\] | OpBooleanAnd |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Or'\] | OpBooleanOr |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Not'\] | OpBooleanNot |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='UnaryOp'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Invert'\] | OpBitwiseComplement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='UAdd'\] | OpPositive |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='USub'\] | OpNegative |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='StringLiteral'\] | StringLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ByteLiteral'\] | ByteStringLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NumLiteral'\] | NumberLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Str'\] | StringLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='BoolLiteral'\] | BooleanLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='JoinedStr'\] | StringLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='JoinedStr'\]/\*\[@InternalType='FormattedValue'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='NoneLiteral'\] | NullLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Set'\] | SetLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='List'\] | ListLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\] | MapLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\]/\*\[@internalRole\]\[@internalRole='keys'\] | MapKey |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Dict'\]/\*\[@internalRole\]\[@internalRole='values'\] | MapValue |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Tuple'\] | TupleLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef'\] | FunctionDeclaration, FunctionDeclarationName, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFunctionDef'\] | FunctionDeclaration, FunctionDeclarationName, SimpleIdentifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef\.decorator\_list'\] | Call, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='FunctionDef\.body'\] | FunctionDeclarationBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\] | FunctionDeclarationArgument, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='args'\] | FunctionDeclarationArgument, FunctionDeclarationArgumentName, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='vararg'\] | FunctionDeclarationArgument, FunctionDeclarationVarArgsList, FunctionDeclarationArgumentName, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='kwarg'\] | FunctionDeclarationArgument, FunctionDeclarationVarArgsList, FunctionDeclarationArgumentName, Incomplete, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@InternalType='arguments\.defaults'\] | FunctionDeclarationArgumentDefaultValue, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@InternalType='arguments\.keywords'\] | FunctionDeclarationArgumentDefaultValue, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@InternalType='AsyncFunctionDef\.decorator\_list'\] | Call, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='arguments'\]/\*\[@InternalType='AsyncFunctionDef\.body'\] | FunctionDeclarationBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\] | FunctionDeclaration, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='Lambda\.body'\] | FunctionDeclarationBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\] | FunctionDeclarationArgument, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='args'\] | FunctionDeclarationArgument, FunctionDeclarationArgumentName, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='vararg'\] | FunctionDeclarationArgument, FunctionDeclarationVarArgsList, FunctionDeclarationArgumentName, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\]/\*\[@internalRole\]\[@internalRole='kwarg'\] | FunctionDeclarationArgument, FunctionDeclarationVarArgsList, FunctionDeclarationArgumentName, Incomplete, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\]/\*\[@InternalType='arguments\.defaults'\] | FunctionDeclarationArgumentDefaultValue, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Lambda'\]/\*\[@InternalType='arguments'\]/\*\[@InternalType='arguments\.keywords'\] | FunctionDeclarationArgumentDefaultValue, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Attribute'\] | SimpleIdentifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Attribute'\]/\*\[@InternalType='Name'\] | QualifiedIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\] | Call, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='args'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='keywords'\] | CallNamedArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='keywords'\]/\*\[@internalRole\]\[@internalRole='value'\] | CallNamedArgumentValue |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Name'\] | Call |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Attribute'\] | CallCallee |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Call'\]/\*\[@internalRole\]\[@internalRole='func'\]/self::\*\[@InternalType='Attribute'\]/\*\[@internalRole\]\[@internalRole='value'\] | CallReceiver |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\] | Assignment, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\]/\*\[@internalRole\]\[@internalRole='targets'\] | AssignmentVariable |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assign'\]/\*\[@internalRole\]\[@internalRole='value'\] | AssignmentValue |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\] | AugmentedAssignment, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='op'\] | AugmentedAssignmentOperator |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='target'\] | AugmentedAssignmentVariable |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AugAssign'\]/\*\[@internalRole\]\[@internalRole='value'\] | AugmentedAssignmentValue |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Expression'\] | Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Expr'\] | Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Name'\] | SimpleIdentifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='SameLineNoops'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='PreviousNoops'\] | Whitespace |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='PreviousNoops'\]/\*\[@internalRole\]\[@internalRole='lines'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RemainderNoops'\] | Whitespace |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='RemainderNoops'\]/\*\[@internalRole\]\[@internalRole='lines'\] | Comment |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Constant'\] | SimpleIdentifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\] | Try, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.body'\] | TryBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.finalbody'\] | TryFinally |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.handlers'\] | TryCatch |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Try'\]/\*\[@InternalType='Try\.orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='TryExcept'\] | TryCatch, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ExceptHandler'\] | TryCatch, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='TryFinally'\] | TryFinally, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Raise'\] | Throw, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With'\] | BlockScope, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With\.body'\] | BlockScope, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='With\.items'\] | SimpleIdentifier, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncWith'\] | BlockScope, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='withitem'\] | SimpleIdentifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Return'\] | Return, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Break'\] | Break, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Continue'\] | Continue, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\] | BinaryExpression, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\]/\*\[@InternalType='Compare\.ops'\] | BinaryExpressionOp |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare'\]/\*\[@internalRole\]\[@internalRole='left'\] | BinaryExpressionLeft |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Compare\.comparators'\] | BinaryExpressionRight |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\] | If, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@InternalType='If\.body'\] | IfBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@internalRole\]\[@internalRole='test'\] | IfCondition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='If'\]/\*\[@InternalType='If\.orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\] | If, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='body'\] | IfBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='test'\] | IfCondition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='IfExp'\]/\*\[@internalRole\]\[@internalRole='orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Import'\] | ImportDeclaration, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='alias'\] | ImportPath, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ImportFrom\.module'\] | ImportPath, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='alias\.asname'\] | ImportAlias, SimpleIdentifier |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ImportFrom'\] | ImportDeclaration, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\] | TypeDeclaration, SimpleIdentifier, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.body'\] | TypeDeclarationBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.bases'\] | TypeDeclarationBases |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.keywords'\] | Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ClassDef'\]/\*\[@InternalType='ClassDef\.keywords'\]/\*\[@InternalType='keyword'\] | SimpleIdentifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\] | ForEach, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@InternalType='For\.body'\] | ForBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@internalRole\]\[@internalRole='iter'\] | ForExpression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@internalRole\]\[@internalRole='target'\] | ForUpdate |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='For'\]/\*\[@InternalType='For\.orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\] | ForEach, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@InternalType='AsyncFor\.body'\] | ForBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@internalRole\]\[@internalRole='iter'\] | ForExpression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@internalRole\]\[@internalRole='target'\] | ForUpdate |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AsyncFor'\]/\*\[@InternalType='AsyncFor\.orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\] | While, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@InternalType='While\.body'\] | WhileBody |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@internalRole\]\[@internalRole='test'\] | WhileCondition |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='While'\]/\*\[@InternalType='While\.orelse'\] | IfElse |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Pass'\] | Noop, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Num'\] | NumberLiteral, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Assert'\] | Assert, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\] | Call, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='body'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='globals'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Exec'\]/\*\[@internalRole\]\[@internalRole='locals'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\] | Call, CallCallee, SimpleIdentifier, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='dest'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='nl'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='values'\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Print'\]/\*\[@internalRole\]\[@internalRole='values'\]/\*\[\*\] | CallPositionalArgument |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='AnnAssign'\] | Assignment, Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Annotation'\] | Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@internalRole\]\[@internalRole='returns'\] | Comment, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Ellipsis'\] | SimpleIdentifier, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\] | ForEach, Expression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@internalRole\]\[@internalRole='iter'\] | ForUpdate, Statement |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@internalRole\]\[@internalRole='target'\] | ForExpression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\] | IfCondition, BinaryExpression |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\]/\*\[@InternalType='Compare\.ops'\] | BinaryExpressionOp |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='comprehension'\]/\*\[@InternalType='Compare'\]/\*\[@internalRole\]\[@internalRole='left'\] | BinaryExpressionLeft |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ListComp'\] | ListLiteral, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='DictComp'\] | MapLiteral, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='SetComp'\] | SetLiteral, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Delete'\] | Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Await'\] | Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Global'\] | Statement, VisibleFromWorld, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Nonlocal'\] | Statement, VisibleFromModule, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Yield'\] | Return, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='YieldFrom'\] | Return, Statement, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Yield'\] | ListLiteral, Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Subscript'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Index'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='Slice'\] | Expression, Incomplete |
| /self::\*\[@InternalType='Module'\]//\*\[@InternalType='ExtSlice'\] | Expression, Incomplete |
