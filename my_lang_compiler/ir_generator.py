from .ast_nodes import Program, Block, VarDecl, Assignment, BinaryOp, UnaryOp, Num, String, Bool, Var, If, While, Print, Return, NoOp
from .ir import OpCode, Quadruple, IRProgram
from .tokens import TokenType

class IRGenerator:
    def __init__(self):
        self.program = IRProgram()
        self.temp_counter = 0
        self.label_counter = 0
    
    def fresh_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def fresh_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)
        return self.program

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        if node.initializer:
            # Generate code for initializer expr
            result_temp = self.visit(node.initializer)
            # Store result in variable
            self.program.add(Quadruple(OpCode.STORE, arg1=result_temp, result=node.var_name.value))

    def visit_Assignment(self, node):
        result_temp = self.visit(node.right)
        self.program.add(Quadruple(OpCode.STORE, arg1=result_temp, result=node.left.value))

    def visit_BinaryOp(self, node):
        left_temp = self.visit(node.left)
        right_temp = self.visit(node.right)
        result_temp = self.fresh_temp()
        
        op_map = {
            TokenType.PLUS: OpCode.ADD,
            TokenType.MINUS: OpCode.SUB,
            TokenType.MUL: OpCode.MUL,
            TokenType.DIV: OpCode.DIV,
            TokenType.EQ: OpCode.SEQ,
            TokenType.NE: OpCode.SNE,
            TokenType.LT: OpCode.SLT,
            TokenType.LE: OpCode.SLE,
            TokenType.GT: OpCode.SGT,
            TokenType.GE: OpCode.SGE,
        }
        
        op_code = op_map.get(node.op.type)
        if op_code:
            self.program.add(Quadruple(op_code, arg1=left_temp, arg2=right_temp, result=result_temp))
        else:
            raise Exception(f"Unknown binary op {node.op.type}")
            
        return result_temp

    def visit_UnaryOp(self, node):
        expr_temp = self.visit(node.expr)
        result_temp = self.fresh_temp()
        
        if node.op.type == TokenType.MINUS:
            # 0 - expr
            zero = self.fresh_temp()
            self.program.add(Quadruple(OpCode.CONST, arg1=0, result=zero))
            self.program.add(Quadruple(OpCode.SUB, arg1=zero, arg2=expr_temp, result=result_temp))
        elif node.op.type == TokenType.PLUS:
            return expr_temp
            
        return result_temp

    def visit_Num(self, node):
        temp = self.fresh_temp()
        self.program.add(Quadruple(OpCode.CONST, arg1=node.value, result=temp))
        return temp

    def visit_String(self, node):
        return node.value

    def visit_Bool(self, node):
        temp = self.fresh_temp()
        self.program.add(Quadruple(OpCode.CONST, arg1=1 if node.value else 0, result=temp))
        return temp

    def visit_Var(self, node):
        temp = self.fresh_temp()
        self.program.add(Quadruple(OpCode.LOAD, arg1=node.value, result=temp))
        return temp

    def visit_If(self, node):
        condition_temp = self.visit(node.condition)
        
        else_label = self.fresh_label()
        end_label = self.fresh_label()
        
        # If false, jump to else
        self.program.add(Quadruple(OpCode.JFALSE, arg1=condition_temp, result=else_label))
        
        # Then block
        self.visit(node.then_branch)
        self.program.add(Quadruple(OpCode.JMP, result=end_label))
        
        # Else block
        self.program.add(Quadruple(OpCode.LABEL, result=else_label))
        if node.else_branch:
            self.visit(node.else_branch)
            
        self.program.add(Quadruple(OpCode.LABEL, result=end_label))

    def visit_While(self, node):
        start_label = self.fresh_label()
        end_label = self.fresh_label()
        
        self.program.add(Quadruple(OpCode.LABEL, result=start_label))
        
        condition_temp = self.visit(node.condition)
        self.program.add(Quadruple(OpCode.JFALSE, arg1=condition_temp, result=end_label))
        
        self.visit(node.body)
        self.program.add(Quadruple(OpCode.JMP, result=start_label))
        
        self.program.add(Quadruple(OpCode.LABEL, result=end_label))

    def visit_Print(self, node):
        if isinstance(node.expr, String):
            self.program.add(Quadruple(OpCode.PRINTS, arg1=node.expr.value))
        else:
            expr_temp = self.visit(node.expr)
            self.program.add(Quadruple(OpCode.PRINT, arg1=expr_temp))

    def visit_Return(self, node):
        if node.expr is None:
            self.program.add(Quadruple(OpCode.RETURN, arg1=0))
            return

        if isinstance(node.expr, String):
            raise Exception("Return expression must be numeric or boolean")

        expr_temp = self.visit(node.expr)
        self.program.add(Quadruple(OpCode.RETURN, arg1=expr_temp))

    def visit_NoOp(self, node):
        pass
