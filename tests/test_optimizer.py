import unittest

from my_lang_compiler.ir import IRProgram, OpCode, Quadruple
from my_lang_compiler.optimizer import Optimizer


class OptimizerTests(unittest.TestCase):
    def test_propagates_constants_through_store_and_load(self):
        ir = IRProgram()
        ir.add(Quadruple(OpCode.CONST, arg1=7, result="t1"))
        ir.add(Quadruple(OpCode.STORE, arg1="t1", result="x"))
        ir.add(Quadruple(OpCode.LOAD, arg1="x", result="t2"))

        optimized = Optimizer(ir).optimize()

        self.assertEqual(optimized.instructions[2].op, OpCode.CONST)
        self.assertEqual(optimized.instructions[2].arg1, 7)
        self.assertEqual(optimized.instructions[2].result, "t2")

    def test_folds_comparisons_when_both_operands_are_constant(self):
        ir = IRProgram()
        ir.add(Quadruple(OpCode.CONST, arg1=4, result="t1"))
        ir.add(Quadruple(OpCode.CONST, arg1=9, result="t2"))
        ir.add(Quadruple(OpCode.SLT, arg1="t1", arg2="t2", result="t3"))

        optimized = Optimizer(ir).optimize()

        folded = optimized.instructions[2]
        self.assertEqual(folded.op, OpCode.CONST)
        self.assertEqual(folded.arg1, 1)
        self.assertEqual(folded.result, "t3")

    def test_does_not_fold_division_by_zero(self):
        ir = IRProgram()
        ir.add(Quadruple(OpCode.CONST, arg1=4, result="t1"))
        ir.add(Quadruple(OpCode.CONST, arg1=0, result="t2"))
        ir.add(Quadruple(OpCode.DIV, arg1="t1", arg2="t2", result="t3"))

        optimized = Optimizer(ir).optimize()

        self.assertEqual(optimized.instructions[2].op, OpCode.DIV)

    def test_clears_constants_across_control_flow_boundaries(self):
        ir = IRProgram()
        ir.add(Quadruple(OpCode.CONST, arg1=1, result="t1"))
        ir.add(Quadruple(OpCode.STORE, arg1="t1", result="x"))
        ir.add(Quadruple(OpCode.JMP, result="L1"))
        ir.add(Quadruple(OpCode.LABEL, result="L1"))
        ir.add(Quadruple(OpCode.LOAD, arg1="x", result="t2"))

        optimized = Optimizer(ir).optimize()

        self.assertEqual(optimized.instructions[4].op, OpCode.LOAD)


if __name__ == "__main__":
    unittest.main()
