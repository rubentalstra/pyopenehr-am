# Generated from grammars/path/OpenEHRPath.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OpenEHRPathParser import OpenEHRPathParser
else:
    from OpenEHRPathParser import OpenEHRPathParser

# This class defines a complete generic visitor for a parse tree produced by OpenEHRPathParser.

class OpenEHRPathVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OpenEHRPathParser#path.
    def visitPath(self, ctx:OpenEHRPathParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenEHRPathParser#segment.
    def visitSegment(self, ctx:OpenEHRPathParser.SegmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenEHRPathParser#predicate.
    def visitPredicate(self, ctx:OpenEHRPathParser.PredicateContext):
        return self.visitChildren(ctx)



del OpenEHRPathParser