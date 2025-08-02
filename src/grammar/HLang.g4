grammar HLang;

@lexer::header {
from lexererr import *
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

//--------------------------------LEXER------------------------------//
//KEYWORDS
BOOL: 'bool';
BREAK: 'break';
CONST: 'const';
CONTINUE: 'continue';
IF: 'if';
ELSE: 'else';
FALSE: 'false';
TRUE: 'true';
FLOAT: 'float';
FOR: 'for';
FUNC: 'func';
IN: 'in';
INT: 'int';
LET: 'let';
RETURN: 'return';
STRING: 'string';
VOID: 'void';
WHILE: 'while';

//OPERATORS
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

EQUAL: '==';
NOT_EQUAL: '!=';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';

AND: '&&';
OR: '||';
NOT: '!';

ASSIGN: '=';

ARROW: '->';
PIPELINE: '>>';

DOT: '.';

//SEPARATOR
LRB: '(';
RRB: ')';

LCB: '{';
RCB: '}';

LSB: '[';
RSB: ']';

COMMA: ',';
SEMICOLON: ';';
COLON: ':';

//IDENTIFIERS
ID: [a-zA-Z_][a-zA-Z0-9_]*;

//LITERAL
INT_LIT: HEX | BIN | OCT | DEC;
DEC: '0' | [1-9][0-9]* | '0'[0-9]+;
BIN: '0' [Bb] [01]+;
OCT: '0' [Oo] [0-7]+;
HEX: '0' [Xx] [0-9A-Fa-f]+;


fragment DIGIT: [0-9]+;
fragment EXP: [Ee] [+-]? DIGIT;
FLOAT_LIT: DIGIT [.] [0-9]* EXP?;

fragment ESCAPE_SEQUENCE:  '\\' [ntr"\\];
fragment CHAR_LIT: ~[\\"\n\t\r] | ESCAPE_SEQUENCE;
STR_LIT: '"' CHAR_LIT* '"' {
    # Remove quotes from the text
    self.text = self.text[1:-1]
};

//COMMENT, NEWLINE, WHITE SPACE

SINGLE_COMMENT: '//' ~[\r\n]* -> skip;
MULTI_COMMENT: '/*' (MULTI_COMMENT |.)*? '*/' -> skip;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

//ERROR TOKENS - Must be at the end, with ERROR_CHAR last
UNCLOSE_STRING: '"' CHAR_LIT* ('\r\n' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[1:-2] + '\r\n')
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[1:-1] + '\n')
    else:
        raise UncloseString(self.text[1:])
};

fragment ILLEGAL_CHAR: '\\' ~[ntr"\\];
ILLEGAL_ESCAPE: '"' CHAR_LIT* ILLEGAL_CHAR {
    raise IllegalEscape(self.text[1:])
};

ERROR_CHAR: . {raise ErrorToken(self.text)};

//--------------------------------PARSER------------------------------//

program: const_decl* func_decl* EOF;

// Global constant declaration
const_decl: CONST ID (COLON type_spec)? ASSIGN expression SEMICOLON;

// Function declaration  
func_decl: FUNC ID LRB parameter_list? RRB ARROW return_type LCB statement* RCB;

parameter_list: parameter (COMMA parameter)*;
parameter: ID COLON type_spec;

// Type specifications
type_spec: primitive_type 
         | array_type;

// Return type (allows void, but type_spec doesn't)
return_type: primitive_type 
           | array_type
           | VOID;

primitive_type: INT | FLOAT | BOOL | STRING;
array_type: LSB type_spec SEMICOLON INT_LIT RSB;

// Statements
statement: var_decl
         | assignment_stmt
         | if_stmt
         | while_stmt
         | for_stmt
         | return_stmt
         | break_stmt
         | continue_stmt
         | expression_stmt
         | block_stmt;

// Variable declaration (only allowed inside functions)
var_decl: LET ID (COLON type_spec)? ASSIGN expression SEMICOLON;

// Assignment statement
assignment_stmt: lvalue ASSIGN expression SEMICOLON;
lvalue: ID
      | ID array_access+;

// Control flow statements
if_stmt: IF LRB expression RRB block_stmt (ELSE IF LRB expression RRB block_stmt)* (ELSE block_stmt)?;

while_stmt: WHILE LRB expression RRB block_stmt;

for_stmt: FOR LRB ID IN expression RRB block_stmt;

return_stmt: RETURN expression? SEMICOLON;

break_stmt: BREAK SEMICOLON;

continue_stmt: CONTINUE SEMICOLON;

expression_stmt: expression SEMICOLON;

block_stmt: LCB statement* RCB;

// Expressions with precedence (lowest to highest)
expression: pipeline_expr;

pipeline_expr: logical_or_expr (PIPELINE logical_or_expr)*;

logical_or_expr: logical_and_expr (OR logical_and_expr)*;

logical_and_expr: equality_expr (AND equality_expr)*;

equality_expr: relational_expr ((EQUAL | NOT_EQUAL) relational_expr)*;

relational_expr: additive_expr ((LT | LTE | GT | GTE) additive_expr)*;

additive_expr: multiplicative_expr ((ADD | SUB) multiplicative_expr)*;

multiplicative_expr: unary_expr ((MUL | DIV | MOD) unary_expr)*;

unary_expr: (NOT | SUB | ADD) unary_expr
          | postfix_expr;

// Allow type keywords to be used as function names
type_keyword: INT | FLOAT | BOOL;

argument_list: expression (COMMA expression)*;

postfix_expr: type_keyword_func
            | ID (LRB argument_list? RRB array_access* | array_access*)
            | literal array_access*
            | LRB expression RRB array_access*;

// Type keyword function call
type_keyword_func: {self._input.LA(2) == HLangParser.LRB}? type_keyword LRB argument_list? RRB;

array_access: LSB expression RSB;

// Literals
literal: INT_LIT
       | FLOAT_LIT
       | bool_literal
       | STR_LIT
       | array_literal;

bool_literal: TRUE | FALSE;

array_literal: LSB (expression (COMMA expression)*)? RSB;