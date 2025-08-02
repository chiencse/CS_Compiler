from utils import Checker
from utils import Checker
from src.semantics.static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)
from src.utils.nodes import *
def test_001():
    """Test a valid program that should pass all checks"""
    source = """
const PI: float = 3.14;
func main() -> void {
    let x: int = 5;
    let y = x + 1;
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
}
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected

def test007():
    """Test redeclared constant"""
    source = """
const x: int = 1;
const x: float = 2.5;
func main() -> void {}
"""
    expected = "Redeclared Constant: x"
    assert Checker(source).check_from_source() == expected

# def test008():
#     """Test undeclared identifier used in const value"""
#     source = """
#             const y = 2;
#             func main() -> void {}
# """
#     expected = "Undeclared Identifier: x"
#     assert Checker(source).check_from_source() == expected
def test009():
    """Test type mismatch: const annotated float, value is bool"""
    source = """
        const x: float = true;
        func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(x, float, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected
def test010():
    """Test type mismatch: const annotated [5]int, value is int"""
    source = """
        const a: [int; 2] = [1, 2];
        func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test011():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func paramConflict(count: int) -> void {
    let count = 0;  // Redeclared(Variable, count) - conflicts with parameter
}


        }
        func main() -> void {}
"""
    expected = "Redeclared Variable: count"
    assert Checker(source).check_from_source() == expected

def test012():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func main() -> void {
            print(str(undeclaredVar));  // Undeclared(Identifier(), undeclaredVar)
        }
"""
def test013():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func main() -> void {
            undeclaredFunc();           // Undeclared(Function(), undeclaredFunc)
        }
"""
    expected = "Undeclared Function: undeclaredFunc"
    assert Checker(source).check_from_source() == expected
def test014():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func beforeDeclaration() -> void {
            let result = x + 10;  
            let x = 5;
}
        func main() -> void {}

"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test015():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func scopeError() -> void {
            if (true) {
                let localVar = 42;
            }
            print(str(localVar));  // Undeclared(Identifier(), localVar)
        }

        func main() -> void {}

"""
    expected = "Undeclared Identifier: localVar"
    assert Checker(source).check_from_source() == expected
def test016():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
        func earlyCall() -> void {
    laterFunc();  // Undeclared(Function(), laterFunc)
}


        func main() -> void {}

"""
    expected = "Undeclared Function: laterFunc"
    assert Checker(source).check_from_source() == expected

def test0017():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
    const MAX_VALUE = 100;
    func main() -> void {
        let value = MAX_VALU + 1;
    }
"""
    expected = "Undeclared Identifier: MAX_VALU"
    assert Checker(source).check_from_source() == expected
def test018():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
func main() -> void {
    break;                               // MustInLoop(break)
    continue;                            // MustInLoop(continue)
}

"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected

def test0019():
    """Test type cannot be inferred: const = void-returning function"""
    source = """
func main() -> void {
if (true) {
        break;                           // MustInLoop(break)
        continue;                        // MustInLoop(continue)
    }
    
    if (someCondition()) {
        print("Processing");
        break;                           // MustInLoop(break)
    } else {
        continue;                        // MustInLoop(continue)
    }
                       
}

"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected

def test_020():
    source = """
func foo() -> void {}
func goo() -> int {
    let a = 2;
    let b = 3.14;
    return 1;
}
func main() -> void {
    print("a");
    let a = int("1");
    let b = float("1.0");
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_021a():
    source = """
const foo = 1;
func main() -> void {
    foo();
}
"""
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == expected

def test_021b():
    source = """
    func main() -> void {
        if (42) {
            print("Fail");
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=IntegerLiteral(42), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Fail')]))]))"
    assert Checker(source).check_from_source() == expected

def test_021c():
    source = """
    func main() -> void {
        if (3.14) {
            print("Fail");
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=FloatLiteral(3.14), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Fail')]))]))"
    assert Checker(source).check_from_source() == expected

def test_022():
    source = """
    func main() -> void {
        if ("hello") {
            print("Fail");
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=StringLiteral('hello'), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Fail')]))]))"
    assert Checker(source).check_from_source() == expected

def test_023():
    source = """
    func main() -> void {
        if (true) {
            print("Pass");
        } else if (123) {
            print("Fail");
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=BooleanLiteral(True), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Pass')]))]), elif_branches=[(IntegerLiteral(123), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Fail')]))]))])"
    assert Checker(source).check_from_source() == expected

