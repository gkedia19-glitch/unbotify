"""
Word (.docx) Document In-Place Processor.
Uses character-span alignment via difflib.SequenceMatcher to project transformed prose
back into innermost OOXML text runs (w:t) while preserving fonts, bold, italics,
tables, headers, footers, and hyperlinks intact.
"""

import io
import difflib
from typing import Callable, Union
from docx import Document
from docx.text.paragraph import Paragraph

class WordDocxParser:
    @staticmethod
    def process_paragraph_runs(paragraph: Paragraph, transform_fn: Callable[[str], str]):
        runs = paragraph.runs
        if not runs:
            return

        full_text = "".join(r.text for r in runs)
        if not full_text.strip():
            return

        # Single run fast-path
        if len(runs) == 1:
            transformed = transform_fn(full_text)
            runs[0].text = transformed
            return

        # Multi-run character span mapping
        run_spans = []
        curr_idx = 0
        for r in runs:
            length = len(r.text)
            run_spans.append((curr_idx, curr_idx + length, r))
            curr_idx += length

        transformed_text = transform_fn(full_text)
        if full_text == transformed_text:
            return

        matcher = difflib.SequenceMatcher(None, full_text, transformed_text)
        new_run_texts = [[] for _ in runs]

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            sub_transformed = transformed_text[j1:j2]
            orig_len = i2 - i1

            if orig_len == 0:
                # Pure insertion: append to run covering i1
                placed = False
                for r_idx, (r_start, r_end, _) in enumerate(run_spans):
                    if r_start <= i1 <= r_end:
                        new_run_texts[r_idx].append(sub_transformed)
                        placed = True
                        break
                if not placed and new_run_texts:
                    new_run_texts[-1].append(sub_transformed)
            else:
                for r_idx, (r_start, r_end, _) in enumerate(run_spans):
                    overlap_start = max(i1, r_start)
                    overlap_end = min(i2, r_end)
                    if overlap_start < overlap_end:
                        t_start = int((overlap_start - i1) * len(sub_transformed) / orig_len)
                        t_end = int((overlap_end - i1) * len(sub_transformed) / orig_len)
                        new_run_texts[r_idx].append(sub_transformed[t_start:t_end])

        for r_idx, run_obj in enumerate(runs):
            run_obj.text = "".join(new_run_texts[r_idx])

    @classmethod
    def process_docx(cls, input_data: Union[str, bytes, io.BytesIO], transform_fn: Callable[[str], str]) -> io.BytesIO:
        if isinstance(input_data, (bytes, bytearray)):
            stream = io.BytesIO(input_data)
        elif isinstance(input_data, str):
            with open(input_data, "rb") as f:
                stream = io.BytesIO(f.read())
        else:
            stream = input_data

        doc = Document(stream)

        # 1. Body paragraphs
        for p in doc.paragraphs:
            cls.process_paragraph_runs(p, transform_fn)

        # 2. Table cells
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        cls.process_paragraph_runs(p, transform_fn)

        # 3. Headers and Footers across all sections
        for s in doc.sections:
            if s.header:
                for p in s.header.paragraphs:
                    cls.process_paragraph_runs(p, transform_fn)
                for table in s.header.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for p in cell.paragraphs:
                                cls.process_paragraph_runs(p, transform_fn)
            if s.footer:
                for p in s.footer.paragraphs:
                    cls.process_paragraph_runs(p, transform_fn)
                for table in s.footer.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for p in cell.paragraphs:
                                cls.process_paragraph_runs(p, transform_fn)

        out_stream = io.BytesIO()
        doc.save(out_stream)
        out_stream.seek(0)
        return out_stream

