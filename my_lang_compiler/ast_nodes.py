class AST:
    pass

class Program(AST):
    def __init__(self, statements):
        self.statements = statements

class Block(AST):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(AST):
    def __init__(self, var_name, type_annotation=None, initializer=None):
        self.var_name = var_name
        self.type_annotation = type_annotation
        self.initializer = initializer

class Assignment(AST):
    def __init__(self, left, right):
        self.left = left # Var
        self.right = right # Expr

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class If(AST):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class NoOp(AST):
    pass
