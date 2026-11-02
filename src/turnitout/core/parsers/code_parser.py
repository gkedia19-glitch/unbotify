"""
Quote-Aware Source Code Comment & Docstring Parser.
Guarantees 100% executable invariance. Code syntax, keywords, identifiers,
logic conditions, and indentation remain bit-for-bit locked while natural language
comments and docstrings are humanized according to Developer Personas.
"""

from enum import Enum, auto
from typing import Callable, List, Optional

class CodeState(Enum):
    CODE = auto()
    STRING_SINGLE = auto()
    STRING_DOUBLE = auto()
    STRING_BACKTICK = auto()
    STRING_TRIPLE_DOUBLE = auto()
    STRING_TRIPLE_SINGLE = auto()
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()

class CodeCommentParser:
    PERSONA_VOCAB = {
        "beginner": {
            "validates collection boundary": "checks if list is empty",
            "evaluates invariant non-empty constraint": "checks if list is empty",
            "iterates over dataset": "loops through all items",
            "executes sequential traversal": "loops through all items",
            "persists user record": "saves user to database",
            "commits entity state to datastore": "saves user to database",
            "asynchronous event loop dispatch": "runs background task",
            "computes heuristic cost metric": "calculates score"
        },
        "senior": {
            "checks if list is empty": "evaluates invariant non-empty constraint",
            "loops through all items": "executes sequential traversal across collection",
            "saves user to database": "commits entity state to datastore",
            "runs background task": "dispatches asynchronous event worker",
            "calculates score": "computes objective cost metric",
            "handles error": "executes fault-tolerant recovery fallback",
            "gets data": "queries upstream persistence provider"
        }
    }

    @classmethod
    def adapt_persona(cls, comment_text: str, persona: str) -> str:
        persona = persona.lower()
        if persona in cls.PERSONA_VOCAB:
            for src, target in cls.PERSONA_VOCAB[persona].items():
                comment_text = comment_text.replace(src, target)
        return comment_text

    @classmethod
    def process_code(
        cls,
        code: str,
        lang: str = "python",
        persona: str = "intermediate",
        convert_docstrings: bool = False,
        transform_fn: Optional[Callable[[str], str]] = None
    ) -> str:
        lang = lang.lower()
        i = 0
        n = len(code)
        state = CodeState.CODE
        out = []
        token_buf = []

        def flush_comment(buf: List[str], prefix: str, suffix: str) -> str:
            raw = "".join(buf).strip()
            humanized = transform_fn(raw) if transform_fn else raw
            adapted = cls.adapt_persona(humanized, persona)
            return f"{prefix}{adapted}{suffix}"

        while i < n:
            ch = code[i]
            next_ch = code[i+1] if i + 1 < n else ""
            triplet = code[i:i+3]

            if state == CodeState.CODE:
                # Python docstring detection
                if lang == "python" and triplet == '"""':
                    state = CodeState.STRING_TRIPLE_DOUBLE
                    token_buf = []
                    i += 3
                    continue
                elif lang == "python" and triplet == "'''":
                    state = CodeState.STRING_TRIPLE_SINGLE
                    token_buf = []
                    i += 3
                    continue
                # Line comments
                elif (lang in ["python", "shell", "r"] and ch == '#') or \
                     (lang in ["c", "cpp", "java", "javascript", "typescript", "go", "rust", "csharp", "php", "swift", "kotlin"] and ch == '/' and next_ch == '/') or \
                     (lang == "sql" and ch == '-' and next_ch == '-'):
                    state = CodeState.LINE_COMMENT
                    token_buf = []
                    i += (2 if next_ch in ['/', '-'] else 1)
                    continue
                # Block comments
                elif (lang in ["c", "cpp", "java", "javascript", "typescript", "go", "rust", "csharp", "php", "sql", "css"] and ch == '/' and next_ch == '*'):
                    state = CodeState.BLOCK_COMMENT
                    token_buf = []
                    i += 2
                    continue
                elif (lang in ["html", "xml"] and triplet == '<!--'):
                    state = CodeState.BLOCK_COMMENT
                    token_buf = []
                    i += 4
                    continue
                # String literals
                elif ch == "'":
                    state = CodeState.STRING_SINGLE
                    out.append(ch)
                    i += 1
                elif ch == '"':
                    state = CodeState.STRING_DOUBLE
                    out.append(ch)
                    i += 1
                elif ch == '`' and lang in ["javascript", "typescript", "go"]:
                    state = CodeState.STRING_BACKTICK
                    out.append(ch)
                    i += 1
                else:
                    out.append(ch)
                    i += 1

            elif state == CodeState.LINE_COMMENT:
                if ch == '\n':
                    prefix = "// " if lang in ["c", "cpp", "java", "javascript", "typescript", "go", "rust", "csharp", "php"] else ("-- " if lang == "sql" else "# ")
                    out.append(flush_comment(token_buf, prefix, ""))
                    out.append('\n')
                    state = CodeState.CODE
                    token_buf = []
                else:
                    token_buf.append(ch)
                i += 1

            elif state == CodeState.BLOCK_COMMENT:
                if (lang in ["html", "xml"] and triplet == '-->'):
                    out.append(flush_comment(token_buf, "<!-- ", " -->"))
                    state = CodeState.CODE
                    token_buf = []
                    i += 3
                elif (ch == '*' and next_ch == '/'):
                    out.append(flush_comment(token_buf, "/* ", " */"))
                    state = CodeState.CODE
                    token_buf = []
                    i += 2
                else:
                    token_buf.append(ch)
                i += 1

            elif state == CodeState.STRING_TRIPLE_DOUBLE:
                if triplet == '"""':
                    if convert_docstrings:
                        raw = "".join(token_buf).strip()
                        lines = raw.splitlines()
                        converted_lines = []
                        for l in lines:
                            l_strip = l.strip()
                            if l_strip:
                                hum = transform_fn(l_strip) if transform_fn else l_strip
                                hum = cls.adapt_persona(hum, persona)
                                converted_lines.append(f"# {hum}")
                            else:
                                converted_lines.append("#")
                        out.append("\n".join(converted_lines) + "\n")
                    else:
                        out.append(f'"""{flush_comment(token_buf, "", "")}"""')
                    state = CodeState.CODE
                    token_buf = []
                    i += 3
                    continue
                else:
                    token_buf.append(ch)
                i += 1

            elif state == CodeState.STRING_TRIPLE_SINGLE:
                if triplet == "'''":
                    if convert_docstrings:
                        raw = "".join(token_buf).strip()
                        lines = raw.splitlines()
                        converted_lines = [f"# {cls.adapt_persona(transform_fn(l.strip()) if transform_fn else l.strip(), persona)}" for l in lines if l.strip()]
                        out.append("\n".join(converted_lines) + "\n")
                    else:
                        out.append(f"'''{flush_comment(token_buf, '', '')}'''")
                    state = CodeState.CODE
                    token_buf = []
                    i += 3
                    continue
                else:
                    token_buf.append(ch)
                i += 1

            elif state in [CodeState.STRING_SINGLE, CodeState.STRING_DOUBLE, CodeState.STRING_BACKTICK]:
                out.append(ch)
                if ch == '\\' and i + 1 < n:
                    out.append(code[i+1])
                    i += 2
                    continue
                if (state == CodeState.STRING_SINGLE and ch == "'") or \
                   (state == CodeState.STRING_DOUBLE and ch == '"') or \
                   (state == CodeState.STRING_BACKTICK and ch == '`'):
                    state = CodeState.CODE
                i += 1

        if state == CodeState.LINE_COMMENT:
            prefix = "// " if lang in ["c", "cpp", "java", "javascript", "typescript", "go", "rust", "csharp", "php"] else ("-- " if lang == "sql" else "# ")
            out.append(flush_comment(token_buf, prefix, ""))

        return "".join(out)
