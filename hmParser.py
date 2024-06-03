# Generated from hm.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,9,42,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,1,1,1,1,1,1,
        1,1,1,1,3,1,17,8,1,1,1,1,1,3,1,21,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,36,8,2,1,3,1,3,3,3,40,8,3,1,3,0,0,
        4,0,2,4,6,0,0,43,0,8,1,0,0,0,2,20,1,0,0,0,4,35,1,0,0,0,6,39,1,0,
        0,0,8,9,3,2,1,0,9,1,1,0,0,0,10,21,3,4,2,0,11,12,5,1,0,0,12,13,3,
        4,2,0,13,14,5,2,0,0,14,17,1,0,0,0,15,17,3,4,2,0,16,11,1,0,0,0,16,
        15,1,0,0,0,17,18,1,0,0,0,18,19,3,4,2,0,19,21,1,0,0,0,20,10,1,0,0,
        0,20,16,1,0,0,0,21,3,1,0,0,0,22,23,5,3,0,0,23,24,5,6,0,0,24,25,5,
        4,0,0,25,36,3,2,1,0,26,27,5,1,0,0,27,28,5,7,0,0,28,29,5,2,0,0,29,
        36,3,4,2,0,30,31,5,1,0,0,31,32,5,8,0,0,32,33,5,2,0,0,33,36,3,4,2,
        0,34,36,3,6,3,0,35,22,1,0,0,0,35,26,1,0,0,0,35,30,1,0,0,0,35,34,
        1,0,0,0,36,5,1,0,0,0,37,40,5,5,0,0,38,40,5,6,0,0,39,37,1,0,0,0,39,
        38,1,0,0,0,40,7,1,0,0,0,4,16,20,35,39
    ]

class hmParser ( Parser ):

    grammarFileName = "hm.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'\\'", "'->'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "NUMBER", "VARIABLE", "OPERATORHP", "OPERATORLP", 
                      "WS" ]

    RULE_root = 0
    RULE_expr = 1
    RULE_term = 2
    RULE_fact = 3

    ruleNames =  [ "root", "expr", "term", "fact" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    NUMBER=5
    VARIABLE=6
    OPERATORHP=7
    OPERATORLP=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(hmParser.ExprContext,0)


        def getRuleIndex(self):
            return hmParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = hmParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return hmParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TerminoContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(hmParser.TermContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermino" ):
                return visitor.visitTermino(self)
            else:
                return visitor.visitChildren(self)


    class ApplicationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(hmParser.TermContext)
            else:
                return self.getTypedRuleContext(hmParser.TermContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitApplication" ):
                return visitor.visitApplication(self)
            else:
                return visitor.visitChildren(self)



    def expr(self):

        localctx = hmParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        try:
            self.state = 20
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = hmParser.TerminoContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 10
                self.term()
                pass

            elif la_ == 2:
                localctx = hmParser.ApplicationContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 16
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 11
                    self.match(hmParser.T__0)
                    self.state = 12
                    self.term()
                    self.state = 13
                    self.match(hmParser.T__1)
                    pass

                elif la_ == 2:
                    self.state = 15
                    self.term()
                    pass


                self.state = 18
                self.term()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return hmParser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LowPrioOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def OPERATORLP(self):
            return self.getToken(hmParser.OPERATORLP, 0)
        def term(self):
            return self.getTypedRuleContext(hmParser.TermContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLowPrioOperator" ):
                return visitor.visitLowPrioOperator(self)
            else:
                return visitor.visitChildren(self)


    class FactorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def fact(self):
            return self.getTypedRuleContext(hmParser.FactContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)


    class HighPrioOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def OPERATORHP(self):
            return self.getToken(hmParser.OPERATORHP, 0)
        def term(self):
            return self.getTypedRuleContext(hmParser.TermContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHighPrioOperator" ):
                return visitor.visitHighPrioOperator(self)
            else:
                return visitor.visitChildren(self)


    class AbstractionContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(hmParser.VARIABLE, 0)
        def expr(self):
            return self.getTypedRuleContext(hmParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbstraction" ):
                return visitor.visitAbstraction(self)
            else:
                return visitor.visitChildren(self)



    def term(self):

        localctx = hmParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_term)
        try:
            self.state = 35
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = hmParser.AbstractionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 22
                self.match(hmParser.T__2)
                self.state = 23
                self.match(hmParser.VARIABLE)
                self.state = 24
                self.match(hmParser.T__3)
                self.state = 25
                self.expr()
                pass

            elif la_ == 2:
                localctx = hmParser.HighPrioOperatorContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 26
                self.match(hmParser.T__0)
                self.state = 27
                self.match(hmParser.OPERATORHP)
                self.state = 28
                self.match(hmParser.T__1)
                self.state = 29
                self.term()
                pass

            elif la_ == 3:
                localctx = hmParser.LowPrioOperatorContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 30
                self.match(hmParser.T__0)
                self.state = 31
                self.match(hmParser.OPERATORLP)
                self.state = 32
                self.match(hmParser.T__1)
                self.state = 33
                self.term()
                pass

            elif la_ == 4:
                localctx = hmParser.FactorContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 34
                self.fact()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return hmParser.RULE_fact

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class NumberContext(FactContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.FactContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(hmParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)


    class VARIABLEContext(FactContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.FactContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(hmParser.VARIABLE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVARIABLE" ):
                return visitor.visitVARIABLE(self)
            else:
                return visitor.visitChildren(self)



    def fact(self):

        localctx = hmParser.FactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_fact)
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                localctx = hmParser.NumberContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 37
                self.match(hmParser.NUMBER)
                pass
            elif token in [6]:
                localctx = hmParser.VARIABLEContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 38
                self.match(hmParser.VARIABLE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