def test_024():
    source = """
    func main() -> void {
        if (false) {
            if ("wrong") {
                print("Invalid");
            }
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=StringLiteral('wrong'), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Invalid')]))]))"
    assert Checker(source).check_from_source() == expected

def test_025():
    source = """
    func main() -> void {
        return 5;
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected

def test_026():
    source = """
    func abc() -> int {
        return;
    }
    func main() -> void {
        abc();
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt()"
    assert Checker(source).check_from_source() == expected

def test_027():
    source = """
    func abc() -> int {
        return true;
    }
    func main() -> void {
        abc();
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_028():
    source = """
    func abc() -> float {
        return "oops";
    }
    func main() -> void {
        abc();
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('oops'))"
    assert Checker(source).check_from_source() == expected

def test_029():
    source = """
    func abc() -> [int; 2] {
        return [1.1, 2.2];
    }
    func main() -> void {
        abc();
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(ArrayLiteral([FloatLiteral(1.1), FloatLiteral(2.2)]))"
    assert Checker(source).check_from_source() == expected
def test_030():
    source = """
func conditionalErrors() -> void {
    let x = true;
    let y = 5
    let message = "hello";
    
    if (x) {                            // TypeMismatchInStatement - int condition
        print("Invalid");
    }
    
    if (!x) {                      // TypeMismatchInStatement - string condition
        print("Also invalid");
    }
    
    if (y > 5 && message) {             // TypeMismatchInStatement - string in logical expression
        print("Mixed error");
    }
}

    func main() -> void {
        return;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BinaryOp(Identifier(y), >, IntegerLiteral(5)), &&, Identifier(message))"
    assert Checker(source).check_from_source() == expected

def test_030_unary_not_on_int():
    source = """
    func main() -> void {
        let x = !42;
    }
    """
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_031_unary_minus_on_bool():
    source = """
    func main() -> void {
        let y = -true;
    }
    """
    expected = "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_032_unary_plus_on_string():
    source = """
    func main() -> void {
        let z = +"hello";
    }
    """
    expected = "Type Mismatch In Expression: UnaryOp(+, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_033_unary_not_on_string():
    source = """
    func main() -> void {
        let a = !"false";
    }
    """
    expected = "Type Mismatch In Expression: UnaryOp(!, StringLiteral('false'))"
    assert Checker(source).check_from_source() == expected

def test_034_unary_minus_on_array():
    source = """
    func main() -> void {
        let a = -[1, 2, 3];
    }
    """
    expected = "Type Mismatch In Expression: UnaryOp(-, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_035_add_string_and_int():
    source = """
    func main() -> void {
        let a = "count: " + 10;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('count: '), +, IntegerLiteral(10))"
    assert Checker(source).check_from_source() == expected

def test_036_logical_and_with_int():
    source = """
    func main() -> void {
        let b = 1 && true;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), &&, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_037_arithmetic_add_bool_and_float():
    source = """
    func main() -> void {
        let c = true + 3.14;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), +, FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected

def test_038_comparison_string_and_bool():
    source = """
    func main() -> void {
        let result = "abc" > false;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('abc'), >, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected

def test_039_equality_int_and_string():
    source = """
    func main() -> void {
        let eq = 1 == "1";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), ==, StringLiteral('1'))"
    assert Checker(source).check_from_source() == expected

def test_040_assign_void_to_variable():
    source = """
    func printMessage(msg: string) -> void {
        print(msg);
    }
    func main() -> void {
        let result = printMessage("hi");    // TypeMismatchInStatement - void function assigned to variable
    }
    """
    # expected = "Type Cannot Be Inferred: VarDecl(result, FunctionCall(Identifier(printMessage), [StringLiteral('hi')]))"
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printMessage), [StringLiteral('hi')])"
    assert Checker(source).check_from_source() == expected

def test_041_string_args_to_int_params():
    source = """
    func addNumbers(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        addNumbers("5", "10");              // TypeMismatchInStatement - string args to int params
    }
    """
    # expected = "Type Mismatch In Statement: FunctionCall(Identifier(addNumbers), [StringLiteral('5'), StringLiteral('10')])"
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(addNumbers), [StringLiteral('5'), StringLiteral('10')]))"
    assert Checker(source).check_from_source() == expected

def test_042_too_many_arguments():
    source = """
    func addNumbers(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        addNumbers(5, 10, 15);              // TypeMismatchInStatement - too many arguments
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(addNumbers), [IntegerLiteral(5), IntegerLiteral(10), IntegerLiteral(15)]))"
    assert Checker(source).check_from_source() == expected

def test_043_too_few_arguments():
    source = """
    func addNumbers(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        addNumbers(5);                      // TypeMismatchInStatement - too few arguments
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(addNumbers), [IntegerLiteral(5)]))"
    assert Checker(source).check_from_source() == expected

def test_050():
    """Test valid program with array declaration and loop"""
    source = """
const SIZE = 3;
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    for x in arr {
        print(str(x));
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Test redeclared function"""
    source = """
func foo() -> void {}
func foo() -> int { return 1; }
func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected

def test_052():
    """Test undeclared array access"""
    source = """
func main() -> void {
    let x = arr[0];
}
"""
    expected = "Undeclared Identifier: arr"
    assert Checker(source).check_from_source() == expected

def test_053():
    """Test type mismatch in array access index"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    let x = arr["invalid"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Test type mismatch in array literal elements"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2.5, 3];
}
"""
    # expected = "Type Mismatch In Statement: VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), FloatLiteral(2.5), IntegerLiteral(3)]))"
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), FloatLiteral(2.5), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Test valid nested loops with break and continue"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    for x in arr {
        if (x > 1) {
            break;
        }
        for y in arr {
            if (y == 1) {
                continue;
            }
            print(str(y));
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_056():
    """Test type mismatch in for loop iterable"""
    source = """
