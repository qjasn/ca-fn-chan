"""
Rewrite by Asahi_Qin
该文件是Latexify的扩展库，可以实现从文本生成latex
作者Asahi_Qin
"""

from __future__ import annotations

import ast
import enum
import textwrap

from latexify import codegen, exceptions
from latexify import config as cfg
from latexify import parser, transformers


class Style(enum.Enum):
    """The style of the generated LaTeX."""

    ALGORITHMIC = "algorithmic"
    FUNCTION = "function"
    IPYTHON_ALGORITHMIC = "ipython-algorithmic"


def get_latex_with_code(
        name: str,
        args: str,
        code: str,
        *,
        style: Style = Style.FUNCTION,
        config: cfg.Config | None = None,
        **kwargs,
) -> str:
    """Obtains LaTeX description from the function's source.

    Args:
        code:  A function source code to analyze.
        args: The function args
        name:  The function name.
        style: Style of the LaTeX description, the default is FUNCTION.
        config: Use defined Config object, if it is None, it will be automatic assigned
            with default value.
        **kwargs: Dict of Config field values that could be defined individually
            by users.

    Returns:
        Generated LaTeX description.

    Raises:
        latexify.exceptions.LatexifyError: Something went wrong during conversion.
        latexify.exceptions.LatexifySyntaxError: The code syntax error
    """
    merged_config = cfg.Config.defaults().merge(config=config, **kwargs)

    # Obtains the source AST.
    code = """def {}({}):{}""".format(name, args, code)
    source = textwrap.dedent(code)
    tree = ast.parse(source)
    if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
        raise exceptions.LatexifySyntaxError("Not a function.")

    # Mandatory AST Transformation.
    tree = transformers.AugAssignReplacer().visit(tree)

    # Conditional AST transformation.
    if merged_config.prefixes is not None:
        tree = transformers.PrefixTrimmer(merged_config.prefixes).visit(tree)
    if merged_config.identifiers is not None:
        tree = transformers.IdentifierReplacer(merged_config.identifiers).visit(tree)
    if merged_config.reduce_assignments:
        tree = transformers.DocstringRemover().visit(tree)
        tree = transformers.AssignmentReducer().visit(tree)
    if merged_config.expand_functions is not None:
        tree = transformers.FunctionExpander(merged_config.expand_functions).visit(tree)

    # Generates LaTeX.
    if style == Style.ALGORITHMIC:
        return codegen.AlgorithmicCodegen(
            use_math_symbols=merged_config.use_math_symbols,
            use_set_symbols=merged_config.use_set_symbols,
        ).visit(tree)
    elif style == Style.FUNCTION:
        return codegen.FunctionCodegen(
            use_math_symbols=merged_config.use_math_symbols,
            use_signature=merged_config.use_signature,
            use_set_symbols=merged_config.use_set_symbols,
        ).visit(tree)
    elif style == Style.IPYTHON_ALGORITHMIC:
        return codegen.IPythonAlgorithmicCodegen(
            use_math_symbols=merged_config.use_math_symbols,
            use_set_symbols=merged_config.use_set_symbols,
        ).visit(tree)

    raise ValueError(f"Unrecognized style: {style}")
