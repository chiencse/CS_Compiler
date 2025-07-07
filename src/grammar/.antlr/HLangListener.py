# Generated from /home/chieens/hlang-compiler/src/grammar/HLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .HLangParser import HLangParser
else:
    from HLangParser import HLangParser

# This class defines a complete listener for a parse tree produced by HLangParser.
class HLangListener(ParseTreeListener):

    # Enter a parse tree produced by HLangParser#program.
    def enterProgram(self, ctx:HLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by HLangParser#program.
    def exitProgram(self, ctx:HLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by HLangParser#constdecl.
    def enterConstdecl(self, ctx:HLangParser.ConstdeclContext):
        pass

    # Exit a parse tree produced by HLangParser#constdecl.
    def exitConstdecl(self, ctx:HLangParser.ConstdeclContext):
        pass


    # Enter a parse tree produced by HLangParser#vardecl.
    def enterVardecl(self, ctx:HLangParser.VardeclContext):
        pass

    # Exit a parse tree produced by HLangParser#vardecl.
    def exitVardecl(self, ctx:HLangParser.VardeclContext):
        pass


    # Enter a parse tree produced by HLangParser#typ_anno.
    def enterTyp_anno(self, ctx:HLangParser.Typ_annoContext):
        pass

    # Exit a parse tree produced by HLangParser#typ_anno.
    def exitTyp_anno(self, ctx:HLangParser.Typ_annoContext):
        pass


    # Enter a parse tree produced by HLangParser#typ.
    def enterTyp(self, ctx:HLangParser.TypContext):
        pass

    # Exit a parse tree produced by HLangParser#typ.
    def exitTyp(self, ctx:HLangParser.TypContext):
        pass


    # Enter a parse tree produced by HLangParser#array_type.
    def enterArray_type(self, ctx:HLangParser.Array_typeContext):
        pass

    # Exit a parse tree produced by HLangParser#array_type.
    def exitArray_type(self, ctx:HLangParser.Array_typeContext):
        pass


    # Enter a parse tree produced by HLangParser#funcdecl.
    def enterFuncdecl(self, ctx:HLangParser.FuncdeclContext):
        pass

    # Exit a parse tree produced by HLangParser#funcdecl.
    def exitFuncdecl(self, ctx:HLangParser.FuncdeclContext):
        pass


    # Enter a parse tree produced by HLangParser#return_typ.
    def enterReturn_typ(self, ctx:HLangParser.Return_typContext):
        pass

    # Exit a parse tree produced by HLangParser#return_typ.
    def exitReturn_typ(self, ctx:HLangParser.Return_typContext):
        pass


    # Enter a parse tree produced by HLangParser#paramlist.
    def enterParamlist(self, ctx:HLangParser.ParamlistContext):
        pass

    # Exit a parse tree produced by HLangParser#paramlist.
    def exitParamlist(self, ctx:HLangParser.ParamlistContext):
        pass


    # Enter a parse tree produced by HLangParser#params.
    def enterParams(self, ctx:HLangParser.ParamsContext):
        pass

    # Exit a parse tree produced by HLangParser#params.
    def exitParams(self, ctx:HLangParser.ParamsContext):
        pass


    # Enter a parse tree produced by HLangParser#param.
    def enterParam(self, ctx:HLangParser.ParamContext):
        pass

    # Exit a parse tree produced by HLangParser#param.
    def exitParam(self, ctx:HLangParser.ParamContext):
        pass


    # Enter a parse tree produced by HLangParser#body.
    def enterBody(self, ctx:HLangParser.BodyContext):
        pass

    # Exit a parse tree produced by HLangParser#body.
    def exitBody(self, ctx:HLangParser.BodyContext):
        pass


    # Enter a parse tree produced by HLangParser#stmtlist.
    def enterStmtlist(self, ctx:HLangParser.StmtlistContext):
        pass

    # Exit a parse tree produced by HLangParser#stmtlist.
    def exitStmtlist(self, ctx:HLangParser.StmtlistContext):
        pass


    # Enter a parse tree produced by HLangParser#stmt.
    def enterStmt(self, ctx:HLangParser.StmtContext):
        pass

    # Exit a parse tree produced by HLangParser#stmt.
    def exitStmt(self, ctx:HLangParser.StmtContext):
        pass


    # Enter a parse tree produced by HLangParser#break_stmt.
    def enterBreak_stmt(self, ctx:HLangParser.Break_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#break_stmt.
    def exitBreak_stmt(self, ctx:HLangParser.Break_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#continue_stmt.
    def enterContinue_stmt(self, ctx:HLangParser.Continue_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#continue_stmt.
    def exitContinue_stmt(self, ctx:HLangParser.Continue_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#assign_stmt.
    def enterAssign_stmt(self, ctx:HLangParser.Assign_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#assign_stmt.
    def exitAssign_stmt(self, ctx:HLangParser.Assign_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#lvalue.
    def enterLvalue(self, ctx:HLangParser.LvalueContext):
        pass

    # Exit a parse tree produced by HLangParser#lvalue.
    def exitLvalue(self, ctx:HLangParser.LvalueContext):
        pass


    # Enter a parse tree produced by HLangParser#condition_stmt.
    def enterCondition_stmt(self, ctx:HLangParser.Condition_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#condition_stmt.
    def exitCondition_stmt(self, ctx:HLangParser.Condition_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#elif_list.
    def enterElif_list(self, ctx:HLangParser.Elif_listContext):
        pass

    # Exit a parse tree produced by HLangParser#elif_list.
    def exitElif_list(self, ctx:HLangParser.Elif_listContext):
        pass


    # Enter a parse tree produced by HLangParser#else_part.
    def enterElse_part(self, ctx:HLangParser.Else_partContext):
        pass

    # Exit a parse tree produced by HLangParser#else_part.
    def exitElse_part(self, ctx:HLangParser.Else_partContext):
        pass


    # Enter a parse tree produced by HLangParser#while_stmt.
    def enterWhile_stmt(self, ctx:HLangParser.While_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#while_stmt.
    def exitWhile_stmt(self, ctx:HLangParser.While_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#for_stmt.
    def enterFor_stmt(self, ctx:HLangParser.For_stmtContext):
        pass

    # Exit a parse tree produced by HLangParser#for_stmt.
    def exitFor_stmt(self, ctx:HLangParser.For_stmtContext):
        pass


    # Enter a parse tree produced by HLangParser#block_statement.
    def enterBlock_statement(self, ctx:HLangParser.Block_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#block_statement.
    def exitBlock_statement(self, ctx:HLangParser.Block_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#return.
    def enterReturn(self, ctx:HLangParser.ReturnContext):
        pass

    # Exit a parse tree produced by HLangParser#return.
    def exitReturn(self, ctx:HLangParser.ReturnContext):
        pass


    # Enter a parse tree produced by HLangParser#literal.
    def enterLiteral(self, ctx:HLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by HLangParser#literal.
    def exitLiteral(self, ctx:HLangParser.LiteralContext):
        pass


    # Enter a parse tree produced by HLangParser#array_literal.
    def enterArray_literal(self, ctx:HLangParser.Array_literalContext):
        pass

    # Exit a parse tree produced by HLangParser#array_literal.
    def exitArray_literal(self, ctx:HLangParser.Array_literalContext):
        pass


    # Enter a parse tree produced by HLangParser#array_access.
    def enterArray_access(self, ctx:HLangParser.Array_accessContext):
        pass

    # Exit a parse tree produced by HLangParser#array_access.
    def exitArray_access(self, ctx:HLangParser.Array_accessContext):
        pass


    # Enter a parse tree produced by HLangParser#multi_access.
    def enterMulti_access(self, ctx:HLangParser.Multi_accessContext):
        pass

    # Exit a parse tree produced by HLangParser#multi_access.
    def exitMulti_access(self, ctx:HLangParser.Multi_accessContext):
        pass


    # Enter a parse tree produced by HLangParser#index_access.
    def enterIndex_access(self, ctx:HLangParser.Index_accessContext):
        pass

    # Exit a parse tree produced by HLangParser#index_access.
    def exitIndex_access(self, ctx:HLangParser.Index_accessContext):
        pass


    # Enter a parse tree produced by HLangParser#func_call.
    def enterFunc_call(self, ctx:HLangParser.Func_callContext):
        pass

    # Exit a parse tree produced by HLangParser#func_call.
    def exitFunc_call(self, ctx:HLangParser.Func_callContext):
        pass


    # Enter a parse tree produced by HLangParser#arg_list.
    def enterArg_list(self, ctx:HLangParser.Arg_listContext):
        pass

    # Exit a parse tree produced by HLangParser#arg_list.
    def exitArg_list(self, ctx:HLangParser.Arg_listContext):
        pass


    # Enter a parse tree produced by HLangParser#args.
    def enterArgs(self, ctx:HLangParser.ArgsContext):
        pass

    # Exit a parse tree produced by HLangParser#args.
    def exitArgs(self, ctx:HLangParser.ArgsContext):
        pass


    # Enter a parse tree produced by HLangParser#expr.
    def enterExpr(self, ctx:HLangParser.ExprContext):
        pass

    # Exit a parse tree produced by HLangParser#expr.
    def exitExpr(self, ctx:HLangParser.ExprContext):
        pass


    # Enter a parse tree produced by HLangParser#expr1.
    def enterExpr1(self, ctx:HLangParser.Expr1Context):
        pass

    # Exit a parse tree produced by HLangParser#expr1.
    def exitExpr1(self, ctx:HLangParser.Expr1Context):
        pass


    # Enter a parse tree produced by HLangParser#expr2.
    def enterExpr2(self, ctx:HLangParser.Expr2Context):
        pass

    # Exit a parse tree produced by HLangParser#expr2.
    def exitExpr2(self, ctx:HLangParser.Expr2Context):
        pass


    # Enter a parse tree produced by HLangParser#expr3.
    def enterExpr3(self, ctx:HLangParser.Expr3Context):
        pass

    # Exit a parse tree produced by HLangParser#expr3.
    def exitExpr3(self, ctx:HLangParser.Expr3Context):
        pass


    # Enter a parse tree produced by HLangParser#expr4.
    def enterExpr4(self, ctx:HLangParser.Expr4Context):
        pass

    # Exit a parse tree produced by HLangParser#expr4.
    def exitExpr4(self, ctx:HLangParser.Expr4Context):
        pass


    # Enter a parse tree produced by HLangParser#expr5.
    def enterExpr5(self, ctx:HLangParser.Expr5Context):
        pass

    # Exit a parse tree produced by HLangParser#expr5.
    def exitExpr5(self, ctx:HLangParser.Expr5Context):
        pass


    # Enter a parse tree produced by HLangParser#expr6.
    def enterExpr6(self, ctx:HLangParser.Expr6Context):
        pass

    # Exit a parse tree produced by HLangParser#expr6.
    def exitExpr6(self, ctx:HLangParser.Expr6Context):
        pass


    # Enter a parse tree produced by HLangParser#expr7.
    def enterExpr7(self, ctx:HLangParser.Expr7Context):
        pass

    # Exit a parse tree produced by HLangParser#expr7.
    def exitExpr7(self, ctx:HLangParser.Expr7Context):
        pass


    # Enter a parse tree produced by HLangParser#expr8.
    def enterExpr8(self, ctx:HLangParser.Expr8Context):
        pass

    # Exit a parse tree produced by HLangParser#expr8.
    def exitExpr8(self, ctx:HLangParser.Expr8Context):
        pass


    # Enter a parse tree produced by HLangParser#expr9.
    def enterExpr9(self, ctx:HLangParser.Expr9Context):
        pass

    # Exit a parse tree produced by HLangParser#expr9.
    def exitExpr9(self, ctx:HLangParser.Expr9Context):
        pass



del HLangParser