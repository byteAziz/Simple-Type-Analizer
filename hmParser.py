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
        4,1,8,37,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,3,1,21,8,1,1,1,1,1,5,1,25,8,1,10,1,12,1,
        28,9,1,1,2,1,2,1,2,1,2,1,2,3,2,35,8,2,1,2,0,1,2,3,0,2,4,0,0,38,0,
        6,1,0,0,0,2,20,1,0,0,0,4,34,1,0,0,0,6,7,3,2,1,0,7,1,1,0,0,0,8,9,
        6,1,-1,0,9,10,5,1,0,0,10,11,5,6,0,0,11,12,5,2,0,0,12,21,3,2,1,4,
        13,14,5,3,0,0,14,15,3,2,1,0,15,16,5,4,0,0,16,17,1,0,0,0,17,18,3,
        4,2,0,18,21,1,0,0,0,19,21,3,4,2,0,20,8,1,0,0,0,20,13,1,0,0,0,20,
        19,1,0,0,0,21,26,1,0,0,0,22,23,10,2,0,0,23,25,3,4,2,0,24,22,1,0,
        0,0,25,28,1,0,0,0,26,24,1,0,0,0,26,27,1,0,0,0,27,3,1,0,0,0,28,26,
        1,0,0,0,29,30,5,3,0,0,30,31,5,7,0,0,31,35,5,4,0,0,32,35,5,5,0,0,
        33,35,5,6,0,0,34,29,1,0,0,0,34,32,1,0,0,0,34,33,1,0,0,0,35,5,1,0,
        0,0,3,20,26,34
    ]

class hmParser ( Parser ):

    grammarFileName = "hm.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\\'", "'->'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "NUMBER", "VARIABLE", "OPERATOR", "WS" ]

    RULE_root = 0
    RULE_expr = 1
    RULE_atom = 2

    ruleNames =  [ "root", "expr", "atom" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    NUMBER=5
    VARIABLE=6
    OPERATOR=7
    WS=8

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
            self.state = 6
            self.expr(0)
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

        def atom(self):
            return self.getTypedRuleContext(hmParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermino" ):
                return visitor.visitTermino(self)
            else:
                return visitor.visitChildren(self)


    class AbstractionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.ExprContext
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


    class ApplicationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(hmParser.ExprContext,0)

        def atom(self):
            return self.getTypedRuleContext(hmParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitApplication" ):
                return visitor.visitApplication(self)
            else:
                return visitor.visitChildren(self)


    class ApplicationParenContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(hmParser.AtomContext,0)

        def expr(self):
            return self.getTypedRuleContext(hmParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitApplicationParen" ):
                return visitor.visitApplicationParen(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = hmParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                localctx = hmParser.AbstractionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 9
                self.match(hmParser.T__0)
                self.state = 10
                self.match(hmParser.VARIABLE)
                self.state = 11
                self.match(hmParser.T__1)
                self.state = 12
                self.expr(4)
                pass

            elif la_ == 2:
                localctx = hmParser.ApplicationParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 13
                self.match(hmParser.T__2)
                self.state = 14
                self.expr(0)
                self.state = 15
                self.match(hmParser.T__3)
                self.state = 17
                self.atom()
                pass

            elif la_ == 3:
                localctx = hmParser.TerminoContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 19
                self.atom()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 26
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = hmParser.ApplicationContext(self, hmParser.ExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                    self.state = 22
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 23
                    self.atom() 
                self.state = 28
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return hmParser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class OperatorContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def OPERATOR(self):
            return self.getToken(hmParser.OPERATOR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperator" ):
                return visitor.visitOperator(self)
            else:
                return visitor.visitChildren(self)


    class VariableContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(hmParser.VARIABLE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)


    class NumberContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a hmParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(hmParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)



    def atom(self):

        localctx = hmParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_atom)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                localctx = hmParser.OperatorContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.match(hmParser.T__2)
                self.state = 30
                self.match(hmParser.OPERATOR)
                self.state = 31
                self.match(hmParser.T__3)
                pass
            elif token in [5]:
                localctx = hmParser.NumberContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                self.match(hmParser.NUMBER)
                pass
            elif token in [6]:
                localctx = hmParser.VariableContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 33
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



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         




