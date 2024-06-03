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


    # Visit a parse tree produced by hmParser#Application.
    def visitApplication(self, ctx:hmParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Abstraction.
    def visitAbstraction(self, ctx:hmParser.AbstractionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#HighPrioOperator.
    def visitHighPrioOperator(self, ctx:hmParser.HighPrioOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#LowPrioOperator.
    def visitLowPrioOperator(self, ctx:hmParser.LowPrioOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Factor.
    def visitFactor(self, ctx:hmParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#Number.
    def visitNumber(self, ctx:hmParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by hmParser#VARIABLE.
    def visitVARIABLE(self, ctx:hmParser.VARIABLEContext):
        return self.visitChildren(ctx)



del hmParser