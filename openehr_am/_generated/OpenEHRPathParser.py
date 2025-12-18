# Generated from grammars/path/OpenEHRPath.g4 by ANTLR 4.13.2
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
        4,1,4,24,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,0,5,0,11,8,0,10,0,
        12,0,14,9,0,1,0,1,0,1,1,1,1,3,1,20,8,1,1,2,1,2,1,2,0,0,3,0,2,4,0,
        0,22,0,6,1,0,0,0,2,17,1,0,0,0,4,21,1,0,0,0,6,7,5,1,0,0,7,12,3,2,
        1,0,8,9,5,1,0,0,9,11,3,2,1,0,10,8,1,0,0,0,11,14,1,0,0,0,12,10,1,
        0,0,0,12,13,1,0,0,0,13,15,1,0,0,0,14,12,1,0,0,0,15,16,5,0,0,1,16,
        1,1,0,0,0,17,19,5,3,0,0,18,20,3,4,2,0,19,18,1,0,0,0,19,20,1,0,0,
        0,20,3,1,0,0,0,21,22,5,2,0,0,22,5,1,0,0,0,2,12,19
    ]

class OpenEHRPathParser ( Parser ):

    grammarFileName = "OpenEHRPath.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'/'" ]

    symbolicNames = [ "<INVALID>", "SLASH", "PREDICATE", "IDENT", "WS" ]

    RULE_path = 0
    RULE_segment = 1
    RULE_predicate = 2

    ruleNames =  [ "path", "segment", "predicate" ]

    EOF = Token.EOF
    SLASH=1
    PREDICATE=2
    IDENT=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(OpenEHRPathParser.SLASH)
            else:
                return self.getToken(OpenEHRPathParser.SLASH, i)

        def segment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenEHRPathParser.SegmentContext)
            else:
                return self.getTypedRuleContext(OpenEHRPathParser.SegmentContext,i)


        def EOF(self):
            return self.getToken(OpenEHRPathParser.EOF, 0)

        def getRuleIndex(self):
            return OpenEHRPathParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPath" ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPath" ):
                listener.exitPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = OpenEHRPathParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(OpenEHRPathParser.SLASH)
            self.state = 7
            self.segment()
            self.state = 12
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 8
                self.match(OpenEHRPathParser.SLASH)
                self.state = 9
                self.segment()
                self.state = 14
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 15
            self.match(OpenEHRPathParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SegmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenEHRPathParser.IDENT, 0)

        def predicate(self):
            return self.getTypedRuleContext(OpenEHRPathParser.PredicateContext,0)


        def getRuleIndex(self):
            return OpenEHRPathParser.RULE_segment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSegment" ):
                listener.enterSegment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSegment" ):
                listener.exitSegment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSegment" ):
                return visitor.visitSegment(self)
            else:
                return visitor.visitChildren(self)




    def segment(self):

        localctx = OpenEHRPathParser.SegmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_segment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.match(OpenEHRPathParser.IDENT)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 18
                self.predicate()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PREDICATE(self):
            return self.getToken(OpenEHRPathParser.PREDICATE, 0)

        def getRuleIndex(self):
            return OpenEHRPathParser.RULE_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate" ):
                listener.enterPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate" ):
                listener.exitPredicate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPredicate" ):
                return visitor.visitPredicate(self)
            else:
                return visitor.visitChildren(self)




    def predicate(self):

        localctx = OpenEHRPathParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_predicate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self.match(OpenEHRPathParser.PREDICATE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





