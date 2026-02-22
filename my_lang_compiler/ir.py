from enum import Enum, auto

class OpCode(Enum):
    CONST = auto()      # result = const
    LOAD = auto()       # result = var
    STORE = auto()      # var = arg1
    ADD = auto()        # result = arg1 + arg2
    SUB = auto()        # result = arg1 - arg2
    MUL = auto()        # result = arg1 * arg2
    DIV = auto()        # result = arg1 / arg2
    JMP = auto()        # goto arg1 (label)
    JIF = auto()        # if arg1 goto arg2 (label) - Jump if true
    JFALSE = auto()     # if not arg1 goto arg2 - Jump if false
    LABEL = auto()      # label definition
    PRINT = auto()      # print arg1
    PRINTS = auto()     # print string literal
    RETURN = auto()     # return arg1 (or return 0 if omitted)
    SLT = auto()        # Set Less Than: result = (arg1 < arg2)
    SEQ = auto()        # Set Equal: result = (arg1 == arg2)
    SLE = auto()        # Set Less Equal
    SGT = auto()        # Set Greater Than
    SGE = auto()        # Set Greater Equal
    SNE = auto()        # Set Not Equal

class Quadruple:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        op_name = self.op.name
        arg1_str = str(self.arg1) if self.arg1 is not None else ""
        arg2_str = str(self.arg2) if self.arg2 is not None else ""
        res_str = str(self.result) if self.result is not None else ""
        
        if self.op == OpCode.LABEL:
            return f"{res_str}:"
        
        return f"{op_name:6} {arg1_str:10} {arg2_str:10} -> {res_str}"

class IRProgram:
    def __init__(self):
        self.instructions = []

    def add(self, quad):
        self.instructions.append(quad)
    
    def __repr__(self):
        return "\n".join(str(instr) for instr in self.instructions)
