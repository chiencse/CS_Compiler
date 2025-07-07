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


program : constdecl* funcdecl* EOF ;

//decl : vardecl SM;
// Variable Declare
//vardecl : (LET | CONST) IDENTIFIER typ_anno ASS expr ;

constdecl : CONST IDENTIFIER typ_anno ASS expr SM ;
vardecl : LET IDENTIFIER typ_anno ASS expr ;

typ_anno : COLON typ | ;

typ : INT | FLOAT | BOOL | STRING | array_type;
array_type : LS typ SM INT_LITERAL RS ;

// Function Declare
funcdecl : FUNC IDENTIFIER LR paramlist RR ARROW return_typ body ;
return_typ : typ | VOID ;
paramlist : params | ;
params : param CM params | param ;
param : IDENTIFIER COLON typ ;

body : LC stmtlist RC ;
stmtlist : stmt stmtlist | ; // Is body can empty ????
stmt : vardecl SM  | expr SM | return SM | assign_stmt SM | condition_stmt 
    | while_stmt | for_stmt |block_statement | break_stmt SM| continue_stmt SM;

break_stmt : BREAK;
continue_stmt : CONTINUE ;
assign_stmt : lvalue ASS expr;
lvalue : IDENTIFIER multi_access  | IDENTIFIER  ;

condition_stmt : IF LR expr RR body elif_list else_part ;
elif_list : ELSE IF LR expr RR body elif_list | ;
else_part : ELSE body | ;

while_stmt : WHILE LR expr RR body ;
for_stmt : FOR LR IDENTIFIER IN expr RR body ;

block_statement : LC stmtlist RC ;

return : RETURN (expr | )  ;

//Expression
literal
    : INT_LITERAL 
    | FLOAT_LITERAL 
    | TRUE 
    | FALSE 
    | STRING_LITERAL 
    | array_literal
    ;
array_literal : LS arg_list RS ;
//mutilaccess_array
array_access : (IDENTIFIER | func_call | LR expr RR | literal) multi_access ;
multi_access : index_access multi_access | index_access;
index_access : LS expr RS ;
 //function call

func_call: (IDENTIFIER | INT | FLOAT ) LR arg_list RR ;

arg_list : args | ;
args: expr CM args | expr;

//expr
expr    : expr PIPE expr1 | expr1 ;
expr1   : expr1 OR expr2 | expr2 ;
expr2   : expr2 AND expr3 | expr3 ;
expr3   : expr3 (EQ | NEQ) expr4 | expr4 ;
expr4   : expr4 (LT | LTE | GT | GTE) expr5 | expr5 ;
expr5   : expr5 (ADD | MINUS) expr6 | expr6 ;
expr6   : expr6 (MUL | DIV | MOD) expr7 | expr7 ;
expr7   : (NOT | MINUS | ADD) expr7 | expr8 ;
expr8   : (LR expr RR ) | expr9 ;
expr9   : IDENTIFIER | func_call  | literal | array_access;
//TOKEN
//KEY_WORD
BOOL : 'bool';
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
MUL : '*' ;
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
SM : ';';
CM : ',';
LR : '(';
RR : ')';
LC : '{';
RC : '}';
LS : '[';
RS : ']';
DOT : '.';

IDENTIFIER: [a-zA-Z_] [a-zA-Z_0-9]* ;
BOOL_LIT : TRUE | FALSE ;


//LITERAL
//Integer literals
INT_LITERAL : [0-9]+ ;

//Float literals
FLOAT_LITERAL : DIGIT+ '.' DIGIT* EXPONENT? ;
fragment EXPONENT : [eE] [+-]? DIGIT+ ;
fragment DIGIT : [0-9] ;

// String literals
STRING_LITERAL : '"' STRING_CHAR* '"' {
    self.text = self.text[1:-1]
};

fragment STRING_CHAR : ESC_SEQ | ASCII_PRINTABLE_CHAR;
fragment ESC_SEQ : '\\n' | '\\t' | '\\r' | '\\\\' | '\\"' ;
fragment ASCII_PRINTABLE_CHAR : ~["\\\u0000-\u001F\u007F-\uFFFF] ;

// Comment
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT: '/*' (BLOCK_COMMENT |.)*? '*/' -> skip;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

fragment ILLEGAL_ESC_SEQ: '\\' ~[ntr"\\] ; // Identify escape sequence invalide

ILLEGAL_ESCAPE: '"' STRING_CHAR* ILLEGAL_ESC_SEQ {
    raise IllegalEscape(self.text[1:])  
};

UNCLOSE_STRING: '"' STRING_CHAR* (EOF | '\r'? '\n' | '\r') {
    raise UncloseString(self.text[1:])
};
ERROR_CHAR: . {raise ErrorToken(self.text)} ; // If not match any rule
