from utils import ASTGenerator
from src.utils.nodes import Program, ConstDecl, BinaryOp, IntegerLiteral, UnaryOp, FunctionCall, Identifier, ArrayLiteral, Assignment, IdLValue, ArrayAccessLValue, FuncDecl, VoidType, ArrayAccess, IfStmt, BlockStmt, ReturnStmt
from src.utils.nodes import IntType, FloatType, BoolType, StringType, VoidType, ArrayType, VarDecl, Param, FloatLiteral, BooleanLiteral, StringLiteral


def test_001():
    """Test basic constant declaration AST generation"""
    source = "const x: int = 42;"
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected



def test_002():
    """Test function declaration AST generation"""
    source = "func main() -> void {}"
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test function with parameters AST generation"""
    source = "func add(a: int, b: int) -> int { return a + b; }"
    expected = "Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test multiple declarations AST generation"""
    source = """const PI: float = 3.14;
    func square(x: int) -> int { return x * x; }"""
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14))], funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """func main() -> void { 
        if (x > 0) { 
            return x;
        } else { 
            return 0;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(Identifier(x))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test while loop AST generation"""
    source = """func main() -> void { 
        while (i < 10) { 
            i = i + 1; 
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_008():
    """Test array operations AST generation"""
    source = """func main() -> void { 
        let arr = [1, 2, 3];
        let first = arr[0];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])), VarDecl(first, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test pipeline operator AST generation"""
    source = """func main() -> void { 
        let result = data >> process;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(data), >>, Identifier(process)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_013():
    source = """
        const a = 1 || 2;
        const a = 1 || 2 || 3;
        const a = 1 >> 2 || 3;
    """
    expected = Program([
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "||", IntegerLiteral(2))),
        ConstDecl("a", None, BinaryOp(BinaryOp(IntegerLiteral(1), "||", IntegerLiteral(2)), "||", IntegerLiteral(3))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), ">>", BinaryOp(IntegerLiteral(2), "||", IntegerLiteral(3))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_015():
    source = """
        const a = 1 == 2;
        const a = 1 == 2 != 3;
        const a = 1 && 2 == 3;
    """
    expected = Program([
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "==", IntegerLiteral(2))),
        ConstDecl("a", None, BinaryOp(BinaryOp(IntegerLiteral(1), "==", IntegerLiteral(2)), "!=", IntegerLiteral(3))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "&&", BinaryOp(IntegerLiteral(2), "==", IntegerLiteral(3))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_016():
    source = """
        const a = 1 > 2;
        const a = 1 > 2 < 3 >= 4 <= 5;
        const a = 1 == 2 >= 3;
    """
    expected = Program([
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), ">", IntegerLiteral(2))),
        ConstDecl("a", None, BinaryOp(BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), ">", IntegerLiteral(2)), "<", IntegerLiteral(3)), ">=", IntegerLiteral(4)), "<=", IntegerLiteral(5))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "==", BinaryOp(IntegerLiteral(2), ">=", IntegerLiteral(3))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_017():
    source = """
        const a = 1 + 2;
        const a = 1 - 2 + 3;
        const a = 1 > 2 + 3;
    """
    expected = Program([
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "+", IntegerLiteral(2))),
        ConstDecl("a", None, BinaryOp(BinaryOp(IntegerLiteral(1), "-", IntegerLiteral(2)), "+", IntegerLiteral(3))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), ">", BinaryOp(IntegerLiteral(2), "+", IntegerLiteral(3))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_018():
    source = """
        const a = 1 * 2;
        const a = 1 * 2 / 3 % 4;
        const a = 1 + 2 * 3;
    """
    expected = Program([
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "*", IntegerLiteral(2))),
        ConstDecl("a", None, BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), "*", IntegerLiteral(2)), "/", IntegerLiteral(3)), "%", IntegerLiteral(4))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "+", BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(3))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_019():
    source = """
        const a = -1;
        const a = -!+1;
        const a = 1 * -2;
    """
    expected = Program([
        ConstDecl("a", None, UnaryOp("-", IntegerLiteral(1))),
        ConstDecl("a", None, UnaryOp("-", UnaryOp("!", UnaryOp("+", IntegerLiteral(1))))),
        ConstDecl("a", None, BinaryOp(IntegerLiteral(1), "*", UnaryOp("-", IntegerLiteral(2))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_022():
    source = """
        const a = foo();
        const a = foo(1);
        const b = foo(1, [], foo());
    """
    expected = Program([
        ConstDecl("a", None, FunctionCall(Identifier("foo"), [])),
        ConstDecl("a", None, FunctionCall(Identifier("foo"), [IntegerLiteral(1)])),
        ConstDecl("b", None, FunctionCall(Identifier("foo"), [IntegerLiteral(1), ArrayLiteral([]), FunctionCall(Identifier("foo"), [])]))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_030():
    source = """
        func foo() -> void {
            a = 1;
            a[2] = foo() >> a[2];
            a[a[2]][1+2] = 1;
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [Assignment(IdLValue(a), IntegerLiteral(1)), Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(2)), BinaryOp(FunctionCall(Identifier(foo), []), >>, ArrayAccess(Identifier(a), IntegerLiteral(2)))), Assignment(ArrayAccessLValue(ArrayAccess(Identifier(a), ArrayAccess(Identifier(a), IntegerLiteral(2))), BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2))), IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_035():
    source = """
        func foo() -> void {
            if (1) {} else if(2) {} else if(3) {}
            if (1) {return;} else if(2) {return;} else if(3) {return;} else {return;}
        }
    """
    expected = Program([], [FuncDecl("foo", [], VoidType(), [
        IfStmt(IntegerLiteral(1),BlockStmt([]),[(IntegerLiteral(2), BlockStmt([])), (IntegerLiteral(3), BlockStmt([]))],None),
        IfStmt(IntegerLiteral(1),BlockStmt([ReturnStmt()]),[(IntegerLiteral(2), BlockStmt([ReturnStmt()])), (IntegerLiteral(3), BlockStmt([ReturnStmt()]))],BlockStmt([ReturnStmt()]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)
def test_036():
    """Test constant declaration with boolean literal"""
    source = "const flag: bool = true;"
    expected = "Program(consts=[ConstDecl(flag, bool, BooleanLiteral(True))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_037():
    """Test variable declaration with string literal"""
    source = "func main() -> int { let message: string = \"Hello\";}"
    expected = "Program(funcs=[FuncDecl(main, [], int, [VarDecl(message, string, StringLiteral('Hello'))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_038():
    """Test function declaration with empty body"""
    source = "func empty() -> void {};"
    expected = "Program(funcs=[FuncDecl(empty, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_039():
    """Test function with multiple variable declarations and assignments"""
    source = """func test() -> void {
        let x = 10;
        let y = x + 5;
        y = y * 2;
    };"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [VarDecl(x, IntegerLiteral(10)), VarDecl(y, BinaryOp(Identifier(x), +, IntegerLiteral(5))), Assignment(IdLValue(y), BinaryOp(Identifier(y), *, IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_040():
    """Test nested if statements"""
    source = """func main() -> void {
        if (x > 0) {
            if (y < 10) {
                x = x + 1;
            }
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([IfStmt(condition=BinaryOp(Identifier(y), <, IntegerLiteral(10)), then_stmt=BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_041():
    """Test for loop iterating over array"""
    source = """func main() -> void {
        for (i in arr) {
            sum = sum + i;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(arr), BlockStmt([Assignment(IdLValue(sum), BinaryOp(Identifier(sum), +, Identifier(i)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_042():
    """Test while loop with break statement"""
    source = """func main() -> void {
        while (true) {
            break;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BooleanLiteral(True), BlockStmt([BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_043():
    """Test for loop with continue statement"""
    source = """func main() -> void {
        for (x in arr) {
            continue;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(x, Identifier(arr), BlockStmt([ContinueStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_044():
    """Test constant declaration with array type"""
    source = "const arr: [int; 3] = [1, 2, 3];"
    expected = "Program(consts=[ConstDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_045():
    """Test assignment with function call"""
    source = """func main() -> void {
        let x = foo(5);
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, FunctionCall(Identifier(foo), [IntegerLiteral(5)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_046():
    """Test expression with mixed arithmetic and comparison operators"""
    source = "const result = x * 2 + 3 > 10;"
    expected = "Program(consts=[ConstDecl(result, BinaryOp(BinaryOp(BinaryOp(Identifier(x), *, IntegerLiteral(2)), +, IntegerLiteral(3)), >, IntegerLiteral(10)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_047():
    """Test multi-dimensional array access"""
    source = """func main() -> void {
        let x = arr[1][2];
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, ArrayAccess(ArrayAccess(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_048():
    """Test expression with logical AND and OR"""
    source = "const flag = true && false || true;"
    expected = "Program(consts=[ConstDecl(flag, BinaryOp(BinaryOp(BooleanLiteral(True), &&, BooleanLiteral(False)), ||, BooleanLiteral(True)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_049():
    """Test multiple unary operators"""
    source = "const x = -+!true;"
    expected = "Program(consts=[ConstDecl(x, UnaryOp(-, UnaryOp(+, UnaryOp(!, BooleanLiteral(True)))))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_050():
    """Test function with array parameter"""
    source = "func process(arr: [int; 5]) -> void {};"
    expected = "Program(funcs=[FuncDecl(process, [Param(arr, [int; 5])], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_051():
    """Test return statement with complex expression"""
    source = """func calc() -> int {
        return x * 2 + y;
    };"""
    expected = "Program(funcs=[FuncDecl(calc, [], int, [ReturnStmt(BinaryOp(BinaryOp(Identifier(x), *, IntegerLiteral(2)), +, Identifier(y)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_052():
    """Test variable declaration with empty array literal"""
    source = "const arr = [];"
    expected = "Program(consts=[ConstDecl(arr, ArrayLiteral([]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_053():
    """Test function call with array literal as argument"""
    source = """func main() -> void {
        foo([1, 2, 3]);
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(foo), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_054():
    """Test nested block statements"""
    source = """func main() -> void {
        { { x = 1; } }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [BlockStmt([BlockStmt([Assignment(IdLValue(x), IntegerLiteral(1))])])])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_055():
    """Test chained comparison operators"""
    source = "const result = 1 < 2 <= 3;"
    expected = "Program(consts=[ConstDecl(result, BinaryOp(BinaryOp(IntegerLiteral(1), <, IntegerLiteral(2)), <=, IntegerLiteral(3)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_056():
    """Test modulo operator in expression"""
    source = "const x = 10 % 3;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(IntegerLiteral(10), %, IntegerLiteral(3)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_057():
    """Test function with mixed-type parameters"""
    source = "func mix(a: int, b: float, c: bool) -> void {};"
    expected = "Program(funcs=[FuncDecl(mix, [Param(a, int), Param(b, float), Param(c, bool)], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_058():
    """Test while loop with logical condition"""
    source = """func main() -> void {
        while (x > 0 && y < 10) {
            x = x - 1;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(BinaryOp(Identifier(x), >, IntegerLiteral(0)), &&, BinaryOp(Identifier(y), <, IntegerLiteral(10))), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), -, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_059():
    """Test assignment to array element"""
    source = """func main() -> void {
        arr[1] = 42;
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(42))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_060():
    """Test function call in if condition"""
    source = """func main() -> void {
        if (foo()) {
            x = 1;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=FunctionCall(Identifier(foo), []), then_stmt=BlockStmt([Assignment(IdLValue(x), IntegerLiteral(1))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_061():
    """Test if statement with empty else"""
    source = """func main() -> void {
        if (x > 0) {
            x = x + 1;
        } else {}
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]), else_stmt=BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_062():
    """Test nested function calls"""
    source = """func main() -> void {
        let x = foo(bar(1));
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, FunctionCall(Identifier(foo), [FunctionCall(Identifier(bar), [IntegerLiteral(1)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_063():
    """Test function with float return type"""
    source = """func calc() -> float {
        return 3.14;
    };"""
    expected = "Program(funcs=[FuncDecl(calc, [], float, [ReturnStmt(FloatLiteral(3.14))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_064():
    """Test multiple array declarations"""
    source = """const a: [int; 2] = [1, 2];
    const b: [float; 2] = [1.5, 2.5];"""
    expected = "Program(consts=[ConstDecl(a, [int; 2], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])), ConstDecl(b, [float; 2], ArrayLiteral([FloatLiteral(1.5), FloatLiteral(2.5)]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_065():
    """Test logical NOT in if condition"""
    source = """func main() -> void {
        if (!flag) {
            x = 0;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=UnaryOp(!, Identifier(flag)), then_stmt=BlockStmt([Assignment(IdLValue(x), IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_066():
    """Test for loop with array access in body"""
    source = """func main() -> void {
        for (i in arr) {
            arr[i] = i * 2;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(arr), BlockStmt([Assignment(ArrayAccessLValue(Identifier(arr), Identifier(i)), BinaryOp(Identifier(i), *, IntegerLiteral(2)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_067():
    """Test division operator"""
    source = "const x = 10 / 2;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(IntegerLiteral(10), /, IntegerLiteral(2)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_068():
    """Test function returning string"""
    source = """func greet() -> string {
        return "Hello";
    };"""
    expected = "Program(funcs=[FuncDecl(greet, [], string, [ReturnStmt(StringLiteral('Hello'))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_069():
    """Test multiple pipeline operators"""
    source = "const x = a >> b >> c;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(BinaryOp(Identifier(a), >>, Identifier(b)), >>, Identifier(c)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_070():
    """Test function call with array access as argument"""
    source = """func main() -> void {
        foo(arr[0]);
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(foo), [ArrayAccess(Identifier(arr), IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_071():
    """Test function with boolean parameter"""
    source = "func check(flag: bool) -> void {};"
    expected = "Program(funcs=[FuncDecl(check, [Param(flag, bool)], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_072():
    """Test nested while loops"""
    source = """func main() -> void {
        while (x < 10) {
            while (y < 5) {
                y = y + 1;
            }
            x = x + 1;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(x), <, IntegerLiteral(10)), BlockStmt([WhileStmt(BinaryOp(Identifier(y), <, IntegerLiteral(5)), BlockStmt([Assignment(IdLValue(y), BinaryOp(Identifier(y), +, IntegerLiteral(1)))])), Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_073():
    """Test if statement with empty elif list"""
    source = """func main() -> void {
        if (x == 0) {
            x = 1;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), ==, IntegerLiteral(0)), then_stmt=BlockStmt([Assignment(IdLValue(x), IntegerLiteral(1))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_074():
    """Test function call with mixed argument types"""
    source = """func main() -> void {
        foo(1, true, "test");
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(foo), [IntegerLiteral(1), BooleanLiteral(True), StringLiteral('test')]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_075():
    """Test array literal with mixed expressions"""
    source = "const arr = [x + 1, foo(), true];"
    expected = "Program(consts=[ConstDecl(arr, ArrayLiteral([BinaryOp(Identifier(x), +, IntegerLiteral(1)), FunctionCall(Identifier(foo), []), BooleanLiteral(True)]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_076():
    """Test assignment to multi-dimensional array"""
    source = """func main() -> void {
        arr[0][1] = 5;
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(5))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_077():
    """Test comparison involving function call"""
    source = "const x = foo() == 0;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(FunctionCall(Identifier(foo), []), ==, IntegerLiteral(0)))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_078():
    """Test for loop with function call in expression"""
    source = """func main() -> void {
        for (i in foo()) {
            x = x + i;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, FunctionCall(Identifier(foo), []), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, Identifier(i)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_079():
    """Test return statement with array access"""
    source = """func get() -> int {
        return arr[0];
    };"""
    expected = "Program(funcs=[FuncDecl(get, [], int, [ReturnStmt(ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_080():
    """Test complex logical expression with multiple operators"""
    source = "const x = (a || b) && !c;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(BinaryOp(Identifier(a), ||, Identifier(b)), &&, UnaryOp(!, Identifier(c))))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_081():
    """Test for loop with empty body"""
    source = """func main() -> void {
        for (i in arr) {}
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(arr), BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_082():
    """Test chained logical AND and OR"""
    source = "const x = a && b || c && d;"
    expected = "Program(consts=[ConstDecl(x, BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, BinaryOp(Identifier(c), &&, Identifier(d))))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_083():
    """Test function returning array type"""
    source = """func getArray() -> [int; 3] {
        return [1, 2, 3];
    };"""
    expected = "Program(funcs=[FuncDecl(getArray, [], [int; 3], [ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_084():
    """Test break in nested while loop"""
    source = """func main() -> void {
        while (x < 10) {
            while (y < 5) {
                break;
            }
            x = x + 1;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(x), <, IntegerLiteral(10)), BlockStmt([WhileStmt(BinaryOp(Identifier(y), <, IntegerLiteral(5)), BlockStmt([BreakStmt()])), Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_085():
    """Test continue in nested for loop"""
    source = """func main() -> void {
        for (i in arr) {
            for (j in arr) {
                continue;
            }
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(arr), BlockStmt([ForStmt(j, Identifier(arr), BlockStmt([ContinueStmt()]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_011():
    source = """
        const a = [];
        const a = [1];
        const a = [true, 2.5, \"hi\"];
        const a = [[], [1, 2], 2];
    """
    expected = Program([
            ConstDecl("a", None, ArrayLiteral([])),
            ConstDecl("a", None, ArrayLiteral([IntegerLiteral(1)])),
            ConstDecl("a", None, ArrayLiteral([BooleanLiteral(True), FloatLiteral(2.5), StringLiteral('hi')])),
            ConstDecl("a", None, ArrayLiteral([ArrayLiteral([]), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), IntegerLiteral(2)]))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)
def test_020():
    source = """
        const a = a[1];
        const a = a[2][3];
        const a = a[a[2] + [1,2][1]];
    """
    expected = Program([
        ConstDecl("a", None, ArrayAccess(Identifier("a"), IntegerLiteral(1))),
        ConstDecl("a", None, ArrayAccess(ArrayAccess(Identifier("a"), IntegerLiteral(2)), IntegerLiteral(3))),
        ConstDecl("a", None, ArrayAccess(Identifier("a"), BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(2)), "+", ArrayAccess(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), IntegerLiteral(1)))))
        ], [])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_090():
    source = """
    func main() -> void {
        a[1][2] = 1;
    }
    """
    expected = Program([], [FuncDecl("main", [], VoidType(), [Assignment(ArrayAccessLValue(ArrayAccess(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(1))])])
    assert str(ASTGenerator(source).generate()) == str(expected)
def test_012():
    """Test nested conditional"""
    source = """func main() -> void {
        if (a == "HieuThuHai") {
            if (b == "Trinh") {
                play("Track 1");
            } else if (b == "Exit Sign") {
                play(track2);
            } else {
                stop();
            }
        } else {
            print("HieuThuHai co trinh");
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(a), ==, StringLiteral('HieuThuHai')), then_stmt=BlockStmt([IfStmt(condition=BinaryOp(Identifier(b), ==, StringLiteral('Trinh')), then_stmt=BlockStmt([FunctionCall(Identifier(play), [StringLiteral('Track 1')])]), elif_branches=[(BinaryOp(Identifier(b), ==, StringLiteral('Exit Sign')), BlockStmt([FunctionCall(Identifier(play), [Identifier(track2)])]))], else_stmt=BlockStmt([FunctionCall(Identifier(stop), [])]))]), else_stmt=BlockStmt([FunctionCall(Identifier(print), [StringLiteral('HieuThuHai co trinh')])]))])])"
    assert str(ASTGenerator(source).generate()) == expected
