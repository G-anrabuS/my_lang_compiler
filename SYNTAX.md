# My Language Syntax

This document describes the syntax currently accepted by the compiler.

## Program Structure

A program is a sequence of statements:

```ebnf
program      = { statement } ;
```

## Statements

```ebnf
statement    = block
             | var_decl
             | assignment
             | print_stmt
             | if_stmt
             | while_stmt
             | empty_stmt ;

block        = "{" , { statement } , "}" ;
var_decl     = "myvar" , identifier , [ "=" , expr ] , ";" ;
assignment   = identifier , "=" , expr , ";" ;
print_stmt   = "myprint" , "(" , expr , ")" , ";" ;
if_stmt      = "myif" , "(" , expr , ")" , statement , [ "myelse" , statement ] ;
while_stmt   = "mywhile" , "(" , expr , ")" , statement ;
empty_stmt   = ";" ;
```

Notes:
- `if` and `while` bodies can be either one statement or a block.
- Semicolons are required for variable declarations, assignments, print statements, and empty statements.

## Expressions

```ebnf
expr         = term , { ("+" | "-" | "==" | "!=" | "<" | "<=" | ">" | ">=") , term } ;
term         = factor , { ("*" | "/") , factor } ;
factor       = ("+" | "-") , factor
             | number
             | string
             | boolean
             | identifier
             | "(" , expr , ")" ;

boolean      = "mytrue" | "myfalse" ;
```

Operator precedence (highest to lowest):
1. Unary `+` `-`
2. `*` `/`
3. `+` `-` `==` `!=` `<` `<=` `>` `>=` (same precedence, left-associative)

## Lexical Rules

```ebnf
identifier   = ( letter | "_" ) , { letter | digit | "_" } ;
number       = digit , { digit } ;
string       = '"' , { char } , '"'
             | "'" , { char } , "'" ;
comment      = "#" , { any_char_except_newline } ;
```

- Whitespace is ignored outside of strings.
- Strings support escapes: `\\n`, `\\t`, `\\r`, `\\\\`, `\\"`, `\\'`.
- Comments start with `#` and run to end of line.

## Keywords

Implemented in parsing:
- `myvar`
- `myif`
- `myelse`
- `mywhile`
- `myprint`
- `mytrue`
- `myfalse`

## Example

```txt
myvar x = 10;
myvar y = 0;

mywhile (x > 0) {
    y = y + x;
    x = x - 1;
}

myif (y >= 50) {
    myprint("sum is large");
} myelse {
    myprint("sum is small");
}

myvar done = mytrue;
myif (done) {
    myprint("done");
}

myprint(y);
```