func main() -> void {
    for x in 42 {
        print(str(x));
    }
}
"""
    expected = "Type Mismatch In Statement: ForStmt(x, IntegerLiteral(42), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(x)])]))]))"
    assert Checker(source).check_from_source() == expected

# def test_057():
#     """Test type cannot be inferred for variable without initializer"""
#     source = """
# func main() -> void {
#     let x;
# }
# """
#     expected = "Type Cannot Be Inferred: VarDecl(x, None)"
#     assert Checker(source).check_from_source() == expected

def test_058():
    """Test valid program with multiple constant declarations"""
    source = """
const PI = 3.14;
const MAX = 100;
func main() -> void {
    let x = PI + MAX;
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Test type mismatch in binary operation (int + bool)"""
    source = """
func main() -> void {
    let x = 5 + true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Test valid while loop with condition"""
    source = """
func main() -> void {
    let i = 0;
    while (i < 5) {
        print(str(i));
        i = i + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Test type mismatch in while loop condition"""
    source = """
func main() -> void {
    while ("invalid") {
        print("loop");
    }
}
"""
    expected = "Type Mismatch In Statement: WhileStmt(StringLiteral('invalid'), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('loop')]))]))"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Test redeclared parameter in function"""
    source = """
func test(x: int, x: float) -> void {}
func main() -> void {}
"""
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Test undeclared function in expression"""
    source = """
func main() -> void {
    let x = nonexistent();
}
"""
    expected = "Undeclared Function: nonexistent"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Test type mismatch in assignment to array element"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    arr[0] = "string";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('string'))"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Test valid program with string concatenation"""
    source = """
