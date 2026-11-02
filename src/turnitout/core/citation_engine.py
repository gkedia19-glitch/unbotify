"""
Decoupled Citation Inserter & BibTeX Generator.
Identifies empirical claims, anchors citations across standard academic formats,
and generates self-executing BibTeX packages with AI auto-fill prompt headers.
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from turnitout.core.rules import RuleManager

class CitationEngine:
    AI_AUTOFILL_HEADER = """% ==============================================================================
% [AI AUTO-FILL INSTRUCTIONS (CHATGPT / CLAUDE / GEMINI / DEEPSEEK)]
% ------------------------------------------------------------------------------
% To replace these contextual placeholders with genuine published academic papers,
% simply paste this entire file directly into your AI assistant without any extra prompt!
%
% RULES FOR THE AI:
% 1. Replace every placeholder title, author, journal, and DOI with REAL peer-reviewed papers.
% 2. Retain the EXACT citation keys (e.g. @article{Smith2024GenomicSequences, ...)
%    so they continue to link properly to the citations embedded in the manuscript.
% 3. Match the selected academic discipline: {discipline}
% ==============================================================================
"""

    def __init__(self):
        self.rules = RuleManager.get_instance()

    def detect_discipline(self, text: str) -> str:
        """Score text against taxonomy keywords to auto-detect academic field."""
        lower = text.lower()
        best_discipline = "computer_science"
        max_hits = -1

        for disc_key, disc_data in self.rules.taxonomies.items():
            keywords = disc_data.get("keywords", [])
            hits = sum(1 for kw in keywords if kw.lower() in lower)
            if hits > max_hits:
                max_hits = hits
                best_discipline = disc_key

        return best_discipline

    def generate_bib_entry(self, key: str, title: str, author_last: str, author_init: str, venue: str, year: int = 2024) -> str:
        return f"""@article{{{key},
  author  = {{{author_last}, {author_init}}},
  title   = {{A study on {title.lower()}}},
  journal = {{{venue}}},
  year    = {{{year}}},
  volume  = {{42}},
  number  = {{1}},
  pages   = {{100--118}},
  doi     = {{10.1016/j.academic.{year}.001}}
}}
"""

    def insert_citations(
        self,
        text: str,
        citation_count: int = 2,
        citation_format: str = "IEEE [1]",
        discipline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inserts contextual citations into text and generates matching BibTeX entries.
        """
        if not discipline or discipline == "auto" or discipline not in self.rules.taxonomies:
            discipline = self.detect_discipline(text)

        tax_data = self.rules.taxonomies.get(discipline, {})
        disc_name = tax_data.get("discipline", discipline.replace("_", " ").title())
        venues = tax_data.get("venues", ["Journal of Academic Research", "IEEE Transactions"])
        authors = tax_data.get("authors", [("Smith", "R. M."), ("Johnson", "A. K."), ("Williams", "T. L.")])
        keywords = tax_data.get("keywords", ["methodology", "empirical analysis", "framework"])

        # Split into sentences using punctuation boundaries
        sentence_splits = re.split(r"(?<=[.!?])\s+", text)
        eligible_indices = []

        # Identify candidate sentences (substantive claims, not headers or titles)
        for idx, sentence in enumerate(sentence_splits):
            s_clean = sentence.strip()
            # Shield short sentences, questions, or section indicators
            if len(s_clean) >= 60 and not s_clean.endswith("?") and not any(s_clean.lower().startswith(p) for p in ["abstract", "introduction", "conclusion", "table", "figure"]):
                eligible_indices.append(idx)

        if not eligible_indices:
            eligible_indices = list(range(len(sentence_splits)))

        num_citations = min(citation_count, len(eligible_indices))
        if num_citations <= 0:
            return {
                "cited_text": text,
                "bib_text": "",
                "citations_meta": [],
                "citation_count": 0,
                "discipline": disc_name
            }

        # Select evenly spaced sentences from eligible candidates
        step = max(1, len(eligible_indices) // num_citations)
        selected_indices = [eligible_indices[i * step] for i in range(num_citations)]

        bib_entries = []
        citations_meta = []
        cited_sentences = list(sentence_splits)

        for c_idx, target_s_idx in enumerate(selected_indices):
            orig_s = cited_sentences[target_s_idx].strip()
            author_last, author_init = authors[c_idx % len(authors)]
            venue = venues[c_idx % len(venues)]
            kw = keywords[c_idx % len(keywords)]
            clean_kw = "".join(w.capitalize() for w in kw.split()[:2])
            cite_key = f"{author_last}2024{clean_kw}"

            # Format marker
            if "IEEE" in citation_format:
                marker = f" [{c_idx + 1}]"
            elif "APA" in citation_format:
                marker = f" ({author_last} et al., 2024)"
            elif "LaTeX" in citation_format:
                marker = f" \\cite{{{cite_key}}}"
            else:
                marker = f" [{c_idx + 1}]"

            # Insert before terminal punctuation
            if orig_s[-1] in ".!?":
                cited_s = orig_s[:-1].rstrip() + marker + orig_s[-1]
            else:
                cited_s = orig_s + marker

            cited_sentences[target_s_idx] = cited_s

            bib_entry = self.generate_bib_entry(
                key=cite_key,
                title=f"{clean_kw} and related advancements",
                author_last=author_last,
                author_init=author_init,
                venue=venue,
                year=2024
            )
            bib_entries.append(bib_entry)

            citations_meta.append({
                "index": c_idx + 1,
                "key": cite_key,
                "marker": marker.strip(),
                "author": f"{author_last}, {author_init}",
                "venue": venue,
                "sentence_preview": cited_s[:80] + "..."
            })

        full_bib_text = self.AI_AUTOFILL_HEADER.replace("{discipline}", disc_name) + "\n" + "\n".join(bib_entries)
        full_cited_text = " ".join(cited_sentences)

        return {
            "cited_text": full_cited_text,
            "bib_text": full_bib_text,
            "citations_meta": citations_meta,
            "citation_count": num_citations,
            "discipline": disc_name
        }
