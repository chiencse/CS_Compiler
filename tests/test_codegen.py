from src.utils.nodes import *

from utils import CodeGenerator


# def test_001():
#     source = """
# func main() -> void {
#     print("Hello World");
# }
# """
#     expected = "Hello World"
#     assert CodeGenerator().generate_and_run(source) == expected
# def test_002():
#     source = """
# func main() -> void {
#     print(int2str(1));
# }
# """
#     expected = "1"
#     assert CodeGenerator().generate_and_run(source) == expected
# def test_009():
#     source = """
# func main() -> void {
#     let i: float = 1.0 - 2;
#     print(float2str(i));
# }
# """
#     expected = "-1.0"
#     assert CodeGenerator().generate_and_run(source) == expected
# def test_012():
#     source = """
# func main() -> void {
#     let i: int = 3 / 2;
#     print(int2str(i));
# }
# """
#     expected = "1"
#     assert CodeGenerator().generate_and_run(source) == expected
# def test_013():
#     source = """
# func main() -> void {
#     print(bool2str("s1" != "s1"));
# }
# """
#     expected = "false"
#     assert CodeGenerator().generate_and_run(source) == expected
def test_001():
    """Test simple string literal with print."""
    source = """
func main() -> void {
    print("Hello World");
}
"""
    expected = "Hello World"
    assert CodeGenerator().generate_and_run(source) == expected

def test_002():
    """Test integer literal with int2str."""
    source = """
func main() -> void {
    print(int2str(42));
}
"""
    expected = "42"
    assert CodeGenerator().generate_and_run(source) == expected

def test_003():
    """Test negative integer literal."""
    source = """
func main() -> void {
    print(int2str(-17));
}
"""
    expected = "-17"
    assert CodeGenerator().generate_and_run(source) == expected

def test_004():
    """Test float literal with float2str."""
    source = """
func main() -> void {
    print(float2str(3.14));
}
"""
    expected = "3.14"
    assert CodeGenerator().generate_and_run(source) == expected

def test_005():
    """Test float literal with exponent."""
    source = """
func main() -> void {
    print(float2str(1.23e2));
}
"""
    expected = "123.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_006():
    """Test boolean true literal with bool2str."""
    source = """
func main() -> void {
    print(bool2str(true));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_007():
    """Test boolean false literal with bool2str."""
    source = """
func main() -> void {
    print(bool2str(false));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_008():
    """Test empty string literal."""
    source = """
func main() -> void {
    print("");
}
"""
    expected = ""
    assert CodeGenerator().generate_and_run(source) == expected

def test_009():
    """Test string literal with escape sequence."""
    source = """
func main() -> void {
    print("Line\\nBreak");
}
"""
    expected = "Line\nBreak"
    assert CodeGenerator().generate_and_run(source) == expected

def test_010():
    """Test array literal with integers."""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    print(int2str(arr[0]));
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected
def test_011():
    """Test array literal with floats."""
    source = """
func main() -> void {
    let arr: [float; 2] = [1.5, 2.5];
    print(float2str(arr[1]));
}
"""
    expected = "2.5"
    assert CodeGenerator().generate_and_run(source) == expected
def test_012():
    """Test array literal with strings."""
    source = """
func main() -> void {
    let arr: [string; 2] = ["hello", "world"];
    print(arr[0]);
}
"""
    expected = "hello"
    assert CodeGenerator().generate_and_run(source) == expected
def test_013():
    """Test array literal of int arrays."""
    source = """
func main() -> void {
    let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
    print(int2str(arr[1][0]));
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected
def test_018():
        source = """
    func main() -> void {
        print(bool2str(2 != 1.0));
    }
    """
        expected = "true"
        assert CodeGenerator().generate_and_run(source) == expected
def test_019():
    """Test array of string arrays."""
    source = """
func main() -> void {
    let arr: [[string; 2]; 2] = [["a", "b"], ["c", "d"]];
    print(arr[1][0]);
}
"""
    expected = "c"
    assert CodeGenerator().generate_and_run(source) == expected

def test_019b():
    """Unary minus with integer."""
    source = """
func main() -> void {
    let x: int = -10;
    print(int2str(x));
}
"""
    expected = "-10"
    assert CodeGenerator().generate_and_run(source) == expected


def test_020():
    """Unary minus with float."""
    source = """
func main() -> void {
    let y: float = -3.14;
    print(float2str(y));
}
"""
    expected = "-3.14"
    assert CodeGenerator().generate_and_run(source) == expected


def test_021():
    """Unary plus with integer (should keep same value)."""
    source = """
func main() -> void {
    let x: int = +42;
    print(int2str(x));
}
"""
    expected = "42"
    assert CodeGenerator().generate_and_run(source) == expected


def test_022():
    """Unary plus with float (should keep same value)."""
    source = """
func main() -> void {
    let y: float = +1.23;
    print(float2str(y));
}
"""
    expected = "1.23"
    assert CodeGenerator().generate_and_run(source) == expected


def test_023():
    """Unary not with boolean false."""
    source = """
func main() -> void {
    let b: bool = 1 + 2;
    print(bool2str(b));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected


def test_024():
    """Unary not with boolean true."""
    source = """
func main() -> void {
    let b: bool = !true;
    print(bool2str(b));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected


def test_025():
    """Nested unary minus."""
    source = """
func main() -> void {
    let x: int = --10;
    print(int2str(x));
}
"""
    expected = "10"
    assert CodeGenerator().generate_and_run(source) == expected


def test_026():
    """Unary not with expression (false == false) => true => !true => false."""
    source = """
func main() -> void {
    let b : bool = !(false == false);
    print(bool2str(b));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected


def test_027():
    """Unary minus with expression."""
    source = """
func main() -> void {
    print(int2str(-(2 + 3)));
}
"""
    expected = "-5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_028():
    """Unary plus with variable."""
    source = """
func main() -> void {
    let x: float = 2.5;
    let y: float = +x;
    print(float2str(y));
}
"""
    expected = "2.5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_029():
    """Unary not with expression (false == false) => true => !true => false."""
    source = """
func main() -> void {
    print(bool2str(false && false));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected
def test_029a():
    """false && false => false"""
    source = """
func main() -> void {
    print(bool2str(false && false));
}
"""
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected


def test_030():
    """true || false => true"""
    source = """
func main() -> void {
    print(bool2str(true || false));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_031():
    """2 + 3 = 5"""
    source = """
func main() -> void {
    print(int2str(2 + 3));
}
"""
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_032():
    """5 - 2 = 3"""
    source = """
func main() -> void {
    print(int2str(5 - 2));
}
"""
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_033():
    """3 * 4 = 12"""
    source = """
func main() -> void {
    print(int2str(3 * 4));
}
"""
    expected = "12"
    assert CodeGenerator().generate_and_run(source) == expected


def test_034():
    """10 / 2 = 5"""
    source = """
func main() -> void {
    print(int2str(10 / 2));
}
"""
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_035():
    """10 % 3 = 1"""
    source = """
func main() -> void {
    print(int2str(10 % 3));
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected
def test_036():
    """5 + 2.5 = 7.5"""
    source = """
func main() -> void {
    print(float2str(5 + 2.5));
}
"""
    expected = "7.5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_037():
    """4 * 2.0 = 8.0"""
    source = """
func main() -> void {
    print(float2str(4 * 2.0));
}
"""
    expected = "8.0"
    assert CodeGenerator().generate_and_run(source) == expected
def test_038():
    """'Hello' + 'World' = HelloWorld"""
    source = """
func main() -> void {
    print("Hello" + "World");
}
"""
    expected = "HelloWorld"
    assert CodeGenerator().generate_and_run(source) == expected


def test_039():
    """'A' + 1 = A1 (int2str gets called)"""
    source = """
func main() -> void {
    print("A" + 1);
}
"""
    expected = "A1"
    assert CodeGenerator().generate_and_run(source) == expected
def test_040():
    """5 < 10 => true"""
    source = """
func main() -> void {
    print(bool2str(5 < 10));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected


def test_041():
    """10 == 10 => true"""
    source = """
func main() -> void {
    print(bool2str(10 == 10));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected


def test_042():
    """'abc' == 'abc' => true"""
    source = """
func main() -> void {
    print(bool2str("abc" == "abc"));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected


def test_043():
    """'abc' != 'def' => true"""
    source = """
func main() -> void {
    print(bool2str("abc" != "def"));
}
"""
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_044():
    source = """
func main() -> void {
    let arr: [int; 3]  = [42, 43, 44];
    for (x in arr) {
        if (x == 43) {
            continue;  
        }
        print(int2str(x));
    }
}
"""
    expected = "42\n44"
    assert CodeGenerator().generate_and_run(source) == expected
def test_045():
    source = """
func main() -> void {
    let x: int = 20;
    if (x < 5) {
        print("Small");
    } else if (x < 15) {
        print("Medium");
    } else if (x < 20) {
        print("Large");
    } else {
        print("Extra Large");
    }
}
"""
    expected = "Extra Large"
    assert CodeGenerator().generate_and_run(source) == expected
def test_046():
    source = """
func main() -> void {
    let i: int = 0;
    while (i < 4) {
        i = i + 1;
        if (i == 2) {
            continue;
        }
        print(int2str(i));
    }
}
"""
    expected = "1\n3\n4"
    assert CodeGenerator().generate_and_run(source) == expected
def test_047():
    source = """
func main() -> void {
    let i: int = 0;
    while (true) {
        if (i == 3) {
            break;
        }
        print(int2str(i));
        i = i + 1;
    }
}
"""
    expected = "0\n1\n2"
    assert CodeGenerator().generate_and_run(source) == expected
def test_048():
    source = """
func main() -> void {
    let i: int = 0;
    while (i < 2) {
        let j: int = 0;
        while (j < 2) {
            print(int2str(i));
            print(int2str(j));
            j = j + 1;
        }
        i = i + 1;
    }
}
"""
    expected = "0\n0\n0\n1\n1\n0\n1\n1"
    assert CodeGenerator().generate_and_run(source) == expected
def test_049():
    source = """
func main() -> void {
    let i: int = 0;
    let total: int = 0;
    while (i < 5 && total < 6) {
        total = total + i;
        print(int2str(total));
        i = i + 1;
    }
}
"""
    expected = "0\n1\n3\n6"
    assert CodeGenerator().generate_and_run(source) == expected

def test_050():
    """Test array of string arrays."""
    source = """
func main() -> void {
    let arr: [[string; 2]; 2] = [["a", "b"], ["c", "d"]];
    arr[1][0] = "cd";
    print(arr[1][0]);
}
"""
    expected = "cd"
    assert CodeGenerator().generate_and_run(source) == expected
def test_082():
    source = """
func main() -> void {
    let array = [10, 20];
    for (a in array){
        print("" + a);
        continue;
        print("" + a);
    }
}
"""
    expected = "10\n20"
    assert CodeGenerator().generate_and_run(source) == expected
def test_096():
        source = """
    func bubble_sort(arr: [int; 5]) -> void {
        for (i in [0, 1, 2, 3, 4]) {
            for (j in [0, 1, 2, 3]) {
                if (arr[j] > arr[j + 1]) {
                    let temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    func main() -> void {
        let numbers = [5, 2, 4, 1, 3];
        bubble_sort(numbers);
        for (x in numbers) {
            print(int2str(x));
        }
    }
    """
        expected = "1\n2\n3\n4\n5"
        assert CodeGenerator().generate_and_run(source) == expected

def test_042a():
        source = """
    func main() -> void {
        let a: [[int;2];3] = [[1, 2], [3, 4], [3, 4]];
        print(int2str(len(a)));
        print(int2str(len(a[0])));
    }
    """
        expected = "3\n2"
        assert CodeGenerator().generate_and_run(source) == expected
def test_048a():
        source = """
    func main() -> void {
        let a: [[int;2];3] = [[1, 2], [3, 4], [5, 6]];
        a[0] = a[1];
        print("" + a[0][0] + a[0][1]);
    }
    """
        expected = "34"
        assert CodeGenerator().generate_and_run(source) == expected
def test_037a():
        source = """
    func main() -> void {
        let a: [bool;2] = [false, true];
        print(bool2str(a[0] || a[1]));
    }
    """
        expected = "true"
        assert CodeGenerator().generate_and_run(source) == expected
def test_043a():
        source = """
    func main() -> void {
        print("s" + 1);
        print("s" + 1.0);
        print("s" + true);
        print("s" + "s");
    }
    """
        expected = "s1\ns1.0\nstrue\nss"
        assert CodeGenerator().generate_and_run(source) == expected
def test_056a():
        source = """
    func foo() -> int {
        return 1;
    }
    func main() -> void {
        print("" + foo());
    }
    """
        expected = "1"
        assert CodeGenerator().generate_and_run(source) == expected

def test_058a():
    source = """
    func main() -> void {
        let a: [int;3] = [1,2,3];
        let sum: int = foo(a, 2);
        print("" + a[0] + sum);
    }
    
    func foo(arr: [int; 3], value: int) -> int {
        arr[0] = value;
        arr[1] = value * 2;
        arr[2] = value * 3;
        return arr[0] + arr[1] + arr[2];
    }
    
    """
    expected = "212"
    assert CodeGenerator().generate_and_run(source) == expected
def test_062a():
        source = """
    const a = [1, 2, 3];
    const b = a[a[1]] ;
    
    func main() -> void {
        print("" + b);
    }
    """
        expected = "3"
        assert CodeGenerator().generate_and_run(source) == expected
def test_090():
        source = """
    func main() -> void {
        let a = 0;
        while(a <= 5){
            if (a == 0) {print("0");}
            else if (a == 1) {print("1");}
            else {print("2");}
            a = a + 1;
        }
    }
    """
        expected = "0\n1\n2\n2\n2\n2"
        assert CodeGenerator().generate_and_run(source) == expected
def test_100():
        source = """
    func main() -> void {
        let a = 10;
        let b = 3;
        let c = 5;
        let d = 2;
    
        let result1 = a + b * c - d / b + a % d;  // 10 + 3*5 - 2/3 + 10%2
    
        let cmp1 = a > b && b < c || d == 2;     // true && true || true
        let cmp2 = !(a <= c || b != 3);          // !(false || false)
    
        let complex = ((a + b) > (c * d)) && ((a % d) == 0) || !(b < d);
    
        print("result1: " + (result1));
        print("cmp1: " + (cmp1));
        print("cmp2: " + (cmp2));
        print("complex: " + (complex));
    
        if (result1 > 20 && complex) {
            print("OK1");
        }
    
        if (cmp1 && !cmp2 || result1 < 50) {
            print("OK2");
        }
    }
    """
        expected = (
            "result1: 25\n"
            "cmp1: true\n"
            "cmp2: true\n"
            "complex: true\n"
            "OK1\n"
            "OK2"
        )
        assert CodeGenerator().generate_and_run(source) == expected
def test_deep_copy_static_to_local():
    source = """
const a = [1, 2, 3];
func main() -> void {
    let b = a;
    b[0] = 10;
    print("" + a[0]);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_deep_copy_static_to_static():
    source = """
const a = [1, 2, 3];
const b = a;
func main() -> void {
    b[0] = 10;
    print("" + a[0]);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_deep_copy_nested_array():
    source = """
const a = [[1, 2], [3, 4]];
func main() -> void {
    let b = a;
    b[0][0] = 10;
    print("" + a[0][0]);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_deep_copy_string_array():
    source = """
const a = ["x", "y"];
func main() -> void {
    let b = a;
    b[0] = "z";
    print("" + a[0]);
}
"""
    expected = "x"
    assert CodeGenerator().generate_and_run(source) == expected

def test_no_deep_copy_array_literal():
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let b = a;
    b[0] = 10;
    print("" + a[0]);
}
"""
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected
