from enum import Enum, auto

class TokenType(Enum):
    # Operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    ASSIGN = auto()
    EQ = auto()    # ==
    NE = auto()    # !=
    LT = auto()    # <
    GT = auto()    # >
    LE = auto()    # <=
    GE = auto()    # >=

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    # Keywords
    MYIF = auto()
    MYELSE = auto()
    MYWHILE = auto()
    MYVAR = auto()    # Variable declaration
    MYPRINT = auto()

    # Data Types
    NUMBER = auto()     # Integer for simplicity
    STRING = auto()     # String literal
    IDENTIFIER = auto()
    MYBOOL = auto()       # mytrue/myfalse
    
    # Special
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: any, line: int = 0, column: int = 0):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, Line:{self.line}, Col:{self.column})"
