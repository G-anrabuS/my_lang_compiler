from .ast_nodes import Program, Block, VarDecl, Assignment, BinaryOp, UnaryOp, Num, String, Var, If, While, Print, NoOp, AST
from .tokens import TokenType

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type_):
        # Keep declared symbols truthy even when no explicit type annotation is provided.
        self.symbols[name] = type_ if type_ is not None else "auto"

    def lookup(self, name, local_only=False):
        if name in self.symbols:
            return self.symbols[name]
        if local_only:
            return None
        if self.parent:
            return self.parent.lookup(name)
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = SymbolTable()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        # Basic dispatch
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if hasattr(node, '__dict__'):
            for child in node.__dict__.values():
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST):
                             self.visit(item)
                elif isinstance(child, AST):
                    self.visit(child)

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node):
        previous_scope = self.current_scope
        self.current_scope = SymbolTable(parent=previous_scope)
        try:
            for stmt in node.statements:
                self.visit(stmt)
        finally:
            self.current_scope = previous_scope

    def visit_VarDecl(self, node):
        var_name = node.var_name.value
        # Check current scope only for redefinition
        if self.current_scope.lookup(var_name, local_only=True) is not None:
             raise Exception(f"Variable '{var_name}' already declared in this scope")

        if node.initializer:
            self.visit(node.initializer)
            
        self.current_scope.define(var_name, node.type_annotation)

    def visit_Assignment(self, node):
        # Check if left is a Var (it should be)
        if not isinstance(node.left, Var):
             raise Exception(f"Invalid assignment target")
             
        var_name = node.left.value
        if self.current_scope.lookup(var_name) is None:
            raise Exception(f"Variable '{var_name}' not declared before assignment")
        
        self.visit(node.right)

    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Num(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_Var(self, node):
        var_name = node.value
        if self.current_scope.lookup(var_name) is None:
            raise Exception(f"Variable '{var_name}' not declared")

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_While(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_Print(self, node):
        self.visit(node.expr)

    def visit_NoOp(self, node):
        pass

from .ast_nodes import AST
