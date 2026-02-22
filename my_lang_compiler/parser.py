from .lexer import Lexer
from .tokens import TokenType
from .ast_nodes import (
    Program, Block, VarDecl, Assignment, BinaryOp, UnaryOp, Num, String, Bool, Var, If, While, Print, NoOp
)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected=None):
        if expected:
            raise Exception(f"Syntax Error: Expected {expected}, got {self.current_token.type} at line {self.current_token.line}, col {self.current_token.column}")
        else:
            raise Exception(f"Syntax Error: Unexpected token {self.current_token} at line {self.current_token.line}, col {self.current_token.column}")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(expected=token_type)

    def factor(self):
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)
        elif token.type == TokenType.MYBOOL:
            self.eat(TokenType.MYBOOL)
            return Bool(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Var(token)
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            
            node = BinaryOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            # Add comparisons here for simplicity in expr, though precedence might be slightly off without a dedicated level
            elif token.type in (TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
                 self.eat(token.type)

            node = BinaryOp(left=node, op=token, right=self.term())

        return node

    def empty(self):
        return NoOp()

    def variable_declaration(self):
        self.eat(TokenType.MYVAR)
        var_node = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        
        initializer = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            initializer = self.expr()
            
        self.eat(TokenType.SEMICOLON)
        return VarDecl(var_node, initializer=initializer)

    def assignment_statement(self):
        left = Var(self.current_token)
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        self.eat(TokenType.SEMICOLON)
        return Assignment(left, right)

    def print_statement(self):
        self.eat(TokenType.MYPRINT)
        self.eat(TokenType.LPAREN)
        expr = self.expr()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return Print(expr)

    def block(self):
        self.eat(TokenType.LBRACE)
        statements = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        self.eat(TokenType.RBRACE)
        return Block(statements)

    def if_statement(self):
        self.eat(TokenType.MYIF)
        self.eat(TokenType.LPAREN)
        condition = self.expr()
        self.eat(TokenType.RPAREN)
        
        then_branch = self.statement()
        else_branch = None
        
        if self.current_token.type == TokenType.MYELSE:
            self.eat(TokenType.MYELSE)
            else_branch = self.statement()
            
        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.eat(TokenType.MYWHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expr()
        self.eat(TokenType.RPAREN)
        body = self.statement()
        return While(condition, body)

    def statement(self):
        if self.current_token.type == TokenType.LBRACE:
            return self.block()
        elif self.current_token.type == TokenType.MYVAR:
            return self.variable_declaration()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment_statement()
        elif self.current_token.type == TokenType.MYPRINT:
            return self.print_statement()
        elif self.current_token.type == TokenType.MYIF:
            return self.if_statement()
        elif self.current_token.type == TokenType.MYWHILE:
            return self.while_statement()
        elif self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
            return self.empty()
        else:
            self.error()

    def program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def parse(self):
        return self.program()
