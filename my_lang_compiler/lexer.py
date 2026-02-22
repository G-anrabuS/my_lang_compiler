from .tokens import Token, TokenType

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if self.source else None
        
        # Keywords map
        self.keywords = {
            "myif": TokenType.MYIF,
            "myelse": TokenType.MYELSE,
            "mywhile": TokenType.MYWHILE,
            "myvar": TokenType.MYVAR,
            "myprint": TokenType.MYPRINT,
            "mytrue": TokenType.MYBOOL,
            "myfalse": TokenType.MYBOOL
        }

    def error(self):
        raise Exception(f"Invalid character '{self.current_char}' at line {self.line}, column {self.column}")

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        
        self.pos += 1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
            self.column += 1

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance() # Skip the newline

    def number(self):
        result = ""
        start_col = self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return Token(TokenType.NUMBER, int(result), self.line, start_col)

    def string(self):
        quote_char = self.current_char
        start_col = self.column
        self.advance()  # Skip opening quote

        result = ""
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    break
                escape_map = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'",
                }
                result += escape_map.get(self.current_char, self.current_char)
                self.advance()
                continue

            if self.current_char == '\n':
                raise Exception(f"Unterminated string literal at line {self.line}, column {start_col}")

            result += self.current_char
            self.advance()

        if self.current_char != quote_char:
            raise Exception(f"Unterminated string literal at line {self.line}, column {start_col}")

        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result, self.line, start_col)

    def identifier(self):
        result = ""
        start_col = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if keyword
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        # Handle boolean literals specifically if needed, but here simple mapping works
        val = result
        if token_type == TokenType.MYBOOL:
            val = (result == "mytrue")
            
        return Token(token_type, val, self.line, start_col)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char in ('"', "'"):
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Multi-character operators
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, self.column)
                self.advance()
                return Token(TokenType.ASSIGN, '=', self.line, self.column)
            
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.NE, '!=', self.line, self.column)
                self.error()

            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LE, '<=', self.line, self.column)
                self.advance()
                return Token(TokenType.LT, '<', self.line, self.column)
            
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.GE, '>=', self.line, self.column)
                self.advance()
                return Token(TokenType.GT, '>', self.line, self.column)

            # Single-character tokens
            char_to_token = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MUL,
                '/': TokenType.DIV,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }
            
            if self.current_char in char_to_token:
                token = Token(char_to_token[self.current_char], self.current_char, self.line, self.column)
                self.advance()
                return token
            
            self.error()

        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
