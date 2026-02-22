from .ir import OpCode, Quadruple, IRProgram

class Optimizer:
    def __init__(self, ir_program):
        self.ir = ir_program

    def optimize(self):
        new_ir = IRProgram()
        # Constants map: temp -> value
        constants = {}

        for instr in self.ir.instructions:
            if instr.op == OpCode.CONST:
                constants[instr.result] = instr.arg1
                new_ir.add(instr)
            elif instr.op in (OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV):
                arg1_val = constants.get(instr.arg1)
                arg2_val = constants.get(instr.arg2)

                if arg1_val is not None and arg2_val is not None:
                    # Fold constant
                    res_val = 0
                    if instr.op == OpCode.ADD:
                        res_val = arg1_val + arg2_val
                    elif instr.op == OpCode.SUB:
                        res_val = arg1_val - arg2_val
                    elif instr.op == OpCode.MUL:
                        res_val = arg1_val * arg2_val
                    elif instr.op == OpCode.DIV:
                        res_val = arg1_val // arg2_val  # Integer division
                    
                    # Replace with CONST
                    new_instr = Quadruple(OpCode.CONST, arg1=res_val, result=instr.result)
                    constants[instr.result] = res_val
                    new_ir.add(new_instr)
                else:
                    new_ir.add(instr)
            else:
                new_ir.add(instr)
                
        return new_ir
