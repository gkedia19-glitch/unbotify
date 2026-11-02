"""
Multi-File & In-Memory Batch Document Processor.
Stateless in-memory streaming with zero physical disk caching (GDPR & EU AI Act compliant).
Packages humanized files into branded ZIP archives.
"""

import io
import time
import zipfile
from typing import Dict, Tuple, Any, Optional
from unbotify.config import UnbotifyConfig
from unbotify.core.modifier import TextModifier
from unbotify.core.parsers.docx_parser import WordDocxParser
from unbotify.core.parsers.latex_parser import LaTeXDocParser
from unbotify.core.parsers.code_parser import CodeCommentParser
from unbotify.core.parsers.text_parser import PlainTextParser

class DocumentProcessor:
    CODE_EXTENSIONS = {
        ".py": "python", ".c": "c", ".cpp": "cpp", ".h": "cpp", ".hpp": "cpp",
        ".java": "java", ".js": "javascript", ".ts": "typescript", ".go": "go",
        ".rs": "rust", ".cs": "csharp", ".sh": "shell", ".sql": "sql"
    }

    def __init__(self, config: Optional[UnbotifyConfig] = None):
        self.config = config or UnbotifyConfig()
        self.modifier = TextModifier(self.config)

    def process_file_bytes(self, filename: str, file_bytes: bytes) -> Tuple[bytes, str]:
        """
        Processes an individual file given its filename and raw bytes.
        Returns: (processed_bytes, output_mime_type)
        """
        lower = filename.lower()

        # 1. Word .docx
        if lower.endswith(".docx"):
            out_stream = WordDocxParser.process_docx(file_bytes, self.modifier.modify_text)
            return out_stream.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        # 2. LaTeX .tex
        elif lower.endswith((".tex", ".ltx", ".sty")):
            text = file_bytes.decode("utf-8", errors="replace")
            processed = LaTeXDocParser.process_latex(text, self.modifier.modify_text)
            return processed.encode("utf-8"), "application/x-tex"

        # 3. Source Code
        elif any(lower.endswith(ext) for ext in self.CODE_EXTENSIONS):
            ext = next(e for e in self.CODE_EXTENSIONS if lower.endswith(e))
            lang = self.CODE_EXTENSIONS[ext]
            text = file_bytes.decode("utf-8", errors="replace")
            processed = CodeCommentParser.process_code(
                code=text,
                lang=lang,
                persona=self.config.DEVELOPER_PERSONA,
                convert_docstrings=self.config.CONVERT_DOCSTRINGS,
                transform_fn=self.modifier.modify_text
            )
            return processed.encode("utf-8"), "text/plain"

        # 4. Markdown & Plaintext
        elif lower.endswith((".md", ".markdown")):
            text = file_bytes.decode("utf-8", errors="replace")
            processed = PlainTextParser.process_markdown(text, self.modifier.modify_text)
            return processed.encode("utf-8"), "text/markdown"
        elif lower.endswith(".txt"):
            text = file_bytes.decode("utf-8", errors="replace")
            processed = PlainTextParser.process_text(text, self.modifier.modify_text)
            return processed.encode("utf-8"), "text/plain"

        # 5. Fallback for unhandled types: return byte-exact copy
        return file_bytes, "application/octet-stream"

    def process_zip_package(self, zip_bytes: bytes) -> Tuple[bytes, str]:
        """
        Unpacks a ZIP archive in memory, processes supported files, and rebuilds
        a branded archive: Unbotify_Humanized_Docs_{TIMESTAMP}.zip
        """
        in_stream = io.BytesIO(zip_bytes)
        out_stream = io.BytesIO()

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        archive_name = f"Unbotify_Humanized_Docs_{timestamp}.zip"

        with zipfile.ZipFile(in_stream, "r") as in_zip, \
             zipfile.ZipFile(out_stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out_zip:

            for info in in_zip.infolist():
                if info.is_dir():
                    out_zip.writestr(info, b"")
                    continue

                raw_bytes = in_zip.read(info.filename)
                try:
                    processed_bytes, _ = self.process_file_bytes(info.filename, raw_bytes)
                except Exception:
                    # In case of parsing exception on corrupted file, preserve original
                    processed_bytes = raw_bytes

                clean_info = zipfile.ZipInfo(filename=info.filename, date_time=time.localtime()[:6])
                clean_info.compress_type = zipfile.ZIP_DEFLATED
                out_zip.writestr(clean_info, processed_bytes)

        out_stream.seek(0)
        return out_stream.getvalue(), archive_name

