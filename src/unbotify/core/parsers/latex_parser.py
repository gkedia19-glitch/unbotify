"""
LaTeX Document Parser with Bijective Sentinel Masking.
Locks mathematical formulas, environments, commands, and citations,
exposing only human prose to the transformation pipeline.
"""

import re
from typing import Dict, Tuple, Callable

class LaTeXDocParser:
    DISPLAY_ENV_PATTERN = re.compile(
        r"(\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|split|matrix|pmatrix|bmatrix|table\*?|figure\*?)\}.*?\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|split|matrix|pmatrix|bmatrix|table\*?|figure\*?)\})",
        re.DOTALL
    )
    BRACKET_MATH_PATTERN = re.compile(r"(\\\[.*?\\\])", re.DOTALL)
    DOUBLE_DOLLAR_PATTERN = re.compile(r"(\$\$.*?\$\$)", re.DOTALL)
    INLINE_DOLLAR_PATTERN = re.compile(r"(?<!\\)(\$(?:\\.|[^$])+\$)", re.DOTALL)
    INLINE_PAREN_PATTERN = re.compile(r"(\\\(.*?\\\))", re.DOTALL)
    CITE_PATTERN = re.compile(r"(\\(?:cite[a-z]*|citep|citet|nocite)\*?(?:\[.*?\])?\{.*?\})")
    REF_LABEL_PATTERN = re.compile(r"(\\(?:label|ref|eqref|pageref|autoref|nameref)\{.*?\})")
    COMMAND_PATTERN = re.compile(r"(\\(?:usepackage|documentclass|input|include|bibliography|bibliographystyle|newcommand|def)\*?(?:\[.*?\])?\{.*?\})")

    SENTINEL_PREFIX = "⟦TOT_LX_PH_"
    SENTINEL_SUFFIX = "⟧"

    @classmethod
    def mask(cls, content: str) -> Tuple[str, Dict[str, str]]:
        lookup: Dict[str, str] = {}
        idx = 0

        def _repl(m):
            nonlocal idx
            token = f"{cls.SENTINEL_PREFIX}{idx:05d}{cls.SENTINEL_SUFFIX}"
            lookup[token] = m.group(1)
            idx += 1
            return token

        # Order is critical: large environments first
        masked = cls.DISPLAY_ENV_PATTERN.sub(_repl, content)
        masked = cls.BRACKET_MATH_PATTERN.sub(_repl, masked)
        masked = cls.DOUBLE_DOLLAR_PATTERN.sub(_repl, masked)
        masked = cls.INLINE_DOLLAR_PATTERN.sub(_repl, masked)
        masked = cls.INLINE_PAREN_PATTERN.sub(_repl, masked)
        masked = cls.CITE_PATTERN.sub(_repl, masked)
        masked = cls.REF_LABEL_PATTERN.sub(_repl, masked)
        masked = cls.COMMAND_PATTERN.sub(_repl, masked)

        return masked, lookup

    @classmethod
    def restore(cls, masked_content: str, lookup: Dict[str, str]) -> str:
        restored = masked_content
        for token, original in lookup.items():
            restored = restored.replace(token, original)
        return restored

    @classmethod
    def process_latex(cls, content: str, transform_fn: Callable[[str], str]) -> str:
        # Separate preamble if present
        preamble = ""
        body = content
        doc_begin = content.find(r"\begin{document}")
        if doc_begin != -1:
            split_pos = doc_begin + len(r"\begin{document}")
            preamble = content[:split_pos]
            body = content[split_pos:]

        masked_body, lookup = cls.mask(body)
        transformed_body = transform_fn(masked_body)
        restored_body = cls.restore(transformed_body, lookup)

        return preamble + restored_body

