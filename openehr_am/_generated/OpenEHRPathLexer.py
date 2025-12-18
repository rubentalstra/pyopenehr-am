# Generated from grammars/path/OpenEHRPath.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,4,33,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,1,1,4,
        1,14,8,1,11,1,12,1,15,1,1,1,1,1,2,1,2,5,2,22,8,2,10,2,12,2,25,9,
        2,1,3,4,3,28,8,3,11,3,12,3,29,1,3,1,3,0,0,4,1,1,3,2,5,3,7,4,1,0,
        4,4,0,10,10,13,13,47,47,91,93,3,0,65,90,95,95,97,122,4,0,48,57,65,
        90,95,95,97,122,3,0,9,10,13,13,32,32,35,0,1,1,0,0,0,0,3,1,0,0,0,
        0,5,1,0,0,0,0,7,1,0,0,0,1,9,1,0,0,0,3,11,1,0,0,0,5,19,1,0,0,0,7,
        27,1,0,0,0,9,10,5,47,0,0,10,2,1,0,0,0,11,13,5,91,0,0,12,14,8,0,0,
        0,13,12,1,0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,
        1,0,0,0,17,18,5,93,0,0,18,4,1,0,0,0,19,23,7,1,0,0,20,22,7,2,0,0,
        21,20,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,23,24,1,0,0,0,24,6,1,0,
        0,0,25,23,1,0,0,0,26,28,7,3,0,0,27,26,1,0,0,0,28,29,1,0,0,0,29,27,
        1,0,0,0,29,30,1,0,0,0,30,31,1,0,0,0,31,32,6,3,0,0,32,8,1,0,0,0,4,
        0,15,23,29,1,6,0,0
    ]

class OpenEHRPathLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    SLASH = 1
    PREDICATE = 2
    IDENT = 3
    WS = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'/'" ]

    symbolicNames = [ "<INVALID>",
            "SLASH", "PREDICATE", "IDENT", "WS" ]

    ruleNames = [ "SLASH", "PREDICATE", "IDENT", "WS" ]

    grammarFileName = "OpenEHRPath.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


