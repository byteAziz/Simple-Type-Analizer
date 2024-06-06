grammar hm;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z] [a-zA-Z0-9]*;

OPERATOR : '+';

root : expr;

expr : '\\' VARIABLE '->' expr     # Abstraction    
     | expr expr                   # Application
     | '(' expr ')' expr           # ApplicParen
     | '(' OPERATOR ')'            # OperatorNP 
     | NUMBER                      # Number
     | VARIABLE                    # Variable
     ;

WS   : [ \t\n\r]+ -> skip;