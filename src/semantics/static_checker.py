"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral, Type
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)

# Import marker classes with different names to avoid conflict  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__()
        self.param_types = param_types
        self.return_type = return_type

    def accept(self, visitor):
        return visitor.visit_function_type(self)

    def __str__(self):
        params_str = ', '.join(str(t) for t in self.param_types) if self.param_types else ""
        params_part = f"({params_str})" if params_str else "()"
        return f"FunctionType{params_part} -> {self.return_type}"
    
class SymbolEntry:
    """
    Represents a named entity in the program with associated type information.
    Typically used for variables, constants, and function declarations.
    """

    def __init__(self, name: str, typ: 'Type', is_const: bool = False):
        self.name = name  
        self.typ = typ    
        self.is_const = is_const

    def __str__(self):
        return f"SymbolEntry(name={self.name}, type={self.typ}), is_const={self.is_const})"
    
    @staticmethod
    def str(params: List[List['SymbolEntry']]) -> str:
        if not params:
            return "[]"

        result = "[\n"
        for i, scope in enumerate(params):
            result += f"  Scope {i}:\n"
            for sym in scope:
                result += f"    {str(sym)}\n"
        result += "]"
        return result
    
class StaticChecker(ASTVisitor):
    """
    Redeclared - Variables, constants, functions, or parameters declared multiple times in the same scope

    Undeclared - Use of identifiers or functions that have not been declared

    MustInLoop - Break/continue statements outside of loop contexts

    NoEntryPoint - Missing or invalid main function
    """
    def __init__(self):
        self.number_loop = 0
        self.main_func_declared_valid = False
        self.current_function_type = None 
        self.parent_node = None  
        self.operator_pipe = False

    def lookup(self, name: str, lst: List, func):
        """
        Find and return the first element in the list for which the given function
        returns a value equal to `name`.

        Args:
            name (str): The value to match.
            lst (List): A list of elements to search.
            func (Callable): A function that extracts a comparable value from each element.

        Returns:
            Any: The first element `x` in `lst` such that `func(x) == name`, or `None` if not found.
        """
        for x in lst:
            if name == func(x):
                return x
        return None

    def visit(self, node: 'ASTNode', param):
        return node.accept(self, param)

    def check_program(self, node: 'ASTNode'):
        self.visit(node, [])
        if not self.main_func_declared_valid:
            raise NoEntryPoint()

    def visit_program(self, node: 'Program', param):
        # const_decls
        builtins = [
            SymbolEntry("print", FunctionType([StringType()], VoidType())),
            SymbolEntry("input", FunctionType([], StringType())),
            SymbolEntry("str", FunctionType([IntType()], StringType())),
            SymbolEntry("str", FunctionType([FloatType()], StringType())),
            SymbolEntry("str", FunctionType([BoolType()], StringType())),
            SymbolEntry("int", FunctionType([StringType()], IntType())),
            SymbolEntry("float", FunctionType([StringType()], FloatType())),
        ]
        global_scope = [builtins]
        print( str(node))
        reduce(
            lambda acc, ele: [([self.visit(ele, acc)] + acc[0])] + acc[1:], 
            node.const_decls + node.func_decls, 
            global_scope,
        ) 

    def visit_const_decl(self, node: 'ConstDecl', param: List[List['SymbolEntry']]) -> SymbolEntry:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared("Constant", node.name)
        type_ = self.visit(node.value, param)
        if not node.type_annotation and isinstance(type_, VoidType):
            raise TypeCannotBeInferred(node)
        if node.type_annotation and not self.is_compatible(node.type_annotation, type_):
            raise TypeMismatchInStatement(node)
        
        return SymbolEntry(node.name, type_, is_const=True)
    #! Function declared but not accessible
    def visit_func_decl(self, node: 'FuncDecl', param: List[List['SymbolEntry']]):
        self.debug_visit_context(node, param)

        symbol = self.lookup(node.name, param[0], lambda x: x.name)
        if symbol:
            raise Redeclared("Function", node.name)
        if node.name == "main" :
            if not node.params and isinstance(node.return_type, VoidType):
                self.main_func_declared_valid = True
            else: 
                raise NoEntryPoint()
        if node.return_type is None:
            raise TypeCannotBeInferred(node)
        init_scope = [[]] + param
        # Check parameters
        param_result = reduce(
            lambda acc, param : [acc[0] + [self.visit(param, acc)]] + acc[1:], node.params, init_scope
        )
      
        param_types = [symbol.typ for symbol in param_result[0]]
        print(f"Function {node.name} declared with parameters: {param_types}")
        func_type = FunctionType(param_types, node.return_type)
        param_result[0].insert(0, SymbolEntry(node.name, func_type)) # Insert function symbol at the beginning of the scope
        self.current_function_type = node.return_type
        reduce(
            lambda acc, stmt: [
                ([result] + acc[0]) if isinstance(result := self.visit(stmt, acc), SymbolEntry) else acc[0]
            ] + acc[1:],
            node.body,
            param_result
        )
        return SymbolEntry(node.name, func_type)
    
    def visit_param(self, node: 'Param', param: List['SymbolEntry']) -> SymbolEntry:
        # self.debug_visit_context(node, param)
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared("Parameter", node.name)
        if node.param_type is None:
            raise TypeCannotBeInferred(node)
        return SymbolEntry(node.name, node.param_type, is_const = True)
    
    # Statements
    def visit_var_decl(self, node: 'VarDecl', param: List[List['SymbolEntry']]) -> SymbolEntry:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared("Variable", node.name)
        type_ = self.visit(node.value, param)
        if not node.type_annotation and isinstance(type_, VoidType):
            raise TypeCannotBeInferred(node)
        print(f"Type annotation: {node.type_annotation}, Type: {type_}")
        if node.type_annotation and not self.is_compatible(node.type_annotation, type_):
            raise TypeMismatchInStatement(node)
        
        return SymbolEntry(node.name, type_)
    
    
    # While loops: Condition must be bool type
    def visit_while_stmt(self, node: 'WhileStmt', param: List[List['SymbolEntry']]):
        self.number_loop += 1
        cond_type = self.visit(node.condition, param)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(node)
        
        self.visit(node.body, param)
        self.number_loop -= 1
    
    # For loops: Collection must be array type, loop variable automatically typed
    def visit_for_stmt(self, node: 'ForStmt', param: List[List['SymbolEntry']]):
        iterable_type = self.visit(node.iterable, param)
        if not isinstance(iterable_type, ArrayType):
            raise TypeMismatchInStatement(node)
        self.number_loop += 1  

        iterable_type = self.visit(node.iterable, param)
        if not isinstance(iterable_type, ArrayType):
            raise TypeMismatchInStatement(node)

        loop_var = SymbolEntry(node.variable, iterable_type.element_type)
        new_scope = [[loop_var]] + param

        self.parent_node = node
        self.visit(node.body, new_scope)
        self.number_loop -= 1  
        self.parent_node = None

    def visit_break_stmt(self, node: 'BreakStmt', param: List[List['SymbolEntry']]):
        if self.number_loop == 0:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: 'ContinueStmt', param: List[List['SymbolEntry']]):
        if self.number_loop == 0: 
            raise MustInLoop(node)
    
    #! Check if type of lvalue is constant 
    def visit_assignment(self, node: 'Assignment', param: List[List['SymbolEntry']]):
        # self.debug_visit_context(node, param)
        self.parent_node = node 
        lvalue = self.visit(node.lvalue, param)
        rvalue = self.visit(node.value, param)
        self.parent_node = None  
        # if isinstance(node.lvalue, IdLValue):
        #     found_symbol = next((self.lookup(node.lvalue.name, scope, lambda x: x.name)
        #             for scope in param if self.lookup(node.lvalue.name, scope, lambda x: x.name)),
        #         None)
        #     if found_symbol and found_symbol.is_const: 
        #         raise TypeMismatchInStatement(node)
        # if isinstance(node.lvalue, ArrayAccessLValue): #! Check if lvalue is ArrayAccessLValue
        #     print( f"visit aclvalue: {lvalue}, rvalue: {rvalue}")
        #     print( f"lvalue type: {node.lvalue.array}, rvalue type: {type(rvalue)}")
        #     found_symbol = next((self.lookup(node.lvalue.array.name, scope, lambda x: x.name)
        #         for scope in param if self.lookup(node.lvalue.array.name, scope, lambda x: x.name)),
        #     None)
        #     if found_symbol and found_symbol.is_const: 
        #         raise TypeMismatchInStatement(node)
        #     if not self.is_compatible(lvalue, rvalue):
        #         raise TypeMismatchInStatement(node)
        #     return lvalue
        if not self.is_compatible(lvalue, rvalue):
            raise TypeMismatchInStatement(node)

    def visit_block_stmt(self, node: 'BlockStmt', param: List[List['SymbolEntry']]):
        new_scope = [[]] + param
        if isinstance(self.parent_node, ForStmt): new_scope = param
        reduce(lambda acc, stmt: [
            [self.visit(stmt, acc)] + acc[0] if isinstance(self.visit(stmt, acc), SymbolEntry) else acc[0]
        ] + acc[1:], node.statements,  new_scope)
    
    def visit_id_lvalue(self, node: 'IdLValue', param: List[List['SymbolEntry']]):
        found_symbol = next((self.lookup(node.name, scope, lambda x: x.name)
                        for scope in param if self.lookup(node.name, scope, lambda x: x.name)),
                    None)
        if found_symbol:
            if found_symbol.is_const and isinstance(self.parent_node, Assignment):
                raise TypeMismatchInStatement(self.parent_node)
            return found_symbol.typ
        else:
            raise Undeclared(IdentifierMarker(), node.name)
    
    def visit_identifier(self, node: 'Identifier', param: List[List['SymbolEntry']]):
        found_symbol = next((self.lookup(node.name, scope, lambda x: x.name)
                        for scope in param if self.lookup(node.name, scope, lambda x: x.name)),
                    None)
        if found_symbol :
            if isinstance(found_symbol.typ, FunctionType): raise Undeclared(IdentifierMarker(), node.name)
            if found_symbol.is_const and isinstance(self.parent_node, Assignment):
                raise TypeMismatchInStatement(self.parent_node)
            return found_symbol.typ
        else:
            raise Undeclared(IdentifierMarker(), node.name)
    #! Valid: globalFunc declared later but in global scope
    #! TypeMismatchInStatement(<statement>) or TypeMismatchInExpression(<expression>)???
    def visit_function_call(self, node: 'FunctionCall', param: List[List['SymbolEntry']]):
        self.debug_visit_context(node, param)

        if isinstance(node.function, Identifier):
            func_name = node.function.name
            arg_types = list(map(lambda arg: self.visit(arg, param), node.args))

            candidate_symbols = [
                sym
                for scope in param
                for sym in scope
                if sym.name == func_name and isinstance(sym.typ, FunctionType)
            ]

            if not candidate_symbols:
                raise Undeclared(FunctionMarker(), func_name)
            matching_symbol = next(
                (
                    sym for sym in candidate_symbols
                    if len(sym.typ.param_types) == len(arg_types)
                    and all(self.is_compatible(p, a) for p, a in zip(sym.typ.param_types, arg_types))
                ),
                None
            )
            if not matching_symbol:
                raise TypeMismatchInStatement(self.parent_node) if isinstance(self.parent_node, ExprStmt) else TypeMismatchInExpression(node)   
            if not isinstance(self.parent_node, ExprStmt) and isinstance(matching_symbol.typ.return_type, VoidType):
                raise TypeMismatchInExpression(node)
            return matching_symbol.typ.return_type

        raise TypeMismatchInStatement(self.parent_node) if isinstance(self.parent_node, ExprStmt) else TypeMismatchInExpression(node)   




    # TASK 2 BTL3

    def visit_if_stmt(self, node: 'IfStmt', param: List[List['SymbolEntry']]): 
        cond_type = self.visit(node.condition, param)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(node)

        # Visit then block
        self.visit(node.then_stmt, [[]] + param)

        # Check elif branches
        list(map(
            lambda branch: (
                self._check_elif_condition(branch[0], param, node),
                self.visit(branch[1], param)
            ),
            node.elif_branches
        ))
        # Visit else block if it exists
        if node.else_stmt:
            self.visit(node.else_stmt, [[]] + param)
    def _check_elif_condition(self, cond: 'Expr', param: List[List['SymbolEntry']], node: 'IfStmt'):
        cond_type = self.visit(cond, param)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(node)
    def visit_return_stmt(self, node: 'ReturnStmt', param: List[List['SymbolEntry']]): 
        if not self.current_function_type:
            raise TypeMismatchInStatement(node)
        # self.debug_visit_context(node, param)
        if node.value :            
            actual_type = self.visit(node.value, param)
            if not self.is_compatible(self.current_function_type, actual_type):
                raise TypeMismatchInStatement(node)
        else:
            if not isinstance(self.current_function_type, VoidType):
                raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: 'ExprStmt', param: List[List['SymbolEntry']]):
        self.parent_node = node
        expr_type = self.visit(node.expr, param)
        self.parent_node = None
        print(f"Expr type: {type(expr_type)}, Expr: {node.expr}")
        # if isinstance(node.expr, FunctionCall):
        #     if not isinstance(expr_type.return_type, VoidType):
        #         raise TypeMismatchInStatement(node)
        if not isinstance(expr_type, VoidType):
            raise TypeMismatchInStatement(node)

    def visit_binary_op(self, node: 'BinaryOp', param: List[List['SymbolEntry']]): 
        self.debug_visit_context(node, param)
        op = node.operator
        if op == '>>':
            # self.operator_pipe = True
            # left_type = self.visit(node.left, param)
            # right_type = self.visit(node.right, param)#! Nếu là ID -> Trả về FunctionType, Nếu là FunctionCall thì trả về return_type
            # if not isinstance(right_type, FunctionType):
            #     raise TypeMismatchInExpression(node)
            
            
            # param_types = right_type.param_types
            # return_type = right_type.return_type
            # if not param_types:
            #     raise TypeMismatchInExpression(node)  
            

            # print("left_type:", type(left_type), "right_type:", type(param_types[0]))
            # if type(left_type) != type(param_types[0]):
            #     raise TypeMismatchInExpression(node)
            # self.operator_pipe = False
            # return return_type
            left_type = self.visit(node.left, param)
            if isinstance(node.right, Identifier):
                func_name = node.right.name
                arg_types = [left_type]

                candidate_symbols = [
                    sym
                    for scope in param
                    for sym in scope
                    if sym.name == func_name and isinstance(sym.typ, FunctionType)
                ]

                if not candidate_symbols:
                    raise Undeclared(FunctionMarker(), func_name)
            
                matching_symbol = next(
                    (
                        sym for sym in candidate_symbols
                        if len(sym.typ.param_types) == len(arg_types)
                        and all(self.is_compatible(p, a) for p, a in zip(sym.typ.param_types, arg_types))
                    ),
                    None
                )
                if not matching_symbol:
                    raise TypeMismatchInStatement(self.parent_node) if isinstance(self.parent_node, ExprStmt) else TypeMismatchInExpression(node) 
                if not isinstance(self.parent_node, ExprStmt) and isinstance(matching_symbol.typ.return_type, VoidType):
                    raise TypeMismatchInExpression(node)
                return matching_symbol.typ.return_type  
            elif isinstance(node.right, FunctionCall):
                func_name = node.right.function.name
                arg_types = [left_type] + list(map(lambda arg: self.visit(arg, param), node.right.args))

                candidate_symbols = [
                    sym
                    for scope in param
                    for sym in scope
                    if sym.name == func_name and isinstance(sym.typ, FunctionType)
                ]

                if not candidate_symbols:
                    raise Undeclared(FunctionMarker(), func_name)
            
                matching_symbol = next(
                    (
                        sym for sym in candidate_symbols
                        if len(sym.typ.param_types) == len(arg_types)
                        and all(self.is_compatible(p, a) for p, a in zip(sym.typ.param_types, arg_types))
                    ),
                    None
                )
                if not matching_symbol:
                    raise TypeMismatchInStatement(self.parent_node) if isinstance(self.parent_node, ExprStmt) else TypeMismatchInExpression(node) 
                if not isinstance(self.parent_node, ExprStmt) and isinstance(matching_symbol.typ.return_type, VoidType):
                    raise TypeMismatchInExpression(node)  
                return matching_symbol.typ.return_type
            else:
                raise TypeMismatchInExpression(node)

        left_type = self.visit(node.left, param)
        right_type = self.visit(node.right, param)
            
        if op in ['+', '-', '*', '/', '%']:
            if op == '+' and isinstance(left_type, StringType) and isinstance(right_type, StringType):
                return StringType()
            if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                if op == '%':
                    if isinstance(left_type, IntType) and isinstance(right_type, IntType):
                        return IntType()
                    else:
                        raise TypeMismatchInExpression(node)

                if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                    return FloatType()
                return IntType()
            raise TypeMismatchInExpression(node)

        if op in ['<', '<=', '>', '>=']:
            if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                return BoolType()
            # if isinstance(left_type, StringType) and isinstance(right_type, StringType):
            #     return BoolType()
            raise TypeMismatchInExpression(node)
        if op in ['==', '!=']:
            if type(left_type) == type(right_type):  
                return BoolType()
            raise TypeMismatchInExpression(node)
        if op in ['&&', '||']:
            if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
                return BoolType()
            raise TypeMismatchInExpression(node)

        raise TypeMismatchInExpression(node)
    def visit_unary_op(self, node: 'UnaryOp', param: List[List['SymbolEntry']]): 
        operand_type = self.visit(node.operand, param)

        if node.operator == '-':
            if isinstance(operand_type, (IntType, FloatType)):
                return operand_type
            else:
                raise TypeMismatchInExpression(node)

        elif node.operator == '+':
            if isinstance(operand_type, (IntType, FloatType)):
                return operand_type
            else:
                raise TypeMismatchInExpression(node)

        elif node.operator == '!':
            if isinstance(operand_type, BoolType):
                return BoolType()
            else:
                raise TypeMismatchInExpression(node)
    def visit_array_access(self, node: 'ArrayAccess', param: List[List['SymbolEntry']]): 
        array_type = self.visit(node.array, param)
        index_type = self.visit(node.index, param)

        if not isinstance(array_type, ArrayType):
            raise TypeMismatchInExpression(node)
        if not isinstance(index_type, IntType):
            raise TypeMismatchInExpression(node)
        return array_type.element_type

    def visit_array_literal(self, node: 'ArrayLiteral', param: List[List['SymbolEntry']]): 
        if not node.elements:
            raise TypeCannotBeInferred(node)
        
        elem_types = list(map(lambda elem: self.visit(elem, param), node.elements))
        first_type = elem_types[0]
        
        if any(not self.is_compatible(first_type, t) for t in elem_types[1:]):
            raise TypeMismatchInExpression(node)
        
        return ArrayType(first_type, len(node.elements))
    def visit_array_access_lvalue(self, node: 'ArrayAccessLValue', param: List[List['SymbolEntry']]):
        array_type = self.visit(node.array, param)
        if not isinstance(array_type, ArrayType):
            raise TypeMismatchInExpression(node)
        
        index_type = self.visit(node.index, param)
        if not isinstance(index_type, IntType):
            raise TypeMismatchInExpression(node)
        
        return array_type.element_type
    

    def visit_int_type(self, node: 'IntType', param): return node
    def visit_float_type(self, node: 'FloatType', param): return node
    def visit_bool_type(self, node: 'BoolType', param): return node
    def visit_string_type(self, node: 'StringType', param): return node
    def visit_void_type(self, node: 'VoidType', param): return node
    def visit_array_type(self, node: 'ArrayType', param): return node
    def visit_integer_literal(self, node: 'IntegerLiteral', param): return IntType()
    def visit_float_literal(self, node: 'FloatLiteral', param): return FloatType()
    def visit_boolean_literal(self, node: 'BooleanLiteral', param): return BoolType()
    def visit_string_literal(self, node: 'StringLiteral', param): return StringType()

    # func support
    def is_compatible(self, expected: Type, actual: Type) -> bool:
        if type(expected) != type(actual):
            # if isinstance(expected, FloatType) and isinstance(actual, IntType):
            #     return True
            return False
        
        if isinstance(expected, ArrayType):
            if not isinstance(actual, ArrayType):
                return False
            return (expected.size == actual.size and #? check size compatibility
                    self.is_compatible(expected.element_type, actual.element_type))
        
        return True
        
    def debug_visit_context(self, node: ASTNode, param: List[List['SymbolEntry']]):
        print("=== DEBUG VISIT CONTEXT ===")
        print(f"Visiting node type: {type(node).__name__}")
        print(f"Node content: {str(node)}\n")

        print("SymbolEntry table (scopes):")
        print(SymbolEntry.str(param))
        print("===========================\n")
