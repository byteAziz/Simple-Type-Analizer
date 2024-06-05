grammar hm;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z] [a-zA-Z0-9]*;

OPERATOR : '+' | '-';

root : expr;

expr : '\\' VARIABLE '->' expr     # Abstraction    
     | ('(' expr ')') atom         # ApplicationParen
     | expr atom                   # Application
     | atom                        # Termino
     ;

atom : '(' OPERATOR ')'            # Operator
     | NUMBER                      # Number
     | VARIABLE                    # Variable
     ;

WS   : [ \t\n\r]+ -> skip;