from utils import Tokenizer

# Character Set Tests (Unchanged)
def test_001():
    """Normal case: ASCII letters and digits in identifier"""
    source = "myVar123"
    expected = "myVar123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    """Edge case: Single ASCII letter identifier"""
    source = "x"
    expected = "x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_003():
    """Worst case: Long identifier with mixed ASCII letters, digits, underscores"""
    source = "a_very_long_identifier_1234567890"
    expected = "a_very_long_identifier_1234567890,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    """Edge case: Identifier starting with underscore"""
    source = "_hidden"
    expected = "_hidden,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Normal case: Whitespace (space, tab, newline) ignored"""
    source = "let  x\t=\n42;"
    expected = "let,x,=,42,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Edge case: Multiple whitespace types (CRLF, LF, CR)"""
    source = "x\r\ny\rz\n"
    expected = "x,y,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    """Worst case: Non-ASCII character in identifier"""
    source = "café"
    expected = "caf,Error Token é"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    """Edge case: Empty source file"""
    source = ""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    """Normal case: Printable ASCII symbols in string"""
    source = '"!@#$%^&*()"'
    expected = "!@#$%^&*(),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010():
    """Worst case: Non-ASCII character in string"""
    source = '"Cafe"'
    expected = "Cafe,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Comment Tests (Unchanged)
def test_011():
    """Normal case: Single-line comment"""
    source = "// This is a comment"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    """Edge case: Empty line comment"""
    source = "//"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    """Normal case: Block comment single line"""
    source = "/* Comment */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Normal case: Multi-line block comment"""
    source = "/* Line 1\nLine 2 */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """Edge case: Nested block comments"""
    source = "/* Outer /* Inner */ */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """Worst case: Deeply nested block comments"""
    source = "/* 1 /* 2 /* 3 /* 4 */ */ */ */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Edge case: Line comment with code"""
    source = "let x = 42; // Comment"
    expected = "let,x,=,42,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """Normal case: Multiple line comments"""
    source = "// Comment 1\n// Comment 2"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """Edge case: Block comment with code-like content"""
    source = "/* let x = 42; */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """Worst case: Unclosed block comment"""
    source = "/* Comment"
    expected = "/,*,Comment,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Identifier Tests (Unchanged)
def test_021():
    """Normal case: Basic identifier"""
    source = "hello"
    expected = "hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Normal case: Identifier with digits"""
    source = "myVar123"
    expected = "myVar123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Edge case: Identifier starting with underscore"""
    source = "_value"
    expected = "_value,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Worst case: Long identifier with underscores and digits"""
    source = "this_is_a_very_long_identifier_1234567890"
    expected = "this_is_a_very_long_identifier_1234567890,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Edge case: Single letter identifier"""
    source = "x"
    expected = "x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Normal case: Mixed case identifier"""
    source = "MyVar"
    expected = "MyVar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Edge case: Identifier resembling keyword"""
    source = "iffy"
    expected = "iffy,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """Worst case: Identifier with keyword prefix"""
    source = "interface"
    expected = "interface,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """Normal case: Multiple identifiers"""
    source = "x y z"
    expected = "x,y,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """Edge case: Identifier with underscore only"""
    source = "____"
    expected = "____,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Keyword Tests (Unchanged)
def test_031():
    """Normal case: Single keyword"""
    source = "bool"
    expected = "bool,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Normal case: Multiple keywords"""
    source = "if else while"
    expected = "if,else,while,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Edge case: Keyword 'true'"""
    source = "true"
    expected = "true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Edge case: Keyword 'false'"""
    source = "false"
    expected = "false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Normal case: Keywords in code context"""
    source = "let x: int = 42;"
    expected = "let,x,:,int,=,42,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Edge case: Keywords in sequence"""
    source = "func for if else"
    expected = "func,for,if,else,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Worst case: Case-sensitivity test (invalid keyword)"""
    source = "BOOL"
    expected = "BOOL,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Edge case: Keyword 'void'"""
    source = "void"
    expected = "void,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Normal case: Keywords with identifiers"""
    source = "let var = true;"
    expected = "let,var,=,true,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Worst case: All keywords in sequence"""
    source = "bool break const continue else false float for func if in int let return string true void while"
    expected = "bool,break,const,continue,else,false,float,for,func,if,in,int,let,return,string,true,void,while,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Operator Tests (Unchanged)
def test_041():
    """Normal case: Arithmetic operators"""
    source = "+ - * / %"
    expected = "+,-,*,/,%,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Normal case: Comparison operators"""
    source = "== != < <= > >="
    expected = "==,!=,<,<=,>,>=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Normal case: Logical operators"""
    source = "&& || !"
    expected = "&&,||,!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """Edge case: Assignment operator"""
    source = "="
    expected = "=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Edge case: Pipeline operator"""
    source = ">>"
    expected = ">>,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Normal case: Operators in expression"""
    source = "x + y * z == 42"
    expected = "x,+,y,*,z,==,42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Edge case: Type annotation and function return"""
    source = "x: int -> void"
    expected = "x,:,int,->,void,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Worst case: Repeated operators"""
    source = "++ -- ** / / % %"
    expected = "+,+,-,-,*,*,/,/,%,%,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Edge case: Logical operators with booleans"""
    source = "!true && false"
    expected = "!,true,&&,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """Worst case: Mixed operators with spaces"""
    source = " +  ==  &&  >>  :  -> "
    expected = "+,==,&&,>>,:,->,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Separator Tests (Unchanged)
def test_051():
    """Normal case: Basic separators"""
    source = "; , ( ) { } [ ] ."
    expected = ";,,,(,),{,},[,],.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Edge case: Single separator"""
    source = ";"
    expected = ";,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Normal case: Separators in code context"""
    source = "func f(x, y: int) { x.y; }"
    expected = "func,f,(,x,,,y,:,int,),{,x,.,y,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Edge case: Nested parentheses"""
    source = "(())"
    expected = "(,(,),),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Edge case: Nested braces"""
    source = "{{}}"
    expected = "{,{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Edge case: Nested brackets"""
    source = "[[]]"
    expected = "[,[,],],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Worst case: Complex nested separators"""
    source = "{[()]}"
    expected = "{,[,(,),],},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """Normal case: Separators with whitespace"""
    source = " ;  ,  (  ) "
    expected = ";,,,(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """Edge case: Single dot separator"""
    source = "."
    expected = ".,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Worst case: Separators in dense code"""
    source = "x.y[z](a,b);"
    expected = "x,.,y,[,z,],(,a,,,b,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Integer Literal Tests (Unchanged)
def test_061():
    """Normal case: Positive integer"""
    source = "42"
    expected = "42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Edge case: Negative integer"""
    source = "-17"
    expected = "-,17,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Edge case: Zero"""
    source = "0"
    expected = "0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Normal case: Multiple integers"""
    source = "1 2 3"
    expected = "1,2,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Edge case: Leading zeros"""
    source = "007"
    expected = "007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Worst case: Large integer (within 32-bit signed range)"""
    source = "2147483647"
    expected = "2147483647,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Worst case: Negative large integer"""
    source = "-2147483648"
    expected = "-,2147483648,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """Normal case: Integer in expression"""
    source = "5 + 3"
    expected = "5,+,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Edge case: Integer with spaces"""
    source = " 42  0 "
    expected = "42,0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Edge case: Zero with minus"""
    source = "-0"
    expected = "-,0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Float Literal Tests (Unchanged)
def test_071():
    """Normal case: Basic float"""
    source = "3.14"
    expected = "3.14,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    """Edge case: Negative float"""
    source = "-2.5"
    expected = "-,2.5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Edge case: Zero float"""
    source = "0.0"
    expected = "0.0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """Normal case: Float with exponent"""
    source = "1.23e4"
    expected = "1.23e4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Edge case: Negative float with exponent"""
    source = "-5.67e-2"
    expected = "-,5.67e-2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Edge case: Float with no decimal digits"""
    source = "42."
    expected = "42.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """Edge case: Float with only decimal part"""
    source = ".5"
    expected = ".,5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Worst case: Large float with exponent"""
    source = "1.7976931348623157e308"
    expected = "1.7976931348623157e308,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Normal case: Multiple floats"""
    source = "1.1 2.2 3.3"
    expected = "1.1,2.2,3.3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Edge case: Float with uppercase exponent"""
    source = "4.56E-3"
    expected = "4.56E-3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Boolean Literal Tests (Unchanged)
def test_081():
    """Normal case: True boolean"""
    source = "true"
    expected = "true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Normal case: False boolean"""
    source = "false"
    expected = "false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Edge case: Boolean in expression"""
    source = "true && false"
    expected = "true,&&,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Edge case: Boolean with spaces"""
    source = " true  false "
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Worst case: Case-sensitivity test for boolean"""
    source = "TRUE"
    expected = "TRUE,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Edge case: Boolean in code context"""
    source = "let b = true;"
    expected = "let,b,=,true,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    """Normal case: Multiple booleans"""
    source = "true false true"
    expected = "true,false,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_088():
    """Edge case: Boolean with logical operator"""
    source = "!false"
    expected = "!,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    """Worst case: Boolean-like identifier"""
    source = "truee"
    expected = "truee,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    """Edge case: Boolean in comparison"""
    source = "true == false"
    expected = "true,==,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# String Literal Tests (Unchanged)
def test_091():
    """Normal case: Basic string"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Edge case: Empty string"""
    source = '""'
    expected = ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Normal case: String with escape sequences"""
    source = '"Line 1\\nLine 2"'
    expected = "Line 1\\nLine 2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Edge case: String with quote escape"""
    source = '"Quote: \\"text\\""'
    expected = 'Quote: \\"text\\",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Edge case: String with backslash escape"""
    source = '"Path: C:\\\\folder"'
    expected = "Path: C:\\\\folder,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Normal case: String with special characters"""
    source = '"!@#$%^&*()"'
    expected = "!@#$%^&*(),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Edge case: String with tab escape"""
    source = '"Tab:\\tEnd"'
    expected = "Tab:\\tEnd,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Worst case: Long string with multiple escapes"""
    source = '"Very long string with \\n\\t\\r\\\\\\""'
    expected = "Very long string with \\n\\t\\r\\\\\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Normal case: Multiple strings"""
    source = '"abc" "def"'
    expected = "abc,def,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    """Edge case: String with spaces"""
    source = '"  spaces  "'
    expected = "  spaces  ,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Illegal Escape Sequence Tests (Updated)
def test_101():
    """Normal case: Illegal escape sequence"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_102():
    """Edge case: Single illegal escape"""
    source = '"\\z"'
    expected = "Illegal Escape In String: \\z"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_103():
    """Edge case: Illegal escape at start"""
    source = '"\\qabc"'
    expected = "Illegal Escape In String: \\q"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_104():
    """Edge case: Illegal escape at end"""
    source = '"abc\\p"'
    expected = "Illegal Escape In String: abc\\p"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_105():
    """Worst case: Multiple illegal escapes"""
    source = '"\\x\\y\\z"'
    expected = "Illegal Escape In String: \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_106():
    """Normal case: Illegal escape with valid escape"""
    source = '"\\n\\x"'
    expected = "Illegal Escape In String: \\n\\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_107():
    """Edge case: Illegal escape in long string"""
    source = '"This is a long \\k string"'
    expected = "Illegal Escape In String: This is a long \\k"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_108():
    """Edge case: Illegal escape with special chars"""
    source = '"@#\\$%"'
    expected = "Illegal Escape In String: @#\\$"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_109():
    """Edge case: Single illegal escape character"""
    source = '"\\w"'
    expected = "Illegal Escape In String: \\w"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_110():
    """Worst case: Illegal escape with spaces"""
    source = '" \\x "'
    expected = "Illegal Escape In String:  \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Unclosed String Tests (Unchanged, as content up to error point is correct)
def test_111():
    """Normal case: Unclosed string with EOF"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_112():
    """Edge case: Unclosed string with newline"""
    source = '"Hello\nWorld'
    expected = "Unclosed String: Hello\n"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_113():
    """Edge case: Unclosed string with carriage return"""
    source = '"Hello\rWorld'
    expected = "Unclosed String: Hello\r"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_114():
    """Edge case: Empty unclosed string"""
    source = '"'
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_115():
    """Normal case: Unclosed string with escape"""
    source = '"Test \\n'
    expected = "Unclosed String: Test \\n"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_116():
    """Edge case: Unclosed string with spaces"""
    source = '"   '
    expected = "Unclosed String:    "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_117():
    """Normal case: Unclosed string in code"""
    source = 'let s = "test'
    expected = "let,s,=,Unclosed String: test"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_118():
    """Edge case: Unclosed string with special chars"""
    source = '"@#$'
    expected = "Unclosed String: @#$"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_119():
    """Worst case: Unclosed string with newline and code"""
    source = '"Hello\nint x'
    expected = "Unclosed String: Hello\n"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_120():
    """Edge case: Unclosed string with multiple lines"""
    source = '"Line 1\nLine 2'
    expected = "Unclosed String: Line 1\n"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Error Character Tests (Updated for clarity, but mostly unchanged)
def test_121():
    """Normal case: Single non-ASCII character"""
    source = "€"
    expected = "Error Token €"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_122():
    """Edge case: Multiple non-ASCII characters"""
    source = "€£¥"
    expected = "Error Token €"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_123():
    """Normal case: Error character in code"""
    source = "int x = 5; @"
    expected = "int,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_124():
    """Edge case: Error character with spaces"""
    source = " @ # "
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_126():
    """Normal case: Error character after number"""
    source = "42 #"
    expected = "42,Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_127():
    """Edge case: Error character in expression"""
    source = "5 + @"
    expected = "5,+,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_128():
    """Worst case: Multiple error characters in code"""
    source = "let x = 5; @#€"
    expected = "let,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_129():
    """Edge case: Error character between keywords"""
    source = "if @ else"
    expected = "if,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_130():
    """Edge case: Error character at start"""
    source = "# x = 5"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_131():
    """Test unterminated nested comment"""
    source = "let x = 5; /* outer /* inner */ still outer x = 10;"
    expected = "let,x,=,5,;,still,outer,x,=,10,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_132():
    """Test unterminated nested comment"""
    source = "42=x;"
    expected = "42,=,x,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

