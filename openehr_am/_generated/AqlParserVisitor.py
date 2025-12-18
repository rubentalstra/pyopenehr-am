# Generated from grammars/aql/AqlParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AqlParser import AqlParser
else:
    from AqlParser import AqlParser

# This class defines a complete generic visitor for a parse tree produced by AqlParser.

class AqlParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AqlParser#selectQuery.
    def visitSelectQuery(self, ctx:AqlParser.SelectQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#selectClause.
    def visitSelectClause(self, ctx:AqlParser.SelectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#fromClause.
    def visitFromClause(self, ctx:AqlParser.FromClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#whereClause.
    def visitWhereClause(self, ctx:AqlParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#orderByClause.
    def visitOrderByClause(self, ctx:AqlParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#limitClause.
    def visitLimitClause(self, ctx:AqlParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#selectExpr.
    def visitSelectExpr(self, ctx:AqlParser.SelectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#fromExpr.
    def visitFromExpr(self, ctx:AqlParser.FromExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#whereExpr.
    def visitWhereExpr(self, ctx:AqlParser.WhereExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#orderByExpr.
    def visitOrderByExpr(self, ctx:AqlParser.OrderByExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#columnExpr.
    def visitColumnExpr(self, ctx:AqlParser.ColumnExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#containsExpr.
    def visitContainsExpr(self, ctx:AqlParser.ContainsExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#identifiedExpr.
    def visitIdentifiedExpr(self, ctx:AqlParser.IdentifiedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#classExpression.
    def visitClassExpression(self, ctx:AqlParser.ClassExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#versionClassExpr.
    def visitVersionClassExpr(self, ctx:AqlParser.VersionClassExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#terminal.
    def visitTerminal(self, ctx:AqlParser.TerminalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#identifiedPath.
    def visitIdentifiedPath(self, ctx:AqlParser.IdentifiedPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#pathPredicate.
    def visitPathPredicate(self, ctx:AqlParser.PathPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#standardPredicate.
    def visitStandardPredicate(self, ctx:AqlParser.StandardPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#archetypePredicate.
    def visitArchetypePredicate(self, ctx:AqlParser.ArchetypePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#nodePredicate.
    def visitNodePredicate(self, ctx:AqlParser.NodePredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#versionPredicate.
    def visitVersionPredicate(self, ctx:AqlParser.VersionPredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#pathPredicateOperand.
    def visitPathPredicateOperand(self, ctx:AqlParser.PathPredicateOperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#objectPath.
    def visitObjectPath(self, ctx:AqlParser.ObjectPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#pathPart.
    def visitPathPart(self, ctx:AqlParser.PathPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#likeOperand.
    def visitLikeOperand(self, ctx:AqlParser.LikeOperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#matchesOperand.
    def visitMatchesOperand(self, ctx:AqlParser.MatchesOperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#valueListItem.
    def visitValueListItem(self, ctx:AqlParser.ValueListItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#primitive.
    def visitPrimitive(self, ctx:AqlParser.PrimitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#numericPrimitive.
    def visitNumericPrimitive(self, ctx:AqlParser.NumericPrimitiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#functionCall.
    def visitFunctionCall(self, ctx:AqlParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#aggregateFunctionCall.
    def visitAggregateFunctionCall(self, ctx:AqlParser.AggregateFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#terminologyFunction.
    def visitTerminologyFunction(self, ctx:AqlParser.TerminologyFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AqlParser#top.
    def visitTop(self, ctx:AqlParser.TopContext):
        return self.visitChildren(ctx)



del AqlParser