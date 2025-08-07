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


# def test_026():
#     """Unary not with expression (false == false) => true => !true => false."""
#     source = """
# func main() -> void {
#     let b : bool = !(false == false);
#     print(bool2str(b));
# }
# """
#     expected = "false"
#     assert CodeGenerator().generate_and_run(source) == expected


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
# def test_048():
#     source = """
# func main() -> void {
#     let i: int = 0;
#     while (i < 2) {
#         let j: int = 0;
#         while (j < 2) {
#             print(int2str(i));
#             print(int2str(j));
#             j = j + 1;
#         }
#         i = i + 1;
#     }
# }
# """
#     expected = "0\n0\n1\n1\n1\n1\n1\n1\n"
#     assert CodeGenerator().generate_and_run(source) == expected
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