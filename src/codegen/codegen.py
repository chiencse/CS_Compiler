"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.func_decls,
            SubBody(None, IO_SYMBOL_LIST),
        )

        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        pass

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, SubBody(frame, o.sym))
        param_types = list(map(lambda x: x.param_type, node.params))
        return SubBody(
            None,
            [
                Symbol(
                    node.name,
                    FunctionType(param_types, node.return_type),
                    CName(self.class_name),
                )
            ]
            + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system

    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        pass

    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        pass

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.type_annotation,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        if node.value is not None:
            self.visit(
                Assignment(IdLValue(node.name), node.value),
                SubBody(
                    o.frame,
                    [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
                ),
            )
        return SubBody(
            o.frame,
            [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
        )

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        rc, rt = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(rc)
        lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
        self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        pass

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        pass

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        pass

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        pass

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        pass

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        pass

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        pass

    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            False,
        )

        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )

        return code, sym.type

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Any = None):
        pass

    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        pass

    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        pass

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name
        function_symbol = next(filter(lambda x: x.name == function_name, o.sym), False)
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes += [ac]

        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            VoidType(),
        )

    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        pass

    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        pass

    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Any = None):
        pass

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return (
            self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame),
            StringType(),
        )
