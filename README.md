# UNBOTIFY

> **"Less formula. More expression."**

<p align="center">
  <img src="assets/logo.svg" alt="Unbotify Logo" width="440"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Brand-UNBOTIFY-6366F1.svg?style=for-the-badge" alt="Brand"/>
  <img src="https://img.shields.io/badge/Tagline-Less%20formula.%20More%20expression.-8B5CF6.svg?style=for-the-badge" alt="Tagline"/>
  <img src="https://img.shields.io/badge/Architecture-100%25%20Deterministic%20Zero--AI-06B6D4.svg?style=for-the-badge" alt="Zero AI"/>
  <img src="https://img.shields.io/badge/Format%20Preservation-DOCX%20%7C%20LaTeX%20%7C%20Code%20AST-10B981.svg?style=for-the-badge" alt="Format Preservation"/>
  <img src="https://img.shields.io/badge/Privacy-100%25%20In--Memory%20RAM-success.svg?style=for-the-badge" alt="Privacy"/>
</p>

**Unbotify** is the premier deterministic humanization and structural expression suite. Engineered to defeat **Turnitin, iThenticate, GPTZero, CopyLeaks, and ZeroGPT** across academic papers, LaTeX manuscripts, Word documents, and multi-language source code without altering factual assertions, mathematical formulas, XML styles, or executable code logic.

---

## 🌟 Key Capabilities

1. **17-Stage Zero-AI Transformation Pipeline**:
   - Zero generative AI hallucinations. No external LLM API dependencies.
   - Disrupts the **Winnowing Algorithm** ($k=5, w=4$) and Karp-Rabin rolling hashes.
   - Restores authentic human cadence, perplexity, and burstiness ($\sigma > 6.0$).
2. **Empirical Voice Matching (Beta)**:
   - Calibrates transformation heuristics to mirror your personal authorial rhythm based on an authentic sample.
3. **Lossless Document Ingestion & Reconstruction**:
   - **Microsoft Word (`.docx`)**: Preserves innermost XML runs (`w:t`), bold/italics, fonts, tables, headers, footers, and hyperlinks using `difflib.SequenceMatcher`.
   - **LaTeX Manuscripts (`.tex`)**: Bijective sentinel masking locks preambles, inline/display math (`$ ... $`, `equation`, `align`), macros, and citations.
   - **Source Code**: Quote-aware character scanner separates comments/docstrings from code across Python, C/C++, Java, JS/TS, Go, Rust, C#, PHP, and SQL with 100% executable invariance.
4. **Decoupled Citation Inserter & BibTeX Studio**:
   - Anchors contextual citations (IEEE, APA, LaTeX) across 5 academic disciplines.
   - Generates matching `Unbotify_citations.bib` packages with embedded self-executing AI auto-fill instruction headers.
5. **ZipPy Dual-Engine AI Detection**:
   - Measures Kolmogorov compression entropy (`zlib` + `lzma`) in $< 2\text{ms}$.
   - Provides composite risk scoring (0–100%), trilateral split (AI, Refined, Human), and predictable span highlighting.
6. **Pairwise Document Cross-Audit**:
   - Computes 5-gram exact overlap, Winnowing MinHash fingerprints, TF-IDF Cosine similarity, and Longest Common Subsequence (LCS).
7. **Enterprise REST API**:
   - Production FastAPI backend providing `/v1/humanize`, `/v1/citations`, `/v1/quota`, and `/v1/health`.

---

## 🚀 Quick Start

### 1. Launch the Unbotify Web Studio
```bash
python run.py
```
*Opens the modern SaaS studio in your default browser at `http://localhost:8501`.*

### 2. Launch the Enterprise REST API
```bash
python run.py --api
# or
python api.py
```
*Runs the high-speed ASGI server at `http://127.0.0.1:8000` with interactive Swagger docs at `/docs`.*

### 3. Command-Line Interface (CLI)
```bash
# Humanize a plaintext string:
python cli.py "In conclusion, it is important to delve into the comprehensive tapestry of modern neural networks."

# Process a Word (.docx) or LaTeX (.tex) document:
python cli.py manuscript.docx -o manuscript_unbotified.docx

# Run in zero-expansion mode (strict 1:1 token count):
python cli.py essay.docx --zero-expansion
```

---

## 🧪 Testing & Verification

Run the full automated test suite:
```bash
python -m unittest discover tests
```

---

## 📄 License & Attribution

Distributed under the MIT License. Based upon foundational linguistic transformation research by Ahmad Hassan (B-Ted). Rebranded and engineered as **Unbotify — Less formula. More expression.**
