# Generated from hm.g4 by ANTLR 4.13.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,9,51,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,3,1,4,4,
        4,30,8,4,11,4,12,4,31,1,5,1,5,5,5,36,8,5,10,5,12,5,39,9,5,1,6,1,
        6,1,7,1,7,1,8,4,8,46,8,8,11,8,12,8,47,1,8,1,8,0,0,9,1,1,3,2,5,3,
        7,4,9,5,11,6,13,7,15,8,17,9,1,0,6,1,0,48,57,2,0,65,90,97,122,3,0,
        48,57,65,90,97,122,2,0,42,42,47,47,2,0,43,43,45,45,3,0,9,10,13,13,
        32,32,53,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,
        0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,1,19,1,0,
        0,0,3,21,1,0,0,0,5,23,1,0,0,0,7,25,1,0,0,0,9,29,1,0,0,0,11,33,1,
        0,0,0,13,40,1,0,0,0,15,42,1,0,0,0,17,45,1,0,0,0,19,20,5,40,0,0,20,
        2,1,0,0,0,21,22,5,41,0,0,22,4,1,0,0,0,23,24,5,92,0,0,24,6,1,0,0,
        0,25,26,5,45,0,0,26,27,5,62,0,0,27,8,1,0,0,0,28,30,7,0,0,0,29,28,
        1,0,0,0,30,31,1,0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,10,1,0,0,0,
        33,37,7,1,0,0,34,36,7,2,0,0,35,34,1,0,0,0,36,39,1,0,0,0,37,35,1,
        0,0,0,37,38,1,0,0,0,38,12,1,0,0,0,39,37,1,0,0,0,40,41,7,3,0,0,41,
        14,1,0,0,0,42,43,7,4,0,0,43,16,1,0,0,0,44,46,7,5,0,0,45,44,1,0,0,
        0,46,47,1,0,0,0,47,45,1,0,0,0,47,48,1,0,0,0,48,49,1,0,0,0,49,50,
        6,8,0,0,50,18,1,0,0,0,4,0,31,37,47,1,6,0,0
    ]

class hmLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    NUMBER = 5
    VARIABLE = 6
    OPERATORHP = 7
    OPERATORLP = 8
    WS = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'\\'", "'->'" ]

    symbolicNames = [ "<INVALID>",
            "NUMBER", "VARIABLE", "OPERATORHP", "OPERATORLP", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "NUMBER", "VARIABLE", 
                  "OPERATORHP", "OPERATORLP", "WS" ]

    grammarFileName = "hm.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


