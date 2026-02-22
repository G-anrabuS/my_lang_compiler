from .ir import OpCode

class CodeGenerator:
    def __init__(self, ir_program):
        self.ir = ir_program
        self.temps = set()
        self.vars = set()

    def _collect_operand(self, operand):
        if operand is None or not isinstance(operand, str):
            return
        if operand.startswith('L'):
            return
        if operand.startswith('t'):
            self.temps.add(operand)
            return
        if operand.isidentifier():
            self.vars.add(operand)

    def _escape_c_string(self, value):
        escaped = value.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        escaped = escaped.replace("\n", "\\n")
        escaped = escaped.replace("\t", "\\t")
        escaped = escaped.replace("\r", "\\r")
        return escaped

    def generate(self):
        # 1. Collect all variables and temps
        for instr in self.ir.instructions:
            if instr.result is not None:
                self._collect_operand(instr.result)

            if instr.op in (
                OpCode.LOAD, OpCode.STORE, OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV,
                OpCode.JFALSE, OpCode.PRINT, OpCode.SLT, OpCode.SEQ, OpCode.SLE,
                OpCode.SGT, OpCode.SGE, OpCode.SNE
            ):
                self._collect_operand(instr.arg1)
                self._collect_operand(instr.arg2)

        # 2. Output C code
        lines = []
        lines.append("#include <stdio.h>")
        lines.append("int main() {")
        
        # Declarations
        all_vars = sorted(list(self.temps) + list(self.vars))
        if all_vars:
            lines.append("    int " + ", ".join(all_vars) + ";")

        # Instructions
        for instr in self.ir.instructions:
            line = "    "
            if instr.op == OpCode.CONST:
                line += f"{instr.result} = {instr.arg1};"
            elif instr.op == OpCode.LOAD:
                line += f"{instr.result} = {instr.arg1};"
            elif instr.op == OpCode.STORE:
                line += f"{instr.result} = {instr.arg1};"
            elif instr.op == OpCode.ADD:
                line += f"{instr.result} = {instr.arg1} + {instr.arg2};"
            elif instr.op == OpCode.SUB:
                line += f"{instr.result} = {instr.arg1} - {instr.arg2};"
            elif instr.op == OpCode.MUL:
                line += f"{instr.result} = {instr.arg1} * {instr.arg2};"
            elif instr.op == OpCode.DIV:
                line += f"{instr.result} = {instr.arg1} / {instr.arg2};"
            elif instr.op == OpCode.JMP:
                line += f"goto {instr.result};"
            elif instr.op == OpCode.JFALSE:
                line += f"if (!{instr.arg1}) goto {instr.result};"
            elif instr.op == OpCode.LABEL:
                line = f"{instr.result}:;" 
            elif instr.op == OpCode.PRINT:
                line += f'printf("%d\\n", {instr.arg1});'
            elif instr.op == OpCode.PRINTS:
                line += f'printf("%s\\n", "{self._escape_c_string(instr.arg1)}");'
            elif instr.op == OpCode.SLT:
                line += f"{instr.result} = ({instr.arg1} < {instr.arg2});"
            elif instr.op == OpCode.SEQ:
                line += f"{instr.result} = ({instr.arg1} == {instr.arg2});"
            elif instr.op == OpCode.SNE:
                line += f"{instr.result} = ({instr.arg1} != {instr.arg2});"
            elif instr.op == OpCode.SLE:
                line += f"{instr.result} = ({instr.arg1} <= {instr.arg2});"
            elif instr.op == OpCode.SGT:
                line += f"{instr.result} = ({instr.arg1} > {instr.arg2});"
            elif instr.op == OpCode.SGE:
                line += f"{instr.result} = ({instr.arg1} >= {instr.arg2});"
            else:
                raise Exception(f"Unsupported opcode in codegen: {instr.op}")
            
            lines.append(line)

        lines.append("    return 0;")
        lines.append("}")
        return "\n".join(lines)
