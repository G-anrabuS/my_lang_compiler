from .ir import OpCode, Quadruple, IRProgram


class Optimizer:
    def __init__(self, ir_program):
        self.ir = ir_program

    def _compute_binary(self, op, arg1, arg2):
        if op == OpCode.ADD:
            return arg1 + arg2
        if op == OpCode.SUB:
            return arg1 - arg2
        if op == OpCode.MUL:
            return arg1 * arg2
        if op == OpCode.DIV:
            if arg2 == 0:
                return None
            return arg1 // arg2  # Integer division
        if op == OpCode.SEQ:
            return 1 if arg1 == arg2 else 0
        if op == OpCode.SNE:
            return 1 if arg1 != arg2 else 0
        if op == OpCode.SLT:
            return 1 if arg1 < arg2 else 0
        if op == OpCode.SLE:
            return 1 if arg1 <= arg2 else 0
        if op == OpCode.SGT:
            return 1 if arg1 > arg2 else 0
        if op == OpCode.SGE:
            return 1 if arg1 >= arg2 else 0
        return None

    def optimize(self):
        new_ir = IRProgram()
        # Constants map: temp/variable -> value
        constants = {}

        foldable_ops = {
            OpCode.ADD,
            OpCode.SUB,
            OpCode.MUL,
            OpCode.DIV,
            OpCode.SEQ,
            OpCode.SNE,
            OpCode.SLT,
            OpCode.SLE,
            OpCode.SGT,
            OpCode.SGE,
        }

        control_flow_ops = {OpCode.JMP, OpCode.JFALSE, OpCode.JIF, OpCode.LABEL}

        for instr in self.ir.instructions:
            if instr.op == OpCode.CONST:
                constants[instr.result] = instr.arg1
                new_ir.add(instr)
                continue

            if instr.op == OpCode.LOAD:
                known_value = constants.get(instr.arg1)
                if known_value is not None:
                    folded = Quadruple(OpCode.CONST, arg1=known_value, result=instr.result)
                    constants[instr.result] = known_value
                    new_ir.add(folded)
                else:
                    constants.pop(instr.result, None)
                    new_ir.add(instr)
                continue

            if instr.op == OpCode.STORE:
                stored_value = constants.get(instr.arg1)
                if stored_value is not None:
                    constants[instr.result] = stored_value
                else:
                    constants.pop(instr.result, None)
                new_ir.add(instr)
                continue

            if instr.op in foldable_ops:
                arg1_val = constants.get(instr.arg1)
                arg2_val = constants.get(instr.arg2)

                if arg1_val is not None and arg2_val is not None:
                    folded_value = self._compute_binary(instr.op, arg1_val, arg2_val)
                    if folded_value is not None:
                        folded = Quadruple(OpCode.CONST, arg1=folded_value, result=instr.result)
                        constants[instr.result] = folded_value
                        new_ir.add(folded)
                        continue

                constants.pop(instr.result, None)
                new_ir.add(instr)
                continue

            if instr.op in control_flow_ops:
                constants.clear()
                new_ir.add(instr)
                continue

            # Unknown/other instructions can invalidate result knowledge.
            if instr.result is not None:
                constants.pop(instr.result, None)
            new_ir.add(instr)

        return new_ir
