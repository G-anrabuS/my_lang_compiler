import argparse
import re
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .semantic_analyzer import SemanticAnalyzer
from .ir_generator import IRGenerator
from .optimizer import Optimizer
from .codegen import CodeGenerator


def cli_version():
    try:
        return version("my-lang-compiler")
    except PackageNotFoundError:
        pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
        try:
            pyproject_text = pyproject_path.read_text(encoding="utf-8")
        except OSError:
            return "unknown"

        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject_text, flags=re.MULTILINE)
        if match:
            return match.group(1)
        return "unknown"


def compile_source(source_code, verbose=True):
    try:
        if verbose:
            print("1. Lexical Analysis...")
        lexer = Lexer(source_code)

        if verbose:
            print("2. Parsing...")
        parser = Parser(lexer)
        ast = parser.parse()

        if verbose:
            print("3. Semantic Analysis...")
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)

        if verbose:
            print("4. IR Generation...")
        ir_generator = IRGenerator()
        ir_program = ir_generator.visit(ast)

        if verbose:
            print("Original IR:")
            print(ir_program)

        if verbose:
            print("5. Optimization...")
        optimizer = Optimizer(ir_program)
        optimized_ir = optimizer.optimize()

        if verbose:
            print("Optimized IR:")
            print(optimized_ir)

        if verbose:
            print("6. Code Generation...")
        codegen = CodeGenerator(optimized_ir)
        c_code = codegen.generate()

        return c_code

    except Exception as e:
        print(f"Compilation Error: {e}")
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="my-lang-compiler",
        description="Compile .src files into C code.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {cli_version()}",
    )
    parser.add_argument("source", help="Path to source .src file")
    parser.add_argument(
        "-o",
        "--output",
        default="output.c",
        help="Path to generated C file (default: output.c)",
    )
    args = parser.parse_args(argv)

    try:
        with open(args.source, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()
    except OSError as exc:
        print(f"Failed to read source file '{args.source}': {exc}")
        return 1

    c_output = compile_source(source_code)
    if c_output is None:
        return 1

    try:
        with open(args.output, "w", encoding="utf-8") as out_file:
            out_file.write(c_output)
    except OSError as exc:
        print(f"Failed to write output file '{args.output}': {exc}")
        return 1

    print(f"Successfully compiled to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
