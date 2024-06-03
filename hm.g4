grammar hm;

NUMBER : [0-9]+ ;
VARIABLE : [a-zA-Z] [a-zA-Z0-9]*;

OPERATORHP : '*' | '/';
OPERATORLP : '+' | '-';

root : expr;

expr : term                        # Termino
     | ('(' term ')' | term) term  # Application
     ;

term : '\\' VARIABLE '->' expr     # Abstraction 
     | '(' OPERATORHP ')' term     # HighPrioOperator
     | '(' OPERATORLP ')' term     # LowPrioOperator
     | fact                        # Factor
     ;

fact : NUMBER                      # Number
     | VARIABLE                    # Variable
     ;

WS   : [ \t\n\r]+ -> skip;