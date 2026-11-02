import sys
import os
import unittest
import io

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from unbotify.core.parsers.latex_parser import LaTeXDocParser
from unbotify.core.parsers.code_parser import CodeCommentParser
from unbotify.core.parsers.docx_parser import WordDocxParser
from docx import Document

class TestParsers(unittest.TestCase):
    def test_latex_parser_math_protection(self):
        latex_text = r"""\begin{document}
In conclusion, it is important to delve into the error bounds.
\begin{equation}
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\end{equation}
Furthermore, the value of $E = mc^2$ and $\cite{einstein1905}$ are preserved.
\end{document}"""

        def mock_transform(prose):
            return prose.replace("delve into", "explore").replace("Furthermore", "Also")

        result = LaTeXDocParser.process_latex(latex_text, mock_transform)
        # Verify math and cite macros remain 100% intact
        self.assertIn(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}", result)
        self.assertIn("$E = mc^2$", result)
        self.assertIn(r"\cite{einstein1905}", result)
        # Verify prose was modified
        self.assertIn("explore", result)

    def test_code_parser_executable_invariance(self):
        python_code = '''def compute_sum(a, b):
    """
    Computes the sum of two values.
    """
    # checks if list is empty
    if len(a) == 0:
        return "empty string literal # not a comment"
    return a + b
'''
        def mock_transform(comment):
            return comment.replace("Computes the sum", "Calculates total")

        processed = CodeCommentParser.process_code(
            code=python_code,
            lang="python",
            persona="senior",
            convert_docstrings=True,
            transform_fn=mock_transform
        )

        # Ensure executable syntax, function definition, variables and string literal are 100% intact
        self.assertIn("def compute_sum(a, b):", processed)
        self.assertIn('return "empty string literal # not a comment"', processed)
        self.assertIn("return a + b", processed)
        # Ensure persona or comment was adapted
        self.assertIn("# evaluates invariant non-empty constraint", processed)

    def test_docx_parser(self):
        doc = Document()
        p = doc.add_paragraph()
        r1 = p.add_run("The ")
        r2 = p.add_run("multifaceted")
        r2.bold = True
        r3 = p.add_run(" aspect.")

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)

        def mock_transform(text):
            return text.replace("multifaceted", "diverse")

        out_stream = WordDocxParser.process_docx(buf, mock_transform)
        new_doc = Document(out_stream)
        new_p = new_doc.paragraphs[0]
        self.assertEqual("".join(r.text for r in new_p.runs), "The diverse aspect.")
        # Verify bold run was preserved
        bold_runs = [r for r in new_p.runs if r.bold]
        self.assertTrue(len(bold_runs) > 0)

if __name__ == "__main__":
    unittest.main()