func main() -> void {
    let s = "hello" + " world";
    print(s);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_066():
    """Test type mismatch in logical operation"""
    source = """
func main() -> void {
    let x = true || 5;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), ||, IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Test valid nested if statements"""
    source = """
func main() -> void {
    let x = 10;
    if (x > 5) {
        if (x < 15) {
            print("In range");
        }
    } else {
        print("Out of range");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_068():
    """Test type mismatch in array access with float index"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    let x = arr[2.5];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), FloatLiteral(2.5))"
    assert Checker(source).check_from_source() == expected

def test_069():
    """Test type cannot be inferred for empty array literal"""
    source = """
func main() -> void {
    let arr = [];
}
"""
    # expected = "Type Cannot Be Inferred: VarDecl(arr, ArrayLiteral([]))"
    expected = "Type Cannot Be Inferred: ArrayLiteral([])"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Test valid function with multiple parameters"""
    source = """
func add(a: int, b: float) -> float {
    return a + b;
}
func main() -> void {
    let result = add(5, 3.14);
    print(str(result));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Test type mismatch in function return type"""
    source = """
func test() -> int {
    return "string";
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('string'))"
    assert Checker(source).check_from_source() == expected

def test_072():
    """Test undeclared variable in nested block"""
    source = """
func main() -> void {
    if (true) {
        let x = y;
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_073():
    """Test valid program with complex array operations"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    arr[1] = arr[0] + arr[2];
    print(str(arr[1]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_074():
    """Test type mismatch in comparison operation"""
    source = """
func main() -> void {
    let x = 5 <= true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), <=, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_075():
    """Test break in nested if statement"""
    source = """
func main() -> void {
    while (true) {
        if (true) {
            break;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_076():
    """Test invalid main function with parameters"""
    source = """
func main(x: int) -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_077():
    """Test invalid main function with non-void return"""
    source = """
func main() -> int {
    return 0;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_078():
    """Test valid program with multiple functions"""
    source = """
func square(x: int) -> int {
    return x * x;
}
func main() -> void {
    let x = square(4);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_079():
    """Test type mismatch in array element assignment"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    arr[0] = true;
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_080():
    """Test valid nested array access"""
    source = """
func main() -> void {
    let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
    let x = arr[0][1];
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_081():
    """Test type mismatch in nested array access"""
    source = """
func main() -> void {
    let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
    let x = arr[true][1];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_082():
    """Test redeclared variable in nested block"""
    source = """
func main() -> void {
    let x = 5;
    if (true) {
        let x = 10;
    }
}
"""
    expected = "Static checking passed"  # Shadowing is allowed
    assert Checker(source).check_from_source() == expected

def test_083():
    """Test undeclared variable in for loop body"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    for x in arr {
        let y = z;
    }
}
"""
    expected = "Undeclared Identifier: z"
    assert Checker(source).check_from_source() == expected

def test_084():
    """Test type mismatch in array literal size"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2, 3];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [int; 2], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_085():
    """Test valid program with complex condition"""
    source = """
func main() -> void {
    let x = 5;
    let y = 10;
    if (x > 3 && y < 15) {
        print("Valid");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_086():
    """Test type mismatch in logical operation with string"""
    source = """
func main() -> void {
    let x = true && "hello";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), &&, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_087():
    """Test valid program with function returning array"""
    source = """
func getArray() -> [int; 2] {
    return [1, 2];
}
func main() -> void {
    let arr = getArray();
    print(str(arr[0]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


# def test_089():
#     """Test type cannot be inferred for parameter"""
#     source = """
# func test(x: auto) -> void {}
# func main() -> void {}
# """
#     expected = "Type Cannot Be Inferred: Param(x, AutoType())"
#     assert Checker(source).check_from_source() == expected

def test_090():
    """Test valid program with multiple nested loops"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    for x in arr {
        for y in arr {
            print(str(x + y));
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_091():
    """Test type mismatch in return array type"""
    source = """
func test() -> [int; 2] {
    return [1.5, 2.5];
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(ArrayLiteral([FloatLiteral(1.5), FloatLiteral(2.5)]))"
    assert Checker(source).check_from_source() == expected

def test_092():
    """Test undeclared variable in else block"""
    source = """
func main() -> void {
    if (false) {
        let x = 5;
    } else {
        let y = x;
    }
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test_093():
    """Test valid program with complex arithmetic"""
    source = """
func main() -> void {
    let x = 5;
    let y = 3.14;
    let z = (x + y) * 2.0;
    print(str(z));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_094():
    """Test type mismatch in modulo operation"""
    source = """
func main() -> void {
    let x = 5 % 2.5;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), %, FloatLiteral(2.5))"
    assert Checker(source).check_from_source() == expected

def test_095():
    """Test valid program with chained comparisons"""
    source = """
func main() -> void {
    let x = 10;
    if (5 < x && x < 15) {
        print("In range");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_096():
    """Test type mismatch in array assignment to non-array"""
    source = """
func main() -> void {
    let x: int = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_097():
    """Test valid program with recursive function"""
    source = """
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
func main() -> void {
    let x = factorial(5);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
#! Functions must be declared before being called
def test_098():
    """Test type mismatch in recursive function call"""
    source = """
func test(x: int) -> int {
    return test("invalid");
}
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(test), [StringLiteral('invalid')])"
    assert Checker(source).check_from_source() == expected

def test_099():
    """Test continue in nested if statement"""
    source = """
func main() -> void {
    while (true) {
        if (true) {
            continue;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_100():
    """Test type mismatch in array literal with mixed types"""
    source = """
func main() -> void {
    let arr = [1, "string", 3];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), StringLiteral('string'), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected

def test_101():
    """Test valid program with complex nested array"""
    source = """
func main() -> void {
    let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
    let x = arr[0][0] + arr[1][1];
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_102():
    """Test redeclared variable in for loop""" #!redeclared variable in for loop
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    for x in arr {
        let x = 5;
    }
}
"""
    expected = "Redeclared Variable: x" 
    assert Checker(source).check_from_source() == expected

def test_103():
    """Test type mismatch in return with wrong array size"""
    source = """
func test() -> [int; 3] {
    return [1, 2];
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_104():
    """Test undeclared variable in while loop condition"""
    source = """
func main() -> void {
    while (x < 5) {
        print("loop");
    }
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test_105():
    """Test valid program with multiple returns"""
    source = """
func test(x: int) -> int {
    if (x > 0) {
        return x;
    }
    return 0;
}
func main() -> void {
    let x = test(5);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_106():
    """Test type mismatch in string concatenation with int"""
    source = """
func main() -> void {
    let s = "test" + 5;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('test'), +, IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected

def test_107():
    """Test valid program with nested while loops"""
    source = """
func main() -> void {
    let i = 0;
    while (i < 3) {
        let j = 0;
        while (j < 2) {
            print(str(i + j));
            j = j + 1;
        }
        i = i + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_108():
    """Test type mismatch in equality comparison"""
    source = """
func main() -> void {
    let x = 5 == "five";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), ==, StringLiteral('five'))"
    assert Checker(source).check_from_source() == expected

def test_109():
    """Test valid program with array of arrays"""
    source = """
func main() -> void {
    let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
    for row in arr {
        for x in row {
            print(str(x));
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_110():
    """Test type mismatch in array access with bool index"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    let x = arr[true];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_111():
    """Test redeclared constant in global scope"""
    source = """
const X = 5;
const X = 10;
func main() -> void {}
"""
    expected = "Redeclared Constant: X"
    assert Checker(source).check_from_source() == expected

def test_112():
    """Test undeclared variable in array literal"""
    source = """
func main() -> void {
    let arr = [x, 2];
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test_113():
    """Test valid program with complex function call"""
    source = """
func compute(a: int, b: float) -> float {
    return a + b;
}
func main() -> void {
    let x = compute(5, 3.14);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_115():
    """Test valid program with mixed type arithmetic"""
    source = """
func main() -> void {
    let x: float = 5 + 3.14;
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_116():
    """Test type mismatch in division operation"""
    source = """
func main() -> void {
    let x = 5 / true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), /, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_117():
    """Test valid program with else-if chain"""
    source = """
func main() -> void {
    let x = 10;
    if (x < 5) {
        print("Small");
    } else if (x < 15) {
        print("Medium");
    } else {
        print("Large");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_118():
    """Test type mismatch in else-if condition"""
    source = """
func main() -> void {
    if (true) {
        print("True");
    } else if ("false") {
        print("False");
    }
}
"""
    expected = "Type Mismatch In Statement: IfStmt(condition=BooleanLiteral(True), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('True')]))]), elif_branches=[(StringLiteral('false'), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('False')]))]))])"
    assert Checker(source).check_from_source() == expected

def test_119():
    """Test valid program with array modification in loop"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    for i in arr {
        arr[0] = i + 1;
    }
    print(str(arr[0]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_120():
    """Test type mismatch in array element type"""
    source = """
func main() -> void {
    let arr: [string; 2] = ["a", 1];
}
"""
    # expected = "Type Mismatch In Statement: VarDecl(arr, [string; 2], ArrayLiteral([StringLiteral('a'), IntegerLiteral(1)]))"
    expected = "Type Mismatch In Expression: ArrayLiteral([StringLiteral('a'), IntegerLiteral(1)])"
    assert Checker(source).check_from_source() == expected

def test_121():
    """Test valid program with function composition"""
    source = """
func square(x: int) -> int {
    return x * x;
}
func double(x: int) -> int {
    return x * 2;
}
func main() -> void {
    let x = square(double(3));
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_122():
    """Test undeclared function in nested expression"""
    source = """
func main() -> void {
    let x = unknown(5) + 1;
}
"""
    expected = "Undeclared Function: unknown"
    assert Checker(source).check_from_source() == expected

def test_123():
    """Test type mismatch in array access assignment"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    arr[0] = [3, 4];
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)]))"
    assert Checker(source).check_from_source() == expected

def test_124():
    """Test valid program with complex logical expression"""
    source = """
func main() -> void {
    let x = 5;
    let y = 10;
    if (!(x > 3 || y < 5)) {
        print("Complex condition");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_125():
    """Test type mismatch in nested binary operation"""
    source = """
func main() -> void {
    let x = (5 + true) * 2;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_126():
    """Test valid program with array of floats"""
    source = """
func main() -> void {
    let arr: [float; 2] = [1.5, 2.5];
    print(str(arr[0] + arr[1]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_127():
    """Test type mismatch in function call with wrong number of args"""
    source = """
func test(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    test(1);
}
"""
    # expected = "Type Mismatch In Expression: FunctionCall(Identifier(test), [IntegerLiteral(1)])"
    expected= "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(test), [IntegerLiteral(1)]))"
    assert Checker(source).check_from_source() == expected

def test_128():
    """Test valid program with empty block"""
    source = """
func main() -> void {
    if (true) {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_129():
    """Test type mismatch in unary operation on array"""
    source = """
func main() -> void {
    let x = -[1, 2];
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_130():
    """Test valid program with multiple constants and expressions"""
    source = """
const A = 1;
const B = 2.5;
func main() -> void {
    let x = A + B;
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_131():
    """Test redeclared variable in same block"""
    source = """
func main() -> void {
    let x = 5;
    let x = 10;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_132():
    """Test undeclared variable in complex expression"""
    source = """
func main() -> void {
    let x = y + z * 2;
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_133():
    """Test valid program with array initialization and loop"""
    source = """
func main() -> void {
    let arr: [int; 3] = [0, 0, 0];
    let i = 0;
    while (i < 3) {
        arr[i] = i + 1;
        i = i + 1;
    }
    print(str(arr[2]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_134():
    """Test type mismatch in array assignment with wrong type"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    arr[0] = "invalid";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test_135():
    """Test valid program with nested function calls"""
    source = """
func add(x: int, y: int) -> int {
    return x + y;
}
func main() -> void {
    let x = add(add(1, 2), 3);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_136():
    """Test type mismatch in comparison with array"""
    source = """
func main() -> void {
    let x = [1, 2] > [3, 4];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), >, ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)]))"
    assert Checker(source).check_from_source() == expected

def test_137():
    """Test valid program with complex array operations"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    let sum = arr[0] + arr[1] + arr[2];
    print(str(sum));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_138():
    """Test type mismatch in function return with void"""
    source = """
func test() -> void {
    return 5;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected

def test_139():
    """Test valid program with string concatenation in loop"""
    source = """
func main() -> void {
    let arr: [string; 2] = ["a", "b"];
    let s = "";
    for x in arr {
        s = s + x;
    }
    print(s);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_140():
    """Test type mismatch in array literal with wrong size"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_141():
    """Test valid program with nested blocks"""
    source = """
func main() -> void {
    let x = 5;
    {
        let y = x + 1;
        print(str(y));
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_142():
    """Test undeclared variable in nested block"""
    source = """
func main() -> void {
    {
        let x = y;
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_143():
    """Test valid program with multiple array assignments"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    arr[0] = arr[1];
    arr[1] = arr[2];
    print(str(arr[0]));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_144():
    """Test type mismatch in logical operation with float"""
    source = """
func main() -> void {
    let x = 3.14 && true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FloatLiteral(3.14), &&, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_145():
    """Test valid program with complex function"""
    source = """
func process(arr: [int; 3]) -> int {
    let sum = 0;
    for x in arr {
        sum = sum + x;
    }
    return sum;
}
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    let x = process(arr);
    print(str(x));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_146():
    """Test type mismatch in function call with array"""
    source = """
func test(x: int) -> void {}
func main() -> void {
    test([1, 2]);
}
"""
    # expected = "Type Mismatch In Expression: FunctionCall(Identifier(test), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])])"
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(test), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])]))"
    assert Checker(source).check_from_source() == expected

def test_147():
    """Test valid program with empty else block"""
    source = """
func main() -> void {
    if (true) {
        print("True");
    } else {}
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_148():
    """Test type mismatch in array access with string index"""
    source = """
func main() -> void {
    let arr: [int; 2] = [1, 2];
    let x = arr["index"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), StringLiteral('index'))"
    assert Checker(source).check_from_source() == expected

def test_149():
    """Test valid program with complex nested conditions"""
    source = """
func main() -> void {
    let x = 5;
    if (x > 0) {
        if (x < 10) {
            print("In range");
        } else {
            print("Too large");
        }
    } else {
        print("Negative");
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_150():
        source = """
    const foo = 1;
    func main() -> void {
        main = 1;
    }
    """
        expected = "Undeclared Identifier: main"
def test_151():
        source = """
    const c = 1;
    const b: int = 1;
    const a: int = 1.0;
    func main() -> void {}
    """
        expected = TypeMismatchInStatement(ConstDecl("a", IntType(), FloatLiteral(1.0)))

def test_0152():
        source = """
    const a = 1;
    func main() -> void {
        let i = a;
        a = 1; // const
    }
    """
        expected = TypeMismatchInStatement(Assignment(IdLValue("a"), IntegerLiteral(1)))
def test_0153():
    source = """
const a: [int; 3] = [1,2,3];
func main() -> void {
    let i = a[1];
    a[1] = 1; // const
}
"""
    expected = TypeMismatchInStatement(Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(1)))

def test_154():
    source = """
const a: [[int; 2]; 2] = [[1,2],[3,4]];
func main() -> void {
    let i = a[1][1];
    a[1][1] = 1; // const
}
"""
    expected = TypeMismatchInStatement(Assignment(ArrayAccessLValue(ArrayAccess(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(1)), IntegerLiteral(1)))

def test_155a():
    source = """
func main() -> void {
    while(true) {}
    while(1) {}
}
"""
    expected =  TypeMismatchInStatement(WhileStmt(IntegerLiteral(1), BlockStmt([])))

def test_155b():
    source = """
const array = [[1], [2]];
func main() -> void {
    for (a in array) {
        a = [2];
        a = [1,2];
    }
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])))

def test_155c():
    source = """
func main() -> void {
    let a: int = [1,2,3];
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
    assert Checker(source).check_from_source() == str(expected)

def test_156():
    source = """
func main() -> void {
    let a: [int; 3] = [1,2,"s"];
}
"""
    expected = TypeMismatchInExpression(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), StringLiteral('s')]))
    assert Checker(source).check_from_source() == str(expected)

def test_157():
    source = """
func main() -> void {
    for (a in 1) {}
}
"""
    expected = TypeMismatchInStatement(ForStmt("a", IntegerLiteral(1), BlockStmt([])))
    assert Checker(source).check_from_source() == str(expected)

def test_158():
    source = """
func main() -> void {
    return [1,2];
}
"""
    expected = TypeMismatchInStatement(ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])))
    assert Checker(source).check_from_source() == str(expected)

def test_159():
    source = """
func main() -> void {
    let a = [1,2,3];
    let b = a[2][3];
}
"""
    expected = TypeMismatchInExpression(ArrayAccess(ArrayAccess(Identifier("a"), IntegerLiteral(2)), IntegerLiteral(3)))
    assert Checker(source).check_from_source() == str(expected)

# def test_160():
#     source = """
# func main() -> void {
#     print("s");
#     input();
# }
# """
#     expected = TypeMismatchInStatement(FunctionCall(Identifier("input"), []))
#     assert Checker(source).check_from_source() == str(expected)

def test_161():
    source = """
func main() -> void {
    let a: int = str(1) == str(1.0);
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), BinaryOp(FunctionCall(Identifier("str"), [IntegerLiteral(1)]), "==", FunctionCall(Identifier("str"), [FloatLiteral(1.0)]))))
    assert Checker(source).check_from_source() == str(expected)

def test_162():
    source = """
func main() -> void {
    let a: int = str();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("str"), []))
    assert Checker(source).check_from_source() == str(expected)

def test_163():
    source = """
func TIEN(a:int) -> void{
    a = 1;
}
func main() -> void {}
"""
    expected =  TypeMismatchInStatement(Assignment(IdLValue("a"), IntegerLiteral(1)))
    assert Checker(source).check_from_source() == str(expected)

# def test_164():
#     source = """
# func main() -> void {
#     let a = [1, 2];
#     a[1+0] = 1;
#     a = [1,2,3];
# }
# """
#     expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
#     assert Checker(source).check_from_source() == str(expected)

def test_165():
    source = """
func main() -> void {
    let a = --1 > 2 && true;
    let b = "s" + 1;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(StringLiteral('s'), "+", IntegerLiteral(1)))
    assert Checker(source).check_from_source() == str(expected)


def test_166():
    source = """
const array = [1,2,3];
func main() -> void {
    for (a in array) {
        a = 2;
        let a = "string";
    }
}
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == str(expected)

def test_167():
    source = """
func main() -> void {
    if (true) {} else {}
    if (1) {}
}
"""
    expected = TypeMismatchInStatement(IfStmt(IntegerLiteral(1),BlockStmt([]),[],None))
    assert Checker(source).check_from_source() == str(expected)

def test_168():
    source = """
func main() -> void {
    if (true) {} else if (true) {} else if (1) {} else {}
}
"""
    expected = TypeMismatchInStatement(IfStmt(BooleanLiteral(True),BlockStmt([]),[(BooleanLiteral(True), BlockStmt([])), (IntegerLiteral(1), BlockStmt([]))],BlockStmt([])))
    assert Checker(source).check_from_source() == str(expected)

def test_169():
    source = """
func foo() -> int {return 1;}
func main() -> void {
    let a = foo;
}
"""
    expected = "Undeclared Identifier: foo"
    assert Checker(source).check_from_source() == str(expected)

def test_170():
    source = """
func main() -> void {
    let a: float = 1 - 1.0;
    let b: float = 1.0 + 1;
    let c: float = 1.0 + 1.0;
    let d: int = 1.0 - 1;
}
"""
    expected = TypeMismatchInStatement(VarDecl("d", IntType(), BinaryOp(FloatLiteral(1.0), "-", IntegerLiteral(1))))
    assert Checker(source).check_from_source() == str(expected)

# def test_106():
#     source = """
# func main() -> void {
#     let a: bool = 1 == 1;
#     let b: bool = 1.0 != 1.0;
#     let c: bool = 1 == 1.0;
#     let d: bool = 1.0 != 1;
#     let e: bool = "a" != "b";
#     let f: bool = true == false;
# }
# """
#     expected = "Static checking passed"
#     assert Checker(source).check_from_source() == str(expected)

def test_171():
    source = """
func main() -> void {
    let a: bool = 1 >= 1;
    let b: bool = 1.0 <= 1.0;
    let c: bool = 1 > 1.0;
    let d: bool = 1.0 < 1;
    let e: bool = "a" == "b";
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_172():
    source = """
func main() -> void {
    let a: int = 1 == 1;
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), BinaryOp(IntegerLiteral(1), "==", IntegerLiteral(1))))
    assert Checker(source).check_from_source() == str(expected)

def test_173():
    source = """
func main() -> void {
    let a: int = 1 >= 1.0;
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), BinaryOp(IntegerLiteral(1), ">=", FloatLiteral(1.0))))
    assert Checker(source).check_from_source() == str(expected)

def test_174():
    source = """
func main() -> void {
    let a: int = true < false;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(BooleanLiteral(True), "<", BooleanLiteral(False)))
    assert Checker(source).check_from_source() == str(expected)



def test_176():
    source = """
func main() -> void {
    let b: string = str(1);
    let c: string = str(1.0);
    let d: string = str(true);
    let e: string = str();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("str"), []))
    assert Checker(source).check_from_source() == str(expected)

def test_177():
    source = """
func main() -> void {
    let b: string = str(str(1.0) >= "a");
    let c: string = str("s");
}
"""
    # expected =  TypeMismatchInExpression(FunctionCall(Identifier("str"), [StringLiteral('s')]))
    expected = TypeMismatchInExpression(BinaryOp(FunctionCall(Identifier("str"), [FloatLiteral(1.0)]), ">=", StringLiteral('a')))
    assert Checker(source).check_from_source() == str(expected)

def test_178():
    source = """
func a() -> void {}
func main() -> void {
    let b = a();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("a"), []))
    assert Checker(source).check_from_source() == str(expected)

def test_150():
    source = """
func a() -> void {}
func main() -> void {
    print("a");
    print(1);
}
"""
    expected = TypeMismatchInStatement(ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(1)])))
    assert Checker(source).check_from_source() == str(expected)

def test_154():
    source = """
func main() -> void {
    1 + "A";
}
"""
    expected = TypeMismatchInExpression(BinaryOp(IntegerLiteral(1), "+", StringLiteral('A')))
    assert Checker(source).check_from_source() == str(expected)

def test_155():
    source = """
func main() -> void {
    let a: int = [1,2,3];
}
"""
    expected = TypeMismatchInStatement(VarDecl("a", IntType(), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
    assert Checker(source).check_from_source() == str(expected)

def test_156():
    source = """
func main() -> void {
    let a: [int; 3] = [1,2,"s"];
}
"""
    expected = TypeMismatchInExpression(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), StringLiteral('s')]))
    assert Checker(source).check_from_source() == str(expected)

def test_157():
    source = """
func main() -> void {
    for (a in 1) {}
}
"""
    expected = TypeMismatchInStatement(ForStmt("a", IntegerLiteral(1), BlockStmt([])))
    assert Checker(source).check_from_source() == str(expected)

def test_158():
    source = """
func main() -> void {
    return [1,2];
}
"""
    expected = TypeMismatchInStatement(ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])))
    assert Checker(source).check_from_source() == str(expected)

def test_159():
    source = """
func main() -> void {
    let a = [1,2,3];
    let b = a[2][3];
}
"""
    expected = TypeMismatchInExpression(ArrayAccess(ArrayAccess(Identifier("a"), IntegerLiteral(2)), IntegerLiteral(3)))
    assert Checker(source).check_from_source() == str(expected)

def test_160():
    source = """
func main() -> void {
    print("s");
    input();
}
"""
    expected = TypeMismatchInStatement(ExprStmt(FunctionCall(Identifier("input"), [])))
    assert Checker(source).check_from_source() == str(expected)


def test_162():
    source = """
func main() -> void {
    let a: int = str();
}
"""
    expected = TypeMismatchInExpression(FunctionCall(Identifier("str"), []))
    assert Checker(source).check_from_source() == str(expected)

def test_163():
    source = """
func TIEN(a:int) -> void{
    a = 1;
}
func main() -> void {}
"""
    expected =  TypeMismatchInStatement(Assignment(IdLValue("a"), IntegerLiteral(1)))
    assert Checker(source).check_from_source() == str(expected)

def test_163():
    source = """
func main() -> void {
    let a = [1, 2];
    a[1+0] = 1;
    a = [1,2,3];
}
"""
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])))
    assert Checker(source).check_from_source() == str(expected)

def test_164():
    source = """
func main() -> void {
    let a = --1 > 2 && true;
    let b = "s" + 1;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(StringLiteral('s'), "+", IntegerLiteral(1)))
    assert Checker(source).check_from_source() == str(expected)

def test_167():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}

func main() -> void {
    let a: int = 1 >> C;
}
"""
    expected = "Undeclared Function: C"
    assert Checker(source).check_from_source() == str(expected)

def test_174(): #! Check type error when return
    source = """
func A(a: int) -> int {return 1;}
func B() -> int {return 1;}

func main() -> void {
    let a: string = 1 >> str;
    let b: string = 1.0 >> str;
    let c: string = true >> str;
    let d: string = "1" >> print;
}
"""
    expected = TypeMismatchInExpression(BinaryOp(StringLiteral('1'), ">>", Identifier("print")))
    assert Checker(source).check_from_source() == str(expected)

def test_175():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}

func main() -> void {
    let a: int = 2 >> C(1);
}
"""
    expected = "Undeclared Function: C"
    assert Checker(source).check_from_source() == str(expected)

def test_176():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}

func main() -> void {
    let b: int = 2 >> B(1);
    let a: int = 2 >> B(1.0);
}
"""
    expected = TypeMismatchInExpression(BinaryOp(IntegerLiteral(2), ">>", FunctionCall(Identifier("B"), [FloatLiteral(1.0)])))
    assert Checker(source).check_from_source() == str(expected)

def test_180():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> void {return ;}

func main() -> void {
    let b: int = 2 >> A >> B(1);
}
"""
    expected = TypeMismatchInExpression(BinaryOp(BinaryOp(IntegerLiteral(2), ">>", Identifier("A")), ">>", FunctionCall(Identifier("B"), [IntegerLiteral(1)])))
    assert Checker(source).check_from_source() == str(expected)


def test_184():
    source = """
func b(a: int) -> int {return 1;}
func main() -> void {
    2 >> b;
}
"""
    expected = TypeMismatchInStatement(ExprStmt(BinaryOp(IntegerLiteral(2), ">>", Identifier("b"))))
    assert Checker(source).check_from_source() == str(expected)

def test_186():
    source = """
func A(a: int, b: int) -> void {return ;}
func B(a: int) -> int {return 1;}

func main() -> void {
    2 >> B >> A(2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_187():
    source = """
func A(a: int, b: int) -> void {return ;}
func B(a: int) -> int {return 1;}

func main() -> void {
    "s" >> A(2);
}
"""
    expected = TypeMismatchInStatement(ExprStmt(BinaryOp(StringLiteral('s'), ">>", FunctionCall(Identifier("A"), [IntegerLiteral(2)]))))
    assert Checker(source).check_from_source() == str(expected)

def test_179():
        source = """
    func A(a: int) -> int {return 1;}
    func B(a: int, b: int) -> int {return 1;}
    
    func main() -> void {
        let b: int = 2 >> A(1);
    }
    """
        expected = TypeMismatchInExpression(BinaryOp(IntegerLiteral(2), ">>", FunctionCall(Identifier("A"), [IntegerLiteral(1)])))
def test_180():
        source = """
    func A(a: int) -> int {return 1;}
    func B(a: int, b: int) -> int {return 1;}
    
    func main() -> void {
        let a: int = "s" >> A;
    }
    """
        expected = TypeMismatchInExpression(BinaryOp(StringLiteral('s'), ">>", Identifier("A")))
def test_181():
        source = """
    func A(a: int) -> int {return 1;}
    func B(a: int, b: int) -> int {return 1;}
    
    func main() -> void {
        let a: int = 2 >> A;
        let b: string = 2 >> A;
    }
    """
        expected =  TypeMismatchInStatement(VarDecl("b", StringType(), BinaryOp(IntegerLiteral(2), ">>", Identifier("A"))))
def test_182():
        source = """
    func A(a: int) -> int {return 1;}
    func B(a: int, b: int) -> int {return 1;}
    
    func main() -> void {
        let a: int = "s" >> 1;
    }
    """
        expected =  TypeMismatchInExpression(BinaryOp(StringLiteral('s'), ">>", IntegerLiteral(1)))
def test_183():
        source = """
    func A(a: int) -> int {return 1;}
    func B(a: int, b: int) -> int {return 1;}
    
    func main() -> void {
        let a: int = C >> A;
    }
    """
        expected = "Undeclared Identifier: C"
