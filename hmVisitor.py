# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .hmParser import hmParser
else:
    from hmParser import hmParser

# This class defines a complete generic visitor for a parse tree produced by hmParser.

class hmVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by hmParser#root.
    def visitRoot(self, ctx:hmParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Termino.
    def visitTermino(self, ctx:hmParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Abstraction.
    def visitAbstraction(self, ctx:hmParser.AbstractionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Application.
    def visitApplication(self, ctx:hmParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#ApplicationParen.
    def visitApplicationParen(self, ctx:hmParser.ApplicationParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Operator.
    def visitOperator(self, ctx:hmParser.OperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Number.
    def visitNumber(self, ctx:hmParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Variable.
    def visitVariable(self, ctx:hmParser.VariableContext):
        return self.visitChildren(ctx)



del hmParser