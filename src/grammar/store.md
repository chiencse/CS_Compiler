## Lexerr

### Programming code 1

IDENTIFIER : [a-z][a-z0-9]\* ;

STRING*LITERAL
: '\'' ( ~['\r\n] | '\'\'' )* '\''
;
PASCAL*STRING : ['] (~['] | [']['])*? ['] ;

REAL_LITERAL : DIGIT+ '.' DIGIT ([eE] SIGN? DIGIT+ )? | DIGIT+ [eE] SIGN? DIGIT+ | DIGIT+ '.' DIGIT+ ;

fragment DIGIT : [0-9] ;
fragment SIGN : [+-] ;

### Exercise 1 - Lexer

/\* BKNETID : STRING_LOWER+ '.' STRING_LOWER+ SUFFIX ;

fragment SUFFIX : CHAR? CHAR? CHAR? CHAR? CHAR_NO_DOT ;

fragment CHAR*NO_DOT : STRING_LOWER | DIGIT | '*' ;

fragment CHAR : STRING*LOWER | DIGIT | '.' | '*' ;

fragment STRING_LOWER : [a-z] ;

fragment DIGIT : [0-9] ;

\*/

#### 2

/\*
IPV4 : SECTION '.' SECTION '.' SECTION '.' SECTION ;

fragment SECTION : [1-9] DIGIT? DIGIT? | '0' ;

fragment DIGIT : [0-9] ;
\*/

#### 3

/_
PHP*INT
: '0' // Single zero
| DIGIT_UNZERO (('*'? DIGIT)_) // Non-zero starting digit, optional underscores between digits
{ # Build token text from digits only
digits = [c for c in self.text if c != '_']
self.\_text = ''.join(digits)
} ;

#### 4

// Fragment rules for digits
fragment DIGIT_UNZERO : [1-9] ; // Non-zero digits (1-9)
fragment DIGIT : [0-9] ;
\*/

SHEXA
: [02468] | [0-9] [0-9a-fA-F]\* [02468aAeEcC] ;

### Programming code 2

program: (vari | func)+ EOF ;

vari : typ idlist SM ;

idlist : ID CM idlist | ID ;

func : typ ID headfunc body ;

headfunc : LB params RB ;

params : paramslist | ;

paramslist : param SM paramslist | param ;

param : typ idlist ;

body : LC stmtlist RC ;

stmtlist : stmt stmtlist | ;

stmt : (assign | call | return | vari) ;

assign : ID EQUAL expr SM ;

call : ID LB exprlist RB SM | ID LB exprlist RB;

exprlist : exprprime | ;

exprprime : expr CM exprprime | expr ;

return : RETURN expr SM ;

expr : expr1 ADD expr | expr1 ;

expr1 : expr2 SUB expr2 | expr2 ;

expr2 : expr2 MUL expr3 | expr2 DIVIDE expr3 | expr3 ;

expr3 : INTLIT
| FLOATLIT
| ID
| call
| LB expr RB ;

typ : INT | FLOAT ;

INT : 'int' ;

FLOAT : 'float' ;

RETURN : 'return' ;

EQUAL : '=' ;

ADD : '+' ;

SUB : '-' ;

MUL : '\*' ;

DIVIDE : '/' ;

LB : '(' ;

RB : ')' ;

LC : '{' ;

RC : '}' ;

SM : ';' ;

CM : ',' ;

INTLIT : [0-9]+ ;

FLOATLIT : [0-9]+ '.' [0-9]\* ;

ID : [a-zA-Z]+ ;

WS : [ \t\r\n]+ -> skip ;

UNCLOSE_STRING : '"' .\*? (EOF | '\r'? '\n') {
raise UncloseString(self.text[1:])
};

ILLEGAL*ESCAPE : '"' .*? '\\' ~[btnfr"\\] .\_? '"' {
raise IllegalEscape(self.text[1:-1])
};

ERROR_CHAR : . {raise ErrorToken(self.text)} ;

# LEXER BTL

grammar HLang;

@lexer::header {
from lexererr import \*
}

@lexer::members {
def emit(self):
tk = self.type
if tk == self.UNCLOSE_STRING:  
 result = super().emit();
raise UncloseString(result.text);
elif tk == self.ILLEGAL_ESCAPE:
result = super().emit();
raise IllegalEscape(result.text);
elif tk == self.ERROR_CHAR:
result = super().emit();
raise ErrorToken(result.text);
else:
return super().emit();
}

options{
language=Python3;
}

program : EOF ;

//KEY_WORD
BOOLEAN : 'bool';
BREAK : 'break';
CONST : 'const';
CONTINUE : 'continue';
ELSE : 'else';
FALSE : 'false';
FLOAT : 'float';
FOR : 'for';
FUNC : 'func';
IF : 'if';
IN : 'in';
INT : 'int';
LET : 'let';
RETURN : 'return';
STRING : 'string';
TRUE : 'true';
VOID : 'void';
WHILE : 'while';

// OPERATOR

// Arithmetic
ADD : '+' ;
MINUS : '-' ;
MUL : '\*' ;
DIV : '/' ;
MOD : '%' ;

// Comparison
EQ : '==' ;
NEQ : '!=' ;
LT : '<' ;
LTE : '<=' ;
GT : '>' ;
GTE : '>=' ;

// Logical
AND : '&&' ;
OR : '||' ;
NOT : '!' ;

// Assignment
ASS : '=' ;

// Type annotation
COLON : ':' ;

// Function return type
ARROW : '->' ;

// Pipeline
PIPE : '>>' ;

//SEPERATORS
SEMI : ';';
COMMA : ',';
LR : '(';
RR : ')';
LC : '{';
RC : '}';
LS : '[';
RS : ']';
DOT : '.';

IDENTIFIER: [a-zA-Z_] [a-zA-Z_0-9]\* ;

//LITERAL
//Integer literals
INT_LITERAL : [0-9]+ ;

//Float literals
FLOAT_LITERAL : DIGIT+ '.' DIGIT\* EXPONENT? ;
fragment EXPONENT : [eE] [+-]? DIGIT+ ;
fragment DIGIT : [0-9] ;

// String literals
STRING_LITERAL : '"' STRING_CHAR\* '"' {
self.text = self.text[1:-1]
};
fragment STRING_CHAR : ESC_SEQ | ASCII_PRINTABLE_CHAR;
fragment ESC_SEQ : '\\n' | '\\t' | '\\r' | '\\\\' | '\\"' ;
fragment ASCII_PRINTABLE_CHAR : ~["\\\u0000-\u001F\u007F-\uFFFF] ;

// Comment
LINE*COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK*COMMENT: '/*' ( BLOCK*COMMENT | ~[/*] | '/' ~[*] | '\*' ~[/] )\_ '\*/' -> skip ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

fragment ILLEGAL_ESC_SEQ: '\\' ~[ntr"\\] ; // Identify escape sequence invalide

ILLEGAL_ESCAPE: '"' STRING_CHAR\* ILLEGAL_ESC_SEQ {
raise IllegalEscape(self.text[1:])  
};

UNCLOSE_STRING: '"' STRING_CHAR\* (EOF | '\r'? '\n' | '\r') {
raise UncloseString(self.text[1:].rstrip('\r\n'))
};
ERROR_CHAR: . {raise ErrorToken(self.text)} ; // If not match any rule
