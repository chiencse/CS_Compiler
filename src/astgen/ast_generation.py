"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *

class ASTGeneration(HLangVisitor):
    # Visit a parse tree produced by HLangParser#program.
    # program : constdecl* funcdecl* EOF ;
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        const_decls = [self.visit(child) for child in ctx.constdecl()]
        func_decls = [self.visit(child) for child in ctx.funcdecl()]
        return Program(const_decls, func_decls)

    # Visit a parse tree produced by HLangParser#constdecl.
    # constdecl : CONST IDENTIFIER typ_anno ASS expr SM ;
    def visitConstdecl(self, ctx: HLangParser.ConstdeclContext):
        name = ctx.IDENTIFIER().getText()
        type_annotation = self.visit(ctx.typ_anno())
        expr = self.visit(ctx.expr())
        return ConstDecl(name, type_annotation, expr)

    # Visit a parse tree produced by HLangParser#vardecl.
    # vardecl : LET IDENTIFIER typ_anno ASS expr ;
    def visitVardecl(self, ctx: HLangParser.VardeclContext):
        name = ctx.IDENTIFIER().getText()
        type_annotation = self.visit(ctx.typ_anno())
        expr = self.visit(ctx.expr())
        return VarDecl(name, type_annotation, expr)

    # Visit a parse tree produced by HLangParser#typ_anno.
    # typ_anno : COLON typ | ;
    def visitTyp_anno(self, ctx: HLangParser.Typ_annoContext):
        return self.visit(ctx.typ()) if ctx.typ() else None

    # Visit a parse tree produced by HLangParser#typ.
    # typ : INT | FLOAT | BOOL | STRING | array_type;
    def visitTyp(self, ctx: HLangParser.TypContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        return None

    # Visit a parse tree produced by HLangParser#array_type.
    # array_type : LS typ SM INT_LITERAL RS ;
    def visitArray_type(self, ctx: HLangParser.Array_typeContext):
        element_type = self.visit(ctx.typ())
        size = int(ctx.INT_LITERAL().getText())
        return ArrayType(element_type, size)

    # Visit a parse tree produced by HLangParser#funcdecl.
    # funcdecl : FUNC IDENTIFIER LR paramlist RR ARROW return_typ body ;
    def visitFuncdecl(self, ctx: HLangParser.FuncdeclContext):
        # print("----------Visiting funcdecl--------------")
        name = ctx.IDENTIFIER().getText()
        params = self.visit(ctx.paramlist())
        return_type = self.visit(ctx.return_typ())
        body = self.visit(ctx.body())
        return FuncDecl(name, params, return_type, body)

    # Visit a parse tree produced by HLangParser#return_typ.
    # return_typ : typ | VOID ;
    def visitReturn_typ(self, ctx: HLangParser.Return_typContext):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.typ())

    # Visit a parse tree produced by HLangParser#paramlist.
    # paramlist : params | ;
    def visitParamlist(self, ctx: HLangParser.ParamlistContext):
        return self.visit(ctx.params()) if ctx.params() else []

    # Visit a parse tree produced by HLangParser#params.
    # params : param CM params | param ;
    def visitParams(self, ctx: HLangParser.ParamsContext):
        params = [self.visit(ctx.param())]
        if ctx.params():
            params.extend(self.visit(ctx.params()))
        return params

    # Visit a parse tree produced by HLangParser#param.
    # param : IDENTIFIER COLON typ ;
    def visitParam(self, ctx: HLangParser.ParamContext):
        name = ctx.IDENTIFIER().getText()
        param_type = self.visit(ctx.typ())
        return Param(name, param_type)

    # Visit a parse tree produced by HLangParser#body.
    # body : LC stmtlist RC ;
    def visitBody(self, ctx: HLangParser.BodyContext):
        return self.visit(ctx.stmtlist())
        

    # Visit a parse tree produced by HLangParser#stmtlist.
    # stmtlist : stmt stmtlist | ;
    def visitStmtlist(self, ctx: HLangParser.StmtlistContext):
        if not ctx.stmt():
            return []
        statements = [self.visit(ctx.stmt())]
        if ctx.stmtlist():
            statements.extend(self.visit(ctx.stmtlist()))
        return statements

    # Visit a parse tree produced by HLangParser#stmt.
    # stmt : vardecl SM | func_call SM | expr SM | return SM | assign_stmt SM | condition_stmt 
    # | while_stmt | for_stmt |block_statement | break_stmt SM| continue_stmt SM;
    def visitStmt(self, ctx: HLangParser.StmtContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.func_call():
            return ExprStmt(self.visit(ctx.func_call())) #! Check is exist
        elif ctx.expr():
            return ExprStmt(self.visit(ctx.expr()))
        elif ctx.return_():
            return self.visit(ctx.return_())
        elif ctx.assign_stmt():
            return self.visit(ctx.assign_stmt())
        elif ctx.condition_stmt():
            return self.visit(ctx.condition_stmt())
        elif ctx.while_stmt():
            return self.visit(ctx.while_stmt())
        elif ctx.for_stmt():
            return self.visit(ctx.for_stmt())
        elif ctx.block_statement():
            return self.visit(ctx.block_statement())
        elif ctx.break_stmt():
            return self.visit(ctx.break_stmt())
        elif ctx.continue_stmt():
            return self.visit(ctx.continue_stmt())
        return None

    # Visit a parse tree produced by HLangParser#break_stmt.
    def visitBreak_stmt(self, ctx: HLangParser.Break_stmtContext):
        return BreakStmt()

    # Visit a parse tree produced by HLangParser#continue_stmt.
    def visitContinue_stmt(self, ctx: HLangParser.Continue_stmtContext):
        return ContinueStmt()

    # Visit a parse tree produced by HLangParser#assign_stmt.
    # assign_stmt : lvalue ASS expr;
    def visitAssign_stmt(self, ctx: HLangParser.Assign_stmtContext):
        lvalue = self.visit(ctx.lvalue())
        value = self.visit(ctx.expr())
        return Assignment(lvalue, value)

    # Visit a parse tree produced by HLangParser#lvalue.
    # lvalue : IDENTIFIER array_literal | IDENTIFIER ;
    # lvalue : array_access | IDENTIFIER ;
    def visitLvalue(self, ctx: HLangParser.LvalueContext):
        # name = ctx.IDENTIFIER().getText()
        # base = IdLValue(name)
        # if ctx.array_literal():
        #     array_literal = self.visit(ctx.array_literal())  # ArrayLiteral
        #     for idx in array_literal.elements:
        #         base = ArrayAccessLValue(base, idx)
        #     return base
        base = IdLValue(ctx.IDENTIFIER().getText())
        if ctx.multi_access():
            indices = self.visit(ctx.multi_access())  # List of expressions
            for idx in indices:
                base = ArrayAccessLValue(base, idx)
        return base

    # Visit a parse tree produced by HLangParser#condition_stmt.
    # condition_stmt : IF LR expr RR body elif_list else_part;
    def visitCondition_stmt(self, ctx: HLangParser.Condition_stmtContext):
        condition = self.visit(ctx.expr())
        then_stmt = BlockStmt(self.visit(ctx.body()))
        elif_branches = self.visit(ctx.elif_list()) 
        else_stmt = self.visit(ctx.else_part()) 
        return IfStmt(condition, then_stmt, elif_branches, else_stmt)

    # Visit a parse tree produced by HLangParser#elif_list.
    # elif_list : ELIF LR expr RR body elif_list | ;
    def visitElif_list(self, ctx: HLangParser.Elif_listContext):
        # debug_ctx(ctx, rule_name="visitElif_list", visitor=self)
        if ctx.getChildCount() > 0:
            condition = self.visit(ctx.expr())
            body = BlockStmt(self.visit(ctx.body()))
            elif_branches = [(condition, body)]
            if ctx.elif_list():
                elif_branches.extend(self.visit(ctx.elif_list()))
            return elif_branches
        return []

    # Visit a parse tree produced by HLangParser#else_part.
    #else_part : ELSE body | ;
    def visitElse_part(self, ctx: HLangParser.Else_partContext):
        # print("----------Visiting else_part--------------")
        if ctx.ELSE():
            return BlockStmt(self.visit(ctx.body()))
        return None  

    # Visit a parse tree produced by HLangParser#while_stmt.
    # while_stmt : WHILE LR expr RR body ;
    def visitWhile_stmt(self, ctx: HLangParser.While_stmtContext):
        condition = self.visit(ctx.expr())
        body = BlockStmt(self.visit(ctx.body()))
        return WhileStmt(condition, body)

    # Visit a parse tree produced by HLangParser#for_stmt.
    # for_stmt : FOR LR IDENTIFIER IN expr RR body ;
    def visitFor_stmt(self, ctx: HLangParser.For_stmtContext):
        variable = ctx.IDENTIFIER().getText()
        iterable = self.visit(ctx.expr())
        body = BlockStmt(self.visit(ctx.body()))
        return ForStmt(variable, iterable, body)

    # Visit a parse tree produced by HLangParser#block_statement.
    # block_statement : LC stmtlist RC ;
    def visitBlock_statement(self, ctx: HLangParser.Block_statementContext):
        statements = self.visit(ctx.stmtlist())
        return BlockStmt(statements)

    # Visit a parse tree produced by HLangParser#return.
    # return : RETURN (expr | )  ;
    def visitReturn(self, ctx: HLangParser.ReturnContext):
        value = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(value)

    # Visit a parse tree produced by HLangParser#literal.
     #literal: INT_LITERAL | FLOAT_LITERAL | TRUE | FALSE | STRING_LITERAL | array_literal;
    def visitLiteral(self, ctx: HLangParser.LiteralContext):
        # debug_ctx(ctx, rule_name="visitLiteral", visitor=self)
        if ctx.INT_LITERAL():
            return IntegerLiteral(int(ctx.INT_LITERAL().getText()))
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(float(ctx.FLOAT_LITERAL().getText()))
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())
        return None

    # Visit a parse tree produced by HLangParser#array_literal.
    # array_literal : LS arg_list RS  array_literal | LS arg_list RS;
    def visitArray_literal(self, ctx: HLangParser.Array_literalContext):
        elements = self.visit(ctx.arg_list()) if ctx.arg_list() else []
        return ArrayLiteral(elements)

    # Visit a parse tree produced by HLangParser#array_access.
    # array_access : (IDENTIFIER | func_call | LR expr RR | literal) multi_access ;
    
    def visitArray_access(self, ctx: HLangParser.Array_accessContext):
        # debug_ctx(ctx, rule_name="visitArray_access", visitor=self)
    
        base = self.visit(ctx.getChild(0))  #func_call, or literal
        if ctx.IDENTIFIER():
            base = Identifier(ctx.IDENTIFIER().getText())
        if ctx.getChildCount() == 3:  # LR expr RR
            base = self.visit(ctx.expr())
        indices = self.visit(ctx.multi_access())
        # Fold multiple indices into nested ArrayAccess nodes}")
        res = reduce(lambda arr, idx: ArrayAccess(arr, idx), indices, base)
        return res
    # Visit a parse tree produced by HLangParser#multi_access.
    # multi_access : index_access multi_access | index_access;
    def visitMulti_access(self, ctx: HLangParser.Multi_accessContext):
        # print("----------Visiting multi_access--------------")
        indices = [self.visit(ctx.index_access())]
        if ctx.multi_access():
            indices.extend(self.visit(ctx.multi_access()))
        return indices

    # Visit a parse tree produced by HLangParser#index_access.
    # index_access : LS expr RS ;
    def visitIndex_access(self, ctx: HLangParser.Index_accessContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by HLangParser#func_call.
    # func_call: (IDENTIFIER | INT | FLOAT ) LR arg_list RR ;
    def visitFunc_call(self, ctx: HLangParser.Func_callContext):
        function = Identifier(ctx.getChild(0).getText()) 
        args = self.visit(ctx.arg_list())
        return FunctionCall(function, args)

    # Visit a parse tree produced by HLangParser#arg_list.
    # arg_list : args | ;
    def visitArg_list(self, ctx: HLangParser.Arg_listContext):
        return self.visit(ctx.args()) if ctx.args() else []

    # Visit a parse tree produced by HLangParser#args.
    # args: expr CM args | expr;
    def visitArgs(self, ctx: HLangParser.ArgsContext):
        args = [self.visit(ctx.expr())]
        if ctx.args():
            args.extend(self.visit(ctx.args()))
        return args

    # Visit a parse tree produced by HLangParser#expr.
    # expr    : expr PIPE expr1 | expr1 ;
    def visitExpr(self, ctx: HLangParser.ExprContext):
        if ctx.PIPE():
           return BinaryOp(self.visit(ctx.expr()), ctx.PIPE().getText(), self.visit(ctx.expr1()))
        return self.visit(ctx.expr1())

    # Visit a parse tree produced by HLangParser#expr1.
    # expr1   : expr1 OR expr2 | expr2 ;
    def visitExpr1(self, ctx: HLangParser.Expr1Context):
        # print("----------Visiting expr1--------------")
        if ctx.OR():
            return BinaryOp(self.visit(ctx.expr1()), ctx.OR().getText(), self.visit(ctx.expr2()))
        return self.visit(ctx.expr2())

    # Visit a parse tree produced by HLangParser#expr2.
    # expr2   : expr2 AND expr3 | expr3 ;
    def visitExpr2(self, ctx: HLangParser.Expr2Context):
        # print("----------Visiting expr2--------------")
        if ctx.AND():
            operator = ctx.AND().getText()
            return BinaryOp(self.visit(ctx.expr2()), operator, self.visit(ctx.expr3()))
        return self.visit(ctx.expr3())

    # Visit a parse tree produced by HLangParser#expr3.
    # expr3   : expr3 (EQ | NEQ) expr4 | expr4 ;
    def visitExpr3(self, ctx: HLangParser.Expr3Context):
        # print("----------Visiting expr3--------------")
    
        if ctx.getChildCount() == 3:
            operator = ctx.getChild(1).getText()
            return BinaryOp(self.visit(ctx.expr3()), operator, self.visit(ctx.expr4()))
        return self.visit(ctx.expr4()) 

    # Visit a parse tree produced by HLangParser#expr4.
    # expr4   : expr4 (LT | LTE | GT | GTE) expr5 | expr5 ;
    def visitExpr4(self, ctx: HLangParser.Expr4Context):
        # print("----------Visiting expr4--------------")
        if ctx.getChildCount() == 3:
            operator = ctx.getChild(1).getText()
            return BinaryOp(self.visit(ctx.expr4()), operator, self.visit(ctx.expr5()))
        return self.visit(ctx.expr5())

    # Visit a parse tree produced by HLangParser#expr5.
    # expr5   : expr5 (ADD | MINUS) expr6 | expr6 ;
    def visitExpr5(self, ctx: HLangParser.Expr5Context):
        # print("----------Visiting expr5--------------")
        # debug_ctx(ctx, rule_name="visitExpr5", visitor=self)
        if ctx.getChildCount() == 3:
            operator = ctx.getChild(1).getText()
            return BinaryOp(self.visit(ctx.expr5()), operator, self.visit(ctx.expr6()))
        return self.visit(ctx.expr6())

    # Visit a parse tree produced by HLangParser#expr6.
    # expr6   : expr6 (MUL | DIV | MOD) expr7 | expr7 ;
    def visitExpr6(self, ctx: HLangParser.Expr6Context):
        # print("----------Visiting expr6--------------")
        # debug_ctx(ctx, rule_name="visitExpr6", visitor=self)
        if ctx.getChildCount() == 3:
            operator = ctx.getChild(1).getText()
            return BinaryOp(self.visit(ctx.expr6()), operator, self.visit(ctx.expr7()))
        return self.visit(ctx.expr7())

    # Visit a parse tree produced by HLangParser#expr7.
    # expr7   : (NOT | MINUS | ADD) expr7 | expr8 ;
    def visitExpr7(self, ctx: HLangParser.Expr7Context):
        # print("----------Visiting expr7--------------")
        if ctx.getChildCount() == 2:
            operator = ctx.getChild(0).getText()
            return UnaryOp(operator, self.visit(ctx.expr7()))
        return self.visit(ctx.expr8())

    # Visit a parse tree produced by HLangParser#expr8.
    # expr8   : (LR expr RR ) | expr9 ;
    def visitExpr8(self, ctx: HLangParser.Expr8Context):
        # print("----------Visiting expr8--------------")
        # debug_ctx(ctx, rule_name="visitExpr8", visitor=self)
        if ctx.getChildCount() == 3:  # Either LR expr RR or LS expr RS
            return self.visit(ctx.expr())
        return self.visit(ctx.expr9())

    # Visit a parse tree produced by HLangParser#expr9.
    # expr9   : IDENTIFIER | func_call  | literal | array_access;
    def visitExpr9(self, ctx: HLangParser.Expr9Context):
        # print("----------Visiting expr9--------------")
        # debug_ctx(ctx, rule_name="visitExpr9", visitor=self)
        if ctx.IDENTIFIER():
            return Identifier(ctx.IDENTIFIER().getText())
        elif ctx.func_call():
            return self.visit(ctx.func_call())
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.array_access():
            return self.visit(ctx.array_access())
        return None

def debug_ctx(ctx, rule_name=None, visitor=None):
    """
    In thông tin debug cho bất kỳ ParserRuleContext nào.

    Args:
        ctx         : ParserRuleContext từ ANTLR.
        rule_name   : Tên rule hiện tại (tự điền thủ công hoặc lấy từ class name).
        visitor     : Optional - truyền visitor hiện tại để tự động lấy rule_name nếu không có.
    """
    import inspect

    # Lấy tên rule từ tên hàm gọi nếu không truyền vào
    if rule_name is None:
        frame = inspect.currentframe().f_back
        rule_name = frame.f_code.co_name  # vd: visitExpr9

    print("\n\033[96m========== [Visiting {}] ==========\033[0m".format(rule_name))
    print(f"📜 Text       : {ctx.getText()}")
    print(f"🔍 Rule Type  : {type(ctx)}")

    # In từng child token/rule
    for i in range(ctx.getChildCount()):
        child = ctx.getChild(i)
        print(f"  Child[{i}]  : {child.getText():<20} ({type(child)})")

    # In các thành phần con có thể gọi được (IDENTIFIER(), expr(), etc.)
    print("\n🎯 Recognized Sub-rules:")
    for attr in dir(ctx):
        if callable(getattr(ctx, attr)) and not attr.startswith("__"):
            try:
                result = getattr(ctx, attr)()
                if result:
                    print(f"  {attr}() -> {result.getText()}")
            except:
                continue
    print("\033[96m========================================\033[0m\n")
