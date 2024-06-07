grammar hm;

BASICTYPE : 'N';
NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z] [a-zA-Z0-9]*;
OPERATOR : '+';

root : expr;

expr : typeDefinition
     | abstraction
     | application
     | term
     ;

typeDefinition : term '::' type;

type: BASICTYPE ('->' type)*;

abstraction : '\\' VARIABLE '->' expr;

application : application term     # ApplicRecursive
            | term term            # ApplicationBase
            ;

term : '(' expr ')'                # ParenExpr
     | '(' OPERATOR ')'            # OperatorNP
     | NUMBER                      # Number
     | VARIABLE                    # Variable
     ;

WS   : [ \t\n\r]+ -> skip;
