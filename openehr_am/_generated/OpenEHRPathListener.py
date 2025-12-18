# Generated from grammars/path/OpenEHRPath.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OpenEHRPathParser import OpenEHRPathParser
else:
    from OpenEHRPathParser import OpenEHRPathParser

# This class defines a complete listener for a parse tree produced by OpenEHRPathParser.
class OpenEHRPathListener(ParseTreeListener):

    # Enter a parse tree produced by OpenEHRPathParser#path.
    def enterPath(self, ctx:OpenEHRPathParser.PathContext):
        pass

    # Exit a parse tree produced by OpenEHRPathParser#path.
    def exitPath(self, ctx:OpenEHRPathParser.PathContext):
        pass


    # Enter a parse tree produced by OpenEHRPathParser#segment.
    def enterSegment(self, ctx:OpenEHRPathParser.SegmentContext):
        pass

    # Exit a parse tree produced by OpenEHRPathParser#segment.
    def exitSegment(self, ctx:OpenEHRPathParser.SegmentContext):
        pass


    # Enter a parse tree produced by OpenEHRPathParser#predicate.
    def enterPredicate(self, ctx:OpenEHRPathParser.PredicateContext):
        pass

    # Exit a parse tree produced by OpenEHRPathParser#predicate.
    def exitPredicate(self, ctx:OpenEHRPathParser.PredicateContext):
        pass



del OpenEHRPathParser