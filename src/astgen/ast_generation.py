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
    """
    Visitor class that converts ANTLR parse trees into AST nodes.
    """
    
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        """Visit the root program node."""
        const_decls = []
        func_decls = []
        
        for child in ctx.children:
            if child.getText() == '<EOF>':
                continue
            result = self.visit(child)
            if isinstance(result, ConstDecl):
                const_decls.append(result)
            elif isinstance(result, FuncDecl):
                func_decls.append(result)
        
        return Program(const_decls, func_decls)
    
    def visitConst_decl(self, ctx: HLangParser.Const_declContext):
        """Visit constant declaration."""
        name = ctx.ID().getText()
        type_annotation = None
        if ctx.type_spec():
            type_annotation = self.visit(ctx.type_spec())
        value = self.visit(ctx.expression())
        return ConstDecl(name, type_annotation, value)
    
    def visitFunc_decl(self, ctx: HLangParser.Func_declContext):
        """Visit function declaration."""
        name = ctx.ID().getText()
        params = []
        if ctx.parameter_list():
            params = self.visit(ctx.parameter_list())
        return_type = self.visit(ctx.return_type())
        body = []
        if ctx.statement():
            body = [self.visit(stmt) for stmt in ctx.statement()]
        return FuncDecl(name, params, return_type, body)
    
    def visitParameter_list(self, ctx: HLangParser.Parameter_listContext):
        """Visit parameter list."""
        return [self.visit(param) for param in ctx.parameter()]
    
    def visitParameter(self, ctx: HLangParser.ParameterContext):
        """Visit parameter."""
        name = ctx.ID().getText()
        param_type = self.visit(ctx.type_spec())
        return Param(name, param_type)
    
    def visitType_spec(self, ctx: HLangParser.Type_specContext):
        """Visit type specification."""
        if ctx.primitive_type():
            return self.visit(ctx.primitive_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
    
    def visitReturn_type(self, ctx: HLangParser.Return_typeContext):
        """Visit return type."""
        if ctx.primitive_type():
            return self.visit(ctx.primitive_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        elif ctx.VOID():
            return VoidType()
    
    def visitPrimitive_type(self, ctx: HLangParser.Primitive_typeContext):
        """Visit primitive type."""
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STRING():
            return StringType()
    
    def visitArray_type(self, ctx: HLangParser.Array_typeContext):
        """Visit array type."""
        element_type = self.visit(ctx.type_spec())
        size = int(ctx.INT_LIT().getText())
        return ArrayType(element_type, size)
    
    def visitVar_decl(self, ctx: HLangParser.Var_declContext):
        """Visit variable declaration."""
        name = ctx.ID().getText()
        value = self.visit(ctx.expression())
        # Lấy type annotation nếu có, ngược lại None
        type_annotation = self.visit(ctx.type_spec()) if ctx.type_spec() else None
        # Luôn gọi 3 tham số vào VarDecl(name, var_type, value)
        return VarDecl(name, type_annotation, value)
    
    def visitAssignment_stmt(self, ctx: HLangParser.Assignment_stmtContext):
        """Visit assignment statement."""
        lvalue = self.visit(ctx.lvalue())
        value = self.visit(ctx.expression())
        return Assignment(lvalue, value)
    
    def visitLvalue(self, ctx: HLangParser.LvalueContext):
        """Visit an lvalue expression (target of an assignment).
        """
        base = Identifier(ctx.ID().getText())
        
        # Handle array accesses
        if ctx.array_access():
            accesses = ctx.array_access()
            for access in accesses[:-1]:
                index = self.visit(access)
                base = ArrayAccess(base, index)
            last_index = self.visit(accesses[-1])
            return ArrayAccessLValue(base, last_index)
        
        return IdLValue(ctx.ID().getText())
    
    def visitIf_stmt(self, ctx: HLangParser.If_stmtContext):
        """Visit if / else if / else statement."""
        expr_nodes   = [self.visit(e) for e in ctx.expression()]
        block_nodes  = [self.visit(b) for b in ctx.block_stmt()]

        condition = expr_nodes[0]
        then_stmt = block_nodes[0]

        elif_branches = []
        for cond, blk in zip(expr_nodes[1:], block_nodes[1:1 + (len(expr_nodes)-1)]):
            elif_branches.append((cond, blk))

        else_stmt = None
        if len(block_nodes) > len(expr_nodes):
            else_stmt = block_nodes[-1]

        return IfStmt(condition, then_stmt, elif_branches, else_stmt)
    
    def visitWhile_stmt(self, ctx: HLangParser.While_stmtContext):
        """Visit while statement."""
        condition = self.visit(ctx.expression())
        body = self.visit(ctx.block_stmt())
        return WhileStmt(condition, body)
    
    def visitFor_stmt(self, ctx: HLangParser.For_stmtContext):
        """Visit for statement."""
        variable = ctx.ID().getText()
        iterable = self.visit(ctx.expression())
        body = self.visit(ctx.block_stmt())
        return ForStmt(variable, iterable, body)
    
    def visitReturn_stmt(self, ctx: HLangParser.Return_stmtContext):
        """Visit return statement."""
        value = None
        if ctx.expression():
            expr_ctx = ctx.expression()
            value = self.visit(expr_ctx)
        return ReturnStmt(value)
    
    def visitBreak_stmt(self, ctx: HLangParser.Break_stmtContext):
        """Visit break statement."""
        return BreakStmt()
    
    def visitContinue_stmt(self, ctx: HLangParser.Continue_stmtContext):
        """Visit continue statement."""
        return ContinueStmt()
    
    def visitExpression_stmt(self, ctx: HLangParser.Expression_stmtContext):
        """Visit expression statement."""
        expr = self.visit(ctx.expression())
        return ExprStmt(expr)
    
    def visitBlock_stmt(self, ctx: HLangParser.Block_stmtContext):
        """Visit block statement."""
        statements = []
        if ctx.statement():
            statements = [self.visit(stmt) for stmt in ctx.statement()]
        return BlockStmt(statements)
    
    def visitExpression(self, ctx: HLangParser.ExpressionContext):
        """Visit expression."""
        return self.visit(ctx.pipeline_expr())
    
    def visitPipeline_expr(self, ctx: HLangParser.Pipeline_exprContext):
        """Visit pipeline expression."""
        if len(ctx.logical_or_expr()) == 1:
            return self.visit(ctx.logical_or_expr(0))
        else:
            left = self.visit(ctx.logical_or_expr(0))
            for i in range(1, len(ctx.logical_or_expr())):
                right = self.visit(ctx.logical_or_expr(i))
                left = BinaryOp(left, '>>', right)
            return left
    
    def visitLogical_or_expr(self, ctx: HLangParser.Logical_or_exprContext):
        """Visit logical OR expression."""
        if len(ctx.logical_and_expr()) == 1:
            return self.visit(ctx.logical_and_expr(0))
        else:
            left = self.visit(ctx.logical_and_expr(0))
            for i in range(1, len(ctx.logical_and_expr())):
                right = self.visit(ctx.logical_and_expr(i))
                left = BinaryOp(left, '||', right)
            return left
    
    def visitLogical_and_expr(self, ctx: HLangParser.Logical_and_exprContext):
        """Visit logical AND expression."""
        if len(ctx.equality_expr()) == 1:
            return self.visit(ctx.equality_expr(0))
        else:
            left = self.visit(ctx.equality_expr(0))
            for i in range(1, len(ctx.equality_expr())):
                right = self.visit(ctx.equality_expr(i))
                left = BinaryOp(left, '&&', right)
            return left
    
    def visitEquality_expr(self, ctx: HLangParser.Equality_exprContext):
        """Visit equality expression, left‑associative chaining of ==, !=."""
        if len(ctx.relational_expr()) == 1:
            return self.visit(ctx.relational_expr(0))

        left = self.visit(ctx.relational_expr(0))

        for i in range(len(ctx.relational_expr()) - 1):
            right = self.visit(ctx.relational_expr(i + 1))

            if ctx.EQUAL(i):
                op = '=='
            else:
                op = '!='

            left = BinaryOp(left, op, right)

        return left
    
    def visitRelational_expr(self, ctx: HLangParser.Relational_exprContext):
        """Visit relational expression, left‑associative chaining of <, <=, >, >=."""
        if len(ctx.additive_expr()) == 1:
            return self.visit(ctx.additive_expr(0))

        result = self.visit(ctx.additive_expr(0))

        ops = []
        for i in range(len(ctx.children)):
            child = ctx.children[i]
            if child.getChildCount() == 0:
                text = child.getText()
                if text in ['<', '<=', '>', '>=']:
                    ops.append(text)

        for i in range(len(ops)):
            right = self.visit(ctx.additive_expr(i + 1))
            result = BinaryOp(result, ops[i], right)

        return result
    
    def visitAdditive_expr(self, ctx: HLangParser.Additive_exprContext):
        """Visit additive expression."""
        if len(ctx.multiplicative_expr()) == 1:
            return self.visit(ctx.multiplicative_expr(0))

        result = self.visit(ctx.multiplicative_expr(0))

        ops = []
        for i in range(len(ctx.children)):
            child = ctx.children[i]
            if child.getChildCount() == 0:
                text = child.getText()
                if text in ['+', '-']:
                    ops.append(text)

        for i in range(len(ops)):
            right = self.visit(ctx.multiplicative_expr(i + 1))
            result = BinaryOp(result, ops[i], right)

        return result
    
    def visitMultiplicative_expr(self, ctx: HLangParser.Multiplicative_exprContext):
        """Visit multiplicative expression."""
        if len(ctx.unary_expr()) == 1:
            return self.visit(ctx.unary_expr(0))

        result = self.visit(ctx.unary_expr(0))

        ops = []
        for i in range(len(ctx.children)):
            child = ctx.children[i]
            if child.getChildCount() == 0:
                text = child.getText()
                if text in ['*', '/', '%']:
                    ops.append(text)
            
        for i in range(len(ops)):
            right = self.visit(ctx.unary_expr(i + 1))
            result = BinaryOp(result, ops[i], right)
        return result
    
    def visitUnary_expr(self, ctx: HLangParser.Unary_exprContext):
        """Visit unary expression."""
        if ctx.postfix_expr():
            return self.visit(ctx.postfix_expr())
        else:
            if ctx.NOT():
                op = '!'
            elif ctx.SUB():
                op = '-'
            else:
                op = '+'
            operand = self.visit(ctx.unary_expr())
            return UnaryOp(op, operand)
    
    def visitPostfix_expr(self, ctx: HLangParser.Postfix_exprContext):
        """Visit postfix expression."""
        if ctx.type_keyword_func():
            base = self.visit(ctx.type_keyword_func())
        elif ctx.ID():
            base = Identifier(ctx.ID().getText())
            if ctx.LRB():
                args = self.visit(ctx.argument_list()) if ctx.argument_list() else []
                base = FunctionCall(base, args)
        elif ctx.literal():
            base = self.visit(ctx.literal())
        else:
            base = self.visit(ctx.expression())

        if ctx.array_access():
            for access in ctx.array_access():
                index = self.visit(access)
                base = ArrayAccess(base, index)

        return base
    
    def visitType_keyword_func(self, ctx: HLangParser.Type_keyword_funcContext):
        """Visit type keyword function call."""
        func_name = ctx.type_keyword().getText()
        args = []
        if ctx.argument_list():
            args = self.visit(ctx.argument_list())
        return FunctionCall(Identifier(func_name), args)
    
    def visitArgument_list(self, ctx: HLangParser.Argument_listContext):
        """Visit argument list."""
        args = []
        if ctx.expression():
            for expr in ctx.expression():
                args.append(self.visit(expr))
        return args
    
    def visitArray_access(self, ctx: HLangParser.Array_accessContext):
        """Visit array access expression."""
        return self.visit(ctx.expression())
    
    def visitLiteral(self, ctx: HLangParser.LiteralContext):
        """Visit literal."""
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.bool_literal():
            return self.visit(ctx.bool_literal())
        elif ctx.STR_LIT():
            return StringLiteral(ctx.STR_LIT().getText())
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())
    
    def visitBool_literal(self, ctx: HLangParser.Bool_literalContext):
        """Visit boolean literal."""
        return BooleanLiteral(ctx.getText() == 'true')
    
    def visitArray_literal(self, ctx: HLangParser.Array_literalContext):
        """Visit array literal."""
        elements = []
        if ctx.expression():
            elements = [self.visit(expr) for expr in ctx.expression()]
        return ArrayLiteral(elements)