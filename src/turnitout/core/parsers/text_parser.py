"""
Markdown & Plaintext Document Parser.
Preserves Markdown code blocks, inline backticks, table syntax,
image tags, and header boundaries intact while humanizing prose.
"""

import re
from typing import Callable

class PlainTextParser:
    @classmethod
    def process_markdown(cls, content: str, transform_fn: Callable[[str], str]) -> str:
        lines = content.splitlines(keepends=True)
        in_code_block = False
        out = []

        for line in lines:
            stripped = line.strip()

            # 1. Code blocks toggle
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                out.append(line)
                continue

            if in_code_block:
                out.append(line)
                continue

            # 2. Markdown headers, table rows, horizontal rules
            if stripped.startswith(("#", "|", "---", "===", "***")) or re.match(r"^[-*+]\s+", stripped):
                # For bullet items, process text after bullet marker
                bullet_match = re.match(r"^(\s*[-*+]\s+)(.*)$", line)
                if bullet_match:
                    prefix = bullet_match.group(1)
                    bullet_text = bullet_match.group(2)
                    transformed = transform_fn(bullet_text)
                    out.append(prefix + transformed)
                    continue

                out.append(line)
                continue

            # 3. Regular prose lines
            if stripped:
                # Mask inline backtick code snippets
                inline_code = []
                def _mask_code(m):
                    token = f"⟦MD_CODE_{len(inline_code)}⟧"
                    inline_code.append(m.group(0))
                    return token

                masked = re.sub(r"`[^`\n]+`", _mask_code, line)
                transformed = transform_fn(masked)
                for idx, code_str in enumerate(inline_code):
                    transformed = transformed.replace(f"⟦MD_CODE_{idx}⟧", code_str)
                out.append(transformed)
            else:
                out.append(line)

        return "".join(out)

    @classmethod
    def process_text(cls, content: str, transform_fn: Callable[[str], str]) -> str:
        return transform_fn(content)

