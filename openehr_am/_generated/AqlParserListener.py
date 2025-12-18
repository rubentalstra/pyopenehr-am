# Generated from grammars/aql/AqlParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AqlParser import AqlParser
else:
    from AqlParser import AqlParser

# This class defines a complete listener for a parse tree produced by AqlParser.
class AqlParserListener(ParseTreeListener):

    # Enter a parse tree produced by AqlParser#selectQuery.
    def enterSelectQuery(self, ctx:AqlParser.SelectQueryContext):
        pass

    # Exit a parse tree produced by AqlParser#selectQuery.
    def exitSelectQuery(self, ctx:AqlParser.SelectQueryContext):
        pass


    # Enter a parse tree produced by AqlParser#selectClause.
    def enterSelectClause(self, ctx:AqlParser.SelectClauseContext):
        pass

    # Exit a parse tree produced by AqlParser#selectClause.
    def exitSelectClause(self, ctx:AqlParser.SelectClauseContext):
        pass


    # Enter a parse tree produced by AqlParser#fromClause.
    def enterFromClause(self, ctx:AqlParser.FromClauseContext):
        pass

    # Exit a parse tree produced by AqlParser#fromClause.
    def exitFromClause(self, ctx:AqlParser.FromClauseContext):
        pass


    # Enter a parse tree produced by AqlParser#whereClause.
    def enterWhereClause(self, ctx:AqlParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by AqlParser#whereClause.
    def exitWhereClause(self, ctx:AqlParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by AqlParser#orderByClause.
    def enterOrderByClause(self, ctx:AqlParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by AqlParser#orderByClause.
    def exitOrderByClause(self, ctx:AqlParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by AqlParser#limitClause.
    def enterLimitClause(self, ctx:AqlParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by AqlParser#limitClause.
    def exitLimitClause(self, ctx:AqlParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by AqlParser#selectExpr.
    def enterSelectExpr(self, ctx:AqlParser.SelectExprContext):
        pass

    # Exit a parse tree produced by AqlParser#selectExpr.
    def exitSelectExpr(self, ctx:AqlParser.SelectExprContext):
        pass


    # Enter a parse tree produced by AqlParser#fromExpr.
    def enterFromExpr(self, ctx:AqlParser.FromExprContext):
        pass

    # Exit a parse tree produced by AqlParser#fromExpr.
    def exitFromExpr(self, ctx:AqlParser.FromExprContext):
        pass


    # Enter a parse tree produced by AqlParser#whereExpr.
    def enterWhereExpr(self, ctx:AqlParser.WhereExprContext):
        pass

    # Exit a parse tree produced by AqlParser#whereExpr.
    def exitWhereExpr(self, ctx:AqlParser.WhereExprContext):
        pass


    # Enter a parse tree produced by AqlParser#orderByExpr.
    def enterOrderByExpr(self, ctx:AqlParser.OrderByExprContext):
        pass

    # Exit a parse tree produced by AqlParser#orderByExpr.
    def exitOrderByExpr(self, ctx:AqlParser.OrderByExprContext):
        pass


    # Enter a parse tree produced by AqlParser#columnExpr.
    def enterColumnExpr(self, ctx:AqlParser.ColumnExprContext):
        pass

    # Exit a parse tree produced by AqlParser#columnExpr.
    def exitColumnExpr(self, ctx:AqlParser.ColumnExprContext):
        pass


    # Enter a parse tree produced by AqlParser#containsExpr.
    def enterContainsExpr(self, ctx:AqlParser.ContainsExprContext):
        pass

    # Exit a parse tree produced by AqlParser#containsExpr.
    def exitContainsExpr(self, ctx:AqlParser.ContainsExprContext):
        pass


    # Enter a parse tree produced by AqlParser#identifiedExpr.
    def enterIdentifiedExpr(self, ctx:AqlParser.IdentifiedExprContext):
        pass

    # Exit a parse tree produced by AqlParser#identifiedExpr.
    def exitIdentifiedExpr(self, ctx:AqlParser.IdentifiedExprContext):
        pass


    # Enter a parse tree produced by AqlParser#classExpression.
    def enterClassExpression(self, ctx:AqlParser.ClassExpressionContext):
        pass

    # Exit a parse tree produced by AqlParser#classExpression.
    def exitClassExpression(self, ctx:AqlParser.ClassExpressionContext):
        pass


    # Enter a parse tree produced by AqlParser#versionClassExpr.
    def enterVersionClassExpr(self, ctx:AqlParser.VersionClassExprContext):
        pass

    # Exit a parse tree produced by AqlParser#versionClassExpr.
    def exitVersionClassExpr(self, ctx:AqlParser.VersionClassExprContext):
        pass


    # Enter a parse tree produced by AqlParser#terminal.
    def enterTerminal(self, ctx:AqlParser.TerminalContext):
        pass

    # Exit a parse tree produced by AqlParser#terminal.
    def exitTerminal(self, ctx:AqlParser.TerminalContext):
        pass


    # Enter a parse tree produced by AqlParser#identifiedPath.
    def enterIdentifiedPath(self, ctx:AqlParser.IdentifiedPathContext):
        pass

    # Exit a parse tree produced by AqlParser#identifiedPath.
    def exitIdentifiedPath(self, ctx:AqlParser.IdentifiedPathContext):
        pass


    # Enter a parse tree produced by AqlParser#pathPredicate.
    def enterPathPredicate(self, ctx:AqlParser.PathPredicateContext):
        pass

    # Exit a parse tree produced by AqlParser#pathPredicate.
    def exitPathPredicate(self, ctx:AqlParser.PathPredicateContext):
        pass


    # Enter a parse tree produced by AqlParser#standardPredicate.
    def enterStandardPredicate(self, ctx:AqlParser.StandardPredicateContext):
        pass

    # Exit a parse tree produced by AqlParser#standardPredicate.
    def exitStandardPredicate(self, ctx:AqlParser.StandardPredicateContext):
        pass


    # Enter a parse tree produced by AqlParser#archetypePredicate.
    def enterArchetypePredicate(self, ctx:AqlParser.ArchetypePredicateContext):
        pass

    # Exit a parse tree produced by AqlParser#archetypePredicate.
    def exitArchetypePredicate(self, ctx:AqlParser.ArchetypePredicateContext):
        pass


    # Enter a parse tree produced by AqlParser#nodePredicate.
    def enterNodePredicate(self, ctx:AqlParser.NodePredicateContext):
        pass

    # Exit a parse tree produced by AqlParser#nodePredicate.
    def exitNodePredicate(self, ctx:AqlParser.NodePredicateContext):
        pass


    # Enter a parse tree produced by AqlParser#versionPredicate.
    def enterVersionPredicate(self, ctx:AqlParser.VersionPredicateContext):
        pass

    # Exit a parse tree produced by AqlParser#versionPredicate.
    def exitVersionPredicate(self, ctx:AqlParser.VersionPredicateContext):
        pass


    # Enter a parse tree produced by AqlParser#pathPredicateOperand.
    def enterPathPredicateOperand(self, ctx:AqlParser.PathPredicateOperandContext):
        pass

    # Exit a parse tree produced by AqlParser#pathPredicateOperand.
    def exitPathPredicateOperand(self, ctx:AqlParser.PathPredicateOperandContext):
        pass


    # Enter a parse tree produced by AqlParser#objectPath.
    def enterObjectPath(self, ctx:AqlParser.ObjectPathContext):
        pass

    # Exit a parse tree produced by AqlParser#objectPath.
    def exitObjectPath(self, ctx:AqlParser.ObjectPathContext):
        pass


    # Enter a parse tree produced by AqlParser#pathPart.
    def enterPathPart(self, ctx:AqlParser.PathPartContext):
        pass

    # Exit a parse tree produced by AqlParser#pathPart.
    def exitPathPart(self, ctx:AqlParser.PathPartContext):
        pass


    # Enter a parse tree produced by AqlParser#likeOperand.
    def enterLikeOperand(self, ctx:AqlParser.LikeOperandContext):
        pass

    # Exit a parse tree produced by AqlParser#likeOperand.
    def exitLikeOperand(self, ctx:AqlParser.LikeOperandContext):
        pass


    # Enter a parse tree produced by AqlParser#matchesOperand.
    def enterMatchesOperand(self, ctx:AqlParser.MatchesOperandContext):
        pass

    # Exit a parse tree produced by AqlParser#matchesOperand.
    def exitMatchesOperand(self, ctx:AqlParser.MatchesOperandContext):
        pass


    # Enter a parse tree produced by AqlParser#valueListItem.
    def enterValueListItem(self, ctx:AqlParser.ValueListItemContext):
        pass

    # Exit a parse tree produced by AqlParser#valueListItem.
    def exitValueListItem(self, ctx:AqlParser.ValueListItemContext):
        pass


    # Enter a parse tree produced by AqlParser#primitive.
    def enterPrimitive(self, ctx:AqlParser.PrimitiveContext):
        pass

    # Exit a parse tree produced by AqlParser#primitive.
    def exitPrimitive(self, ctx:AqlParser.PrimitiveContext):
        pass


    # Enter a parse tree produced by AqlParser#numericPrimitive.
    def enterNumericPrimitive(self, ctx:AqlParser.NumericPrimitiveContext):
        pass

    # Exit a parse tree produced by AqlParser#numericPrimitive.
    def exitNumericPrimitive(self, ctx:AqlParser.NumericPrimitiveContext):
        pass


    # Enter a parse tree produced by AqlParser#functionCall.
    def enterFunctionCall(self, ctx:AqlParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by AqlParser#functionCall.
    def exitFunctionCall(self, ctx:AqlParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by AqlParser#aggregateFunctionCall.
    def enterAggregateFunctionCall(self, ctx:AqlParser.AggregateFunctionCallContext):
        pass

    # Exit a parse tree produced by AqlParser#aggregateFunctionCall.
    def exitAggregateFunctionCall(self, ctx:AqlParser.AggregateFunctionCallContext):
        pass


    # Enter a parse tree produced by AqlParser#terminologyFunction.
    def enterTerminologyFunction(self, ctx:AqlParser.TerminologyFunctionContext):
        pass

    # Exit a parse tree produced by AqlParser#terminologyFunction.
    def exitTerminologyFunction(self, ctx:AqlParser.TerminologyFunctionContext):
        pass


    # Enter a parse tree produced by AqlParser#top.
    def enterTop(self, ctx:AqlParser.TopContext):
        pass

    # Exit a parse tree produced by AqlParser#top.
    def exitTop(self, ctx:AqlParser.TopContext):
        pass



del AqlParser