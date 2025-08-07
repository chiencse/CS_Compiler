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
            ] + o.sym,
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

    def visit_int_type(self, node: "IntType", o: Any = None):
        return "", IntType()

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return "", FloatType()

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        return "", BoolType()

    def visit_string_type(self, node: "StringType", o: Any = None):
        return "", StringType()

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return "", VoidType()

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        return "", node

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        typ = node.type_annotation
        code, inferred_typ = self.visit(node.value, Access(o.frame, o.sym))
        
        if typ is None:
            typ = inferred_typ
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                typ,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_write_var(node.name, typ, idx, o.frame))
        print(f"Writing variable {node.name} of type {typ} at index {idx}")
        return SubBody(
            o.frame,
            [Symbol(node.name, typ, Index(idx))] + o.sym,
        )

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        if type(node.lvalue) is ArrayAccessLValue:
            arr_code, arr_type = self.visit(node.lvalue.array, o)
            idx_code, idx_type = self.visit(node.lvalue.index, o)
            val_code, val_type = self.visit(node.value, o)
            if not isinstance(val_type, type(arr_type.element_type)):
                raise IllegalOperandException("Type mismatch in array assignment")
            self.emit.print_out(arr_code)
            self.emit.print_out(idx_code)
            self.emit.print_out(val_code)
            self.emit.print_out(self.emit.emit_astore(arr_type.element_type, o.frame))
        else:
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
            self.emit.print_out(rc)
            self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        frame = o.frame
        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        if not isinstance(cond_type, BoolType):
            raise IllegalOperandException("If condition must be boolean")
        self.emit.print_out(cond_code)

        false_label = frame.get_new_label()
        end_label = frame.get_new_label() if node.elif_branches or node.else_stmt else None

        self.emit.print_out(self.emit.emit_if_false(false_label, frame))
        self.visit(node.then_stmt, o)

        if node.elif_branches or node.else_stmt:
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(false_label, frame))

        for cond, block in node.elif_branches:
            cond_code, cond_type = self.visit(cond, Access(frame, o.sym))
            if not isinstance(cond_type, BoolType):
                raise IllegalOperandException("Else if condition must be boolean")
            self.emit.print_out(cond_code)
            false_label = frame.get_new_label()
            self.emit.print_out(self.emit.emit_if_false(false_label, frame))
            self.visit(block, o)
            self.emit.print_out(self.emit.emit_goto(end_label, frame))
            self.emit.print_out(self.emit.emit_label(false_label, frame))

        if node.else_stmt:
            self.visit(node.else_stmt, o)

        if end_label:
            self.emit.print_out(self.emit.emit_label(end_label, frame))

        return o

    def visit_while_stmt(self, node: "WhileStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()

        break_label = frame.get_break_label()
        continue_label = frame.get_continue_label()

        self.emit.print_out(self.emit.emit_label(continue_label, frame))

        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        if not isinstance(cond_type, BoolType):
            raise IllegalOperandException("While condition must be boolean")

        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(break_label, frame))

        self.visit(node.body, o)

        self.emit.print_out(self.emit.emit_goto(continue_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))

        frame.exit_loop()

        return o


    def visit_for_stmt(self, node: "ForStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()  # Push continue and break labels
        start_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        end_label = frame.get_break_label()
        # Initialize loop variable for index
        idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx, "_idx", IntType(), frame.get_start_label(), frame.get_end_label()
            )
        )
        self.emit.print_out(self.emit.emit_push_iconst(0, frame))
        self.emit.print_out(self.emit.emit_write_var("_idx", IntType(), idx, frame))

        # Get array length
        arr_code, arr_type = self.visit(node.iterable, o)
        if not isinstance(arr_type, ArrayType):
            raise IllegalOperandException("For loop iterable must be an array")
        self.emit.print_out(arr_code)
        self.emit.print_out(self.emit.emit_arraylength(frame))
        len_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                len_idx, "_len", IntType(), frame.get_start_label(), frame.get_end_label()
            )
        )
        self.emit.print_out(self.emit.emit_write_var("_len", IntType(), len_idx, frame))

        # Loop start
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        # Condition: _idx < _len
        self.emit.print_out(self.emit.emit_read_var("_idx", IntType(), idx, frame))
        self.emit.print_out(self.emit.emit_read_var("_len", IntType(), len_idx, frame))
        self.emit.print_out(self.emit.emit_re_op("<", IntType(), frame))
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))

        # Body: access array element
        self.emit.print_out(arr_code)
        self.emit.print_out(self.emit.emit_read_var("_idx", IntType(), idx, frame))
        self.emit.print_out(self.emit.emit_aload(arr_type.element_type, frame))
        var_idx = frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                var_idx, node.variable, arr_type.element_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        self.emit.print_out(self.emit.emit_write_var(node.variable, arr_type.element_type, var_idx, frame))
        self.visit(node.body, SubBody(frame, [Symbol(node.variable, arr_type.element_type, Index(var_idx))] + o.sym))

        # Update: _idx++
        self.emit.print_out(self.emit.emit_label(continue_label, frame)) # Continue label
        self.emit.print_out(self.emit.emit_read_var("_idx", IntType(), idx, frame))
        self.emit.print_out(self.emit.emit_push_iconst(1, frame))
        self.emit.print_out(self.emit.emit_add_op("+", IntType(), frame))
        self.emit.print_out(self.emit.emit_write_var("_idx", IntType(), idx, frame))

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop() 

        return o
    def visit_return_stmt(self, node: "ReturnStmt", o: SubBody = None):
        if node.expr:
            code, typ = self.visit(node.expr, Access(o.frame, o.sym))
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_return(typ, o.frame))
        else:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not isinstance(typ, VoidType):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_scope(False)
        o = reduce(lambda acc, cur: self.visit(cur, acc), node.statements, o)
        frame.exit_scope()
        return o

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if not sym:
            raise IllegalOperandException(node.name)
        if type(sym.value) is Index:
            code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
        else:
            raise IllegalOperandException(node.name)
        return code, sym.type

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        arr_code, arr_type = self.visit(node.array, o)
        idx_code, idx_type = self.visit(node.index, o)
        return arr_code + idx_code, arr_type.element_type

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        frame = o.frame
        code_left, type_left = self.visit(node.left, o)
        code_right, type_right = self.visit(node.right, o)
        op = node.operator
        if op in ['||', '&&']:
            label1 = frame.get_new_label()
            label2 = frame.get_new_label()
            result = []

            # Visit left expression and get its code
            code_left, _ = self.visit(node.left, o)
            result.append(code_left)
            result.append(self.emit.emit_dup(frame))

            if op == '||':
                result.append(self.emit.emit_if_false(label1, frame))  # if false, need to evaluate right
                result.append(self.emit.emit_push_iconst(1, frame))    # short-circuit true
            else:  # '&&'
                result.append(self.emit.emit_if_true(label1, frame))   # if true, need to evaluate right
                result.append(self.emit.emit_push_iconst(0, frame))    # short-circuit false

            result.append(self.emit.emit_goto(label2, frame))          # skip right expr
            result.append(self.emit.emit_label(label1, frame))         # label: evaluate right
            code_right, _ = self.visit(node.right, o)
            result.append(code_right)
            result.append(self.emit.emit_label(label2, frame))

            if op == '||':
                result.append(self.emit.emit_or_op(frame))
            else:
                result.append(self.emit.emit_and_op(frame))

            return "".join(result), BoolType()

        if op == '+' and isinstance(type_left, StringType):
            if isinstance(type_right, IntType):
                node.right = FunctionCall(Identifier("int2str"), [node.right])
                code_right, _ = self.visit(node.right, o)
            else:
                code_right, _ = self.visit(node.right, o)
            return (
                code_left + code_right + 
                self.emit.emit_invoke_virtual(
                    "java/lang/String/concat",
                    FunctionType([StringType()], StringType()),
                    frame
                ),
                StringType()
            )

        if node.operator in ['+', '-'] and type(type_left) in [FloatType, IntType]:
            type_return = IntType() if type(type_left) is IntType and type(type_right) is IntType else FloatType()
            if type(type_return) is FloatType:
                if type(type_left) is IntType:
                    code_left += self.emit.emit_i2f(frame)
                if type(type_right) is IntType:
                    code_right += self.emit.emit_i2f(frame)
            return code_left + code_right + self.emit.emit_add_op(node.operator, type_return, frame), type_return

        if node.operator in ['*', '/']:
            type_return = IntType() if type(type_left) is IntType and type(type_right) is IntType else FloatType()
            if type(type_return) is FloatType:
                if type(type_left) is IntType:
                    code_left += self.emit.emit_i2f(frame)
                if type(type_right) is IntType:
                    code_right += self.emit.emit_i2f(frame)
            return code_left + code_right + self.emit.emit_mul_op(node.operator, type_return, frame), type_return

        if op in ['%']:
            if type(type_left) is not IntType or type(type_right) is not IntType:
                raise IllegalOperandException("Modulo operation requires integer operands")
            return code_left + code_right + self.emit.emit_mod(frame), IntType()

        if op in ['==', '!=', '<', '>', '>=', '<=']:
            type_return = BoolType()

            if isinstance(type_left, (IntType, FloatType, BoolType)):
                return (
                    code_left + code_right + 
                    self.emit.emit_re_op(node.operator, type_left, frame),
                    type_return
                )

            elif isinstance(type_left, StringType):
                compare_code = self.emit.emit_invoke_virtual(
                    "java/lang/String/compareTo",
                    FunctionType([StringType()], IntType()),
                    frame
                )
                comparison_value = self.emit.emit_push_iconst(0, frame)
                re_op_code = self.emit.emit_re_op(node.operator, IntType(), frame)
                return (
                    code_left + code_right + compare_code + comparison_value + re_op_code,
                    type_return
                )

        raise IllegalOperandException(node.operator)

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        code, type_return = self.visit(node.operand, o)
        if node.operator == '!':
            return code + self.emit.emit_not(type_return, o.frame), BoolType()
        return (code if node.operator == '+' else code + self.emit.emit_neg_op(type_return, o.frame)), type_return

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name

        function_symbol: Symbol = next(filter(lambda x: x.name == function_name, o.sym), None)
        if not function_symbol:
            raise IllegalOperandException(function_name)
        
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes.append(ac)
        
        return (
            "".join(argument_codes) +
            self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            function_symbol.type.return_type
        )

    def visit_array_access(self, node: "ArrayAccess", o: Access = None) -> tuple[str, Type]:
        code_arr, arr_type = self.visit(node.array, o)
        code_idx, idx_type = self.visit(node.index, o)
        code = code_arr + code_idx + self.emit.emit_aload(arr_type.element_type, o.frame)
        return code, arr_type.element_type

    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None) -> tuple[str, Type]:
        frame = o.frame
        if not node.elements:
            raise IllegalOperandException("Empty array literal")
        
        type_element_array = self.visit(node.elements[0], o)[1] # get type of first element
        code_gen = self.emit.emit_push_iconst(len(node.elements), frame) # create array with length
        if type(type_element_array) is IntType:
            code_gen += self.emit.emit_new_array("int")
        elif type(type_element_array) is FloatType:
            code_gen += self.emit.emit_new_array("float")
        elif isinstance(type_element_array, (ArrayType, StringType, ClassType)):
            code_gen += self.emit.emit_anew_array(type_element_array, frame)
        else:
            raise IllegalOperandException("Unsupported array element type")
        
        for idx, item in enumerate(node.elements):
            code_gen += self.emit.emit_dup(frame)
            code_gen += self.emit.emit_push_iconst(idx, frame)
            item_code, item_type = self.visit(item, o)
            code_gen += item_code
            code_gen += self.emit.emit_astore(type_element_array, frame)
        
        return code_gen, ArrayType(type_element_array, len(node.elements))

    def visit_identifier(self, node: "Identifier", o: Access = None) -> tuple[str, Type]:
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if not sym:
            raise IllegalOperandException(node.name)
        
        if type(sym.value) is Index:
            return self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame), sym.type
        elif type(sym.value) is CName:
            return self.emit.emit_get_static(sym.value.value + "/" + sym.name, sym.type, o.frame), sym.type
        raise IllegalOperandException(node.name)

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_iconst("true" if node.value else "false", o.frame), BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame), StringType()