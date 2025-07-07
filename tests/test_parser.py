from utils import Parser
def test_001():
    """Normal case: Integer variable with explicit type"""
    source = """func main() -> void { let x: int = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Normal case: Float variable with inferred type"""
    source = """func main() -> void { let x = 3.14; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    """Normal case: Boolean variable with explicit type"""
    source = """func main() -> void { let isValid: bool = true; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    """Normal case: String variable with inferred type"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_005():
    """Normal case: Array variable with explicit type"""
    source = """func main() -> void { let numbers: [int; 5] = [1, 2, 3, 4, 5]; }"""
    expected = "success"
    assert Parser(source).parse() == expected



def test_010():
    """Normal case: Multi-dimensional array"""
    source = """func main() -> void { let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_011():
    """Edge case: Invalid array size (non-integer)"""
    source = """func main() -> void{let arr: [int; x] = [1, 2];}"""
    expected = "Error on line 1 col 35: x"
    assert Parser(source).parse() == expected

def test_012():
    """Worst case: Long identifier name"""
    source = """func main() -> void { let veryLongVariableName1234567890: int = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    """Edge case: Missing type in array declaration"""
    source = """func main() -> void{let arr: [; 5] = [1, 2, 3, 4, 5];}"""
    expected = "Error on line 1 col 30: ;"
    assert Parser(source).parse() == expected

def test_014():
    """Normal case: Variable with complex expression initializer"""
    source = """func main() -> void { let result = 5 + 3 * 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_016():
    """Normal case: Variable with function call initializer"""
    source = """func main() -> void { let value = add(5, 3); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_017():
    """Edge case: Missing assignment operator"""
    source = """func main() -> void{let x: int 42;}"""
    expected = "Error on line 1 col 31: 42"
    assert Parser(source).parse() == expected

def test_018():
    """Normal case: Variable with array access initializer"""
    source = """func main() -> void { let x = numbers[0]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_019():
    """Edge case: Missing array size in type annotation"""
    source = """func main() -> void{let arr: [int; ] = [1, 2];}"""
    expected = "Error on line 1 col 35: ]"
    assert Parser(source).parse() == expected

def test_020():
    """Worst case: Nested array declaration"""
    source = """func main() -> void { let cube: [[[int; 4]; 3]; 2] = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_021():
    """Edge case: Whitespace before let"""
    source = """func main() -> void {    let x = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_022():
    """Normal case: Variable with boolean expression"""
    source = """func main() -> void { let flag = true && false; }"""
    expected = "success"
    assert Parser(source).parse() == expected



def test_024():
    """Normal case: Variable with string concatenation"""
    source = """func main() -> void { let message = "Hello" + "World"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_025():
    """Edge case: Missing colon in type annotation"""
    source = """func main() -> void{let x int = 42;}"""
    expected = "Error on line 1 col 26: int"
    assert Parser(source).parse() == expected

def test_026():
    """Normal case: Variable with negative integer"""
    source = """func main() -> void { let x = -42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_027():
    """Edge case: Invalid array literal syntax"""
    source = """func main() -> void{let arr = [1, 2, ;}"""
    expected = "Error on line 1 col 37: ;"
    assert Parser(source).parse() == expected

def test_028():
    """Normal case: Variable with parenthesized expression"""
    source = """func main() -> void { let x = (5 + 3) * 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_029():
    """Edge case: Trailing comma in array literal"""
    source = """func main() -> void {let arr = [1, 2, 3, ];}"""
    expected = "Error on line 1 col 41: ]"
    assert Parser(source).parse() == expected

def test_030():
    """Worst case: Multiple variables in sequence"""
    source = """func main() -> void { let x = 1; let y = 2; let z = 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_031():
    """Normal case: Integer constant with explicit type"""
    source = """const MAX_SIZE: int = 100;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    """Normal case: Float constant with inferred type"""
    source = """const PI = 3.14159;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_033():
    """Normal case: String constant with explicit type"""
    source = """const APP_NAME: string = "HLang";"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_034():
    """Normal case: Boolean constant with inferred type"""
    source = """const IS_DEBUG = false;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_035():
    """Normal case: Array constant with explicit type"""
    source = """const PRIMES: [int; 5] = [2, 3, 5, 7, 11];"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_036():
    """Edge case: Missing initializer for constant"""
    source = """const X: int;"""
    expected = "Error on line 1 col 12: ;"
    assert Parser(source).parse() == expected

def test_037():
    """Edge case: Missing semicolon"""
    source = """const X = 42"""
    expected = "Error on line 1 col 12: <EOF>"
    assert Parser(source).parse() == expected

def test_038():
    """Edge case: Invalid type annotation"""
    source = """const X: invalid = 42;"""
    expected = "Error on line 1 col 9: invalid"
    assert Parser(source).parse() == expected

def test_039():
    """Normal case: Constant with complex expression"""
    source = """const RESULT = 5 + 3 * 2;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_040():
    """Edge case: Empty identifier"""
    source = """const : int = 42;"""
    expected = "Error on line 1 col 6: :"
    assert Parser(source).parse() == expected

def test_041():
    """Normal case: Constant with string concatenation"""
    source = """const GREETING = "Hello" + "World";"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_042():
    """Edge case: Missing assignment operator"""
    source = """const X: int 42;"""
    expected = "Error on line 1 col 13: 42"
    assert Parser(source).parse() == expected

def test_043():
    """Normal case: Multi-dimensional array constant"""
    source = """const MATRIX: [[int; 2]; 2] = [[1, 2], [3, 4]];"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_044():
    """Edge case: Invalid array size"""
    source = """const ARR: [int; x] = [1, 2];"""
    expected = "Error on line 1 col 17: x"
    assert Parser(source).parse() == expected

def test_045():
    """Worst case: Long constant name"""
    source = """const VERY_LONG_CONSTANT_NAME_1234567890: int = 42;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_046():
    """Edge case: Missing colon in type annotation"""
    source = """const X int = 42;"""
    expected = "Error on line 1 col 8: int"
    assert Parser(source).parse() == expected

def test_047():
    """Normal case: Constant with negative float"""
    source = """const NEG_PI = -3.14159;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_048():
    """Edge case: Invalid array literal syntax"""
    source = """const ARR = [1, 2, ;"""
    expected = "Error on line 1 col 19: ;"
    assert Parser(source).parse() == expected

def test_049():
    """Normal case: Constant with boolean expression"""
    source = """const FLAG = true || false;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_050():
    """Edge case: Trailing comma in array literal"""
    source = """const ARR = [1, 2, 3, ];"""
    expected = "Error on line 1 col 22: ]"
    assert Parser(source).parse() == expected

def test_051():
    """Normal case: Constant with parenthesized expression"""
    source = """const VALUE = (5 + 3) * 2;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_052():
    """Edge case: Whitespace before const"""
    source = """   const X = 42;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_053():
    """Normal case: Constant with function call initializer"""
    source = """const RESULT = add(5, 3);"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_054():
    """Edge case: Invalid character in identifier"""
    source = """const x@y: int = 42;"""
    expected = "Error Token @"
    assert Parser(source).parse() == expected

def test_055():
    """Worst case: Multiple constants in sequence"""
    source = """const X = 1; const Y = 2; const Z = 3;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_056():
    """Normal case: Constant with array access initializer"""
    source = """func main() -> void { let VALUE = numbers[0]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_057():
    """Edge case: Missing array size in type annotation"""
    source = """const ARR: [int; ] = [1, 2];"""
    expected = "Error on line 1 col 17: ]"
    assert Parser(source).parse() == expected

def test_058():
    """Normal case: Constant with negative integer"""
    source = """const NEG = -42;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_059():
    """Edge case: Invalid literal in initializer"""
    source = """const X = @invalid;"""
    expected = "Error Token @"
    assert Parser(source).parse() == expected

def test_060():
    """Worst case: Deeply nested array constant"""
    source = """const CUBE: [[[int; 2]; 2]; 2] = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]];"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_061():
    """Normal case: Integer literal expression"""
    source = """func main() -> void { let x = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_062():
    """Normal case: Float literal expression"""
    source = """func main() -> void { let x = 3.14; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_063():
    """Normal case: Boolean literal expression"""
    source = """func main() -> void { let x = true; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_064():
    """Normal case: String literal expression"""
    source = """func main() -> void { let x = "hello"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_065():
    """Normal case: Array literal expression"""
    source = """func main() -> void { let x = [1, 2, 3]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_066():
    """Edge case: Missing closing parenthesis"""
    source = """func main() -> void { let x = (42; }"""
    expected = "Error on line 1 col 33: ;"
    assert Parser(source).parse() == expected

def test_067():
    """Normal case: Arithmetic addition"""
    source = """func main() -> void { let x = 5 + 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_068():
    """Normal case: Arithmetic multiplication"""
    source = """func main() -> void { let x = 5 * 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_069():
    """Normal case: Comparison expression"""
    source = """func main() -> void { let x = 5 < 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_070():
    """Normal case: Logical AND expression"""
    source = """func main() -> void { let x = true && false; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_071():
    """Edge case: Missing operand in binary expression"""
    source = """func main() -> void { let x = 5 + ; }"""
    expected = "Error on line 1 col 34: ;"
    assert Parser(source).parse() == expected

def test_072():
    """Normal case: Array access expression"""
    source = """func main() -> void { let x = numbers[0]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_073():
    """Normal case: Function call expression"""
    source = """func main() -> void { let x = add(5, 3); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_074():
    """Edge case: Missing closing bracket in array access"""
    source = """func main() -> void { let x = numbers[0; }"""
    expected = "Error on line 1 col 39: ;"
    assert Parser(source).parse() == expected

def test_075():
    """Normal case: Pipeline operator"""
    source = """func main() -> void { let x = 5 >> add(3); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_076():
    """Edge case: Invalid operator"""
    source = """func main() -> void { let x = 5 @ 3; }"""
    expected = "Error Token @"
    assert Parser(source).parse() == expected

def test_077():
    """Normal case: Nested arithmetic expression"""
    source = """func main() -> void { let x = (5 + 3) * 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_078():
    """Normal case: Multi-dimensional array access"""
    source = """func main() -> void { let x = matrix[0][1]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_079():
    """Edge case: Missing argument in function call"""
    source = """func main() -> void { let x = add(5, ; }"""
    expected = "Error on line 1 col 37: ;"
    assert Parser(source).parse() == expected

def test_080():
    """Normal case: String concatenation"""
    source = """func main() -> void { let x = "Hello" + "World"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_081():
    """Normal case: Unary negation"""
    source = """func main() -> void { let x = -42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_082():
    """Edge case: Double unary operator"""
    source = """func main() -> void { let x = ++42; }"""
    expected = "success"
    assert Parser(source).parse() == expected  # Lưu ý: ++ được parser chấp nhận như +(+42)

def test_083():
    """Normal case: Logical NOT expression"""
    source = """func main() -> void { let x = !true; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_084():
    """Normal case: Complex logical expression"""
    source = """func main() -> void { let x = (a > 0) && (b < 10); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_085():
    """Edge case: Missing right operand in pipeline"""
    source = """func main() -> void { let x = 5 >> ; }"""
    expected = "Error on line 1 col 35: ;"
    assert Parser(source).parse() == expected

def test_086():
    """Normal case: Chained pipeline"""
    source = """func main() -> void { let x = data >> filter(isValid) >> map(transform); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_087():
    """Edge case: Invalid array literal"""
    source = """func main() -> void { let x = [1, 2, ; }"""
    expected = "Error on line 1 col 37: ;"
    assert Parser(source).parse() == expected

def test_088():
    """Normal case: Nested function call"""
    source = """func main() -> void { let x = add(multiply(2, 3), 4); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_089():
    """Edge case: Unclosed array literal"""
    source = """func main() -> void { let x = [1, 2; }"""
    expected = "Error on line 1 col 35: ;"
    assert Parser(source).parse() == expected

def test_090():
    """Normal case: Equality comparison"""
    source = """func main() -> void { let x = 5 == 5; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_091():
    """Normal case: Inequality comparison"""
    source = """func main() -> void { let x = 5 != 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_092():
    """Edge case: Missing parentheses in function call"""
    source = """func main() -> void { let x = add 5, 3; }"""
    expected = "Error on line 1 col 34: 5"
    assert Parser(source).parse() == expected

def test_093():
    """Normal case: Less than or equal comparison"""
    source = """func main() -> void { let x = 5 <= 10; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_094():
    """Normal case: Greater than comparison"""
    source = """func main() -> void { let x = 10 > 5; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    """Edge case: Trailing comma in function call"""
    source = """func main() -> void { let x = add(5, 3, ); }"""
    expected = "Error on line 1 col 40: )"
    assert Parser(source).parse() == expected

def test_096():
    """Normal case: Modulo operation"""
    source = """func main() -> void { let x = 15 % 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    """Edge case: Invalid index expression"""
    source = """func main() -> void { let x = numbers[; }"""
    expected = "Error on line 1 col 38: ;"
    assert Parser(source).parse() == expected

def test_098():
    """Normal case: Complex arithmetic with precedence"""
    source = """func main() -> void { let x = 2 + 3 * 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_099():
    """Normal case: Mixed operators with pipeline"""
    source = """func main() -> void { let x = (x > 0) && (data >> process); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    """Edge case: Invalid literal character"""
    source = """func main() -> void { let x = @invalid; }"""
    expected = "Error Token @"
    assert Parser(source).parse() == expected

def test_101():
    """Normal case: Unary plus expression"""
    source = """func main() -> void { let x = +42; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_102():
    """Edge case: Invalid pipeline expression"""
    source = """func main() -> void { let x = 5 >> (3); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_103():
    """Normal case: Multi-dimensional array literal"""
    source = """func main() -> void { let x = [[1, 2], [3, 4]]; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_104():
    """Normal case: Complex pipeline chain"""
    source = """func main() -> void { let x = data >> filter(isValid) >> map(transform) >> reduce(combine); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_105():
    """Edge case: Missing operator in expression"""
    source = """func main() -> void { let x = 5 3; }"""
    expected = "Error on line 1 col 32: 3"
    assert Parser(source).parse() == expected

def test_106():
    """Normal case: Boolean OR expression"""
    source = """func main() -> void { let x = true || false; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_107():
    """Edge case: Invalid array access syntax"""
    source = """func main() -> void { let x = numbers[0]]; }"""
    expected = "Error on line 1 col 40: ]"
    assert Parser(source).parse() == expected

def test_108():
    """Normal case: Parenthesized comparison"""
    source = """func main() -> void { let x = (5 < 10); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_109():
    """Worst case: Complex nested expression"""
    source = """func main() -> void { let x = (5 + (3 * 2)) >> add(4) >> multiply(2); }"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_110():
    """Normal case: Multiple constant declarations with various types"""
    source = """
        const a1 = 123;
        const a2: int = 456;
        const b1 = 3.14;
        const b2: float = 2.71;
        const c1 = true;
        const c2: bool = false;
        const d1 = "hello";
        const d2: string = "world";
        const e1 = [1, 2, 3];
        const e2: [int; 3] = [4, 5, 6];
        func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_111():
    """Edge case: Invalid initializer for nested array"""
    source = """
        const e2: [[[int; 1]; 2]; 3] = 1;
        func main() -> void {}
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_112():
    """Normal case: Array access with complex index"""
    source = """func main() -> void { let a = foo()[2][a+1]; }"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_113():
    source = "const a = [1, 2][2][2+2][3]; func main() -> void {  }"
    assert Parser(source).parse() == "success"

def test_114():
    source = "const a = (1+2)*3 + (a)[2][3]; func main() -> void {}"
    assert Parser(source).parse() == "success"
def test_115():
    source = "const a = a[1, 2]; func main() -> void { (a)(3) }"
    assert Parser(source).parse() == "Error on line 1 col 13: ,"
def test_116():
    source = "const a = str()[2][3] + 3[2]; func main() -> void {}"
    assert Parser(source).parse() == "success"
def test_117():
    source = '''
func main () -> void {
    foo()[2] = 1;
}
     '''
    assert Parser(source).parse() == "Error on line 3 col 13: ="

def test_118():
    source = '''
        func a() -> void { a[a[2]][1+2] = 1; }
     '''
    assert Parser(source).parse() == "success"