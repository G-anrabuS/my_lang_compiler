# My Language Compiler

Small educational compiler for a custom language. It compiles `.src` files into C code.

## Prerequisites

- Python 3.9+
- `pip`

## Build

Build a distributable wheel:

```powershell
python -m pip wheel . -w dist
```

The wheel will be created under `dist/` (for example: `dist/my_lang_compiler-0.1.0-py3-none-any.whl`).

## Installation

Install from source (current project folder):

```powershell
python -m pip install .
```

Install from a built wheel (recommended for other machines):

```powershell
python -m pip install dist\my_lang_compiler-0.1.0-py3-none-any.whl
```

## Package Structure

- `my_lang_compiler/main.py`: CLI and compilation pipeline
- `my_lang_compiler/lexer.py`: lexer
- `my_lang_compiler/parser.py`: parser
- `my_lang_compiler/semantic_analyzer.py`: semantic checks
- `my_lang_compiler/ir.py`: IR model
- `my_lang_compiler/ir_generator.py`: AST to IR
- `my_lang_compiler/optimizer.py`: optimization pass
- `my_lang_compiler/codegen.py`: IR to C code
- `my_lang_compiler/ast_nodes.py`: AST nodes
- `my_lang_compiler/tokens.py`: token definitions

## Usage

```powershell
python -m my_lang_compiler.main path\to\program.src -o output.c
```

If installed as a package:

```powershell
my-lang-compiler path\to\program.src -o output.c
```
