"""
UNBOTIFY — Modern Premium SaaS Application
Tagline: "Less formula. More expression."
100% Deterministic Zero-AI Humanizer, Detection Evasion & Code Comment Suite.
"""

import sys
import os
import time
import io
import difflib
import streamlit as st

# Ensure src is on python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from unbotify.config import UnbotifyConfig
from unbotify.core.modifier import TextModifier
from unbotify.core.doc_processor import DocumentProcessor
from unbotify.core.citation_engine import CitationEngine
from unbotify.core.ai_detector import ZipPyDetector
from unbotify.core.similarity_checker import SimilarityChecker
from unbotify.core.parsers.code_parser import CodeCommentParser

# ------------------------------------------------------------------------------
# Streamlit Page Config & Custom Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Unbotify — Less formula. More expression.",
    page_icon="assets/favicon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling (Modern Premium SaaS Aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Branded Header Banner */
    .hero-banner {
        background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, rgba(14, 19, 32, 0) 50%),
                    linear-gradient(135deg, #0A0D16 0%, #111726 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 28px 36px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .brand-row {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 8px;
    }
    .brand-mark {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: linear-gradient(135deg, #6366F1, #8B5CF6, #06B6D4);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        background: linear-gradient(90deg, #FFFFFF 20%, #CBD5E1 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .hero-tagline {
        font-size: 1.05rem;
        font-weight: 600;
        color: #A5B4FC;
        letter-spacing: 0.02em;
        margin-top: 2px;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        max-width: 860px;
        line-height: 1.55;
        margin-top: 10px;
    }

    /* Metric Badges */
    .badge-bar {
        display: flex;
        gap: 10px;
        margin-top: 18px;
        flex-wrap: wrap;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #E2E8F0;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }
    .badge-pill:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
    }
    .badge-accent {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #A5B4FC;
    }

    /* Telemetry Cards */
    .metric-card {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.76rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
        font-weight: 600;
    }

    /* Diff Highlight Spans */
    .diff-del {
        background-color: rgba(239, 68, 68, 0.18);
        color: #F87171;
        text-decoration: line-through;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 4px;
    }
    .diff-ins {
        background-color: rgba(16, 185, 129, 0.18);
        color: #34D399;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Footer styling */
    .footer-bar {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px 0;
        margin-top: 40px;
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
    }
    .footer-bar b {
        color: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Sidebar Controls & Global State
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="36" height="36">
            <rect width="64" height="64" rx="14" fill="#0E1320"/>
            <path d="M 18 16 L 18 36 C 18 45 25 50 34 50 C 43 50 50 44 50 35 L 50 26" 
                  fill="none" stroke="#818CF8" stroke-width="6.5" stroke-linecap="round"/>
            <path d="M 44 14 Q 50 20 44 26 Q 38 20 44 14 Z" fill="#FB923C"/>
        </svg>
        <div>
            <div style="font-size: 1.25rem; font-weight: 900; letter-spacing: -0.02em; color: #FFFFFF;">UNBOTIFY</div>
            <div style="font-size: 0.72rem; color: #818CF8; font-weight: 600;">Less formula. More expression.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Engine Parameters")
    intensity = st.slider(
        "Humanization Intensity (%)",
        min_value=10.0,
        max_value=100.0,
        value=75.0,
        step=5.0,
        help="Controls the density of sentence reordering, voice inversion, and rare academic synonym selection."
    )

    # Calculate and display non-linear power curve
    internal_agg = (intensity / 100.0) ** 0.75
    st.caption(f"⚡ Effective Aggressiveness: **{internal_agg*100:.1f}%** (Power Curve: $I^{{0.75}}$)")

    style_choice = st.selectbox(
        "Writing Register",
        ["academic", "conversational", "casual", "technical"],
        index=0,
        help="Sets target vocabulary tone, contraction expansions, and register formality."
    )

    zero_expansion = st.toggle(
        "🔒 Zero-Expansion Mode (1:1 Words)",
        value=False,
        help="Strictly enforces 1:1 token parity. Disables additive fusions and transitions to guarantee 0 added words for strict limit essays."
    )

    st.markdown("---")
    st.markdown("### 🛡️ Protected Terms Whitelist")
    protected_terms_input = st.text_area(
        "Preserve verbatim (comma-separated):",
        value="CRISPR-Cas9, TensorFlow, PyTorch, Navier-Stokes, O(N log N)",
        height=80,
        help="Mathematical constants, variable names, or technical terms that must NEVER be altered."
    )
    user_protected = [t.strip() for t in protected_terms_input.split(",") if t.strip()]

    st.markdown("---")
    st.markdown("### ℹ️ Unbotify Core Architecture")
    st.markdown("""
    - **Philosophy:** 100% Deterministic Rule Engine
    - **Tagline:** Less formula. More expression.
    - **Anti-Plagiarism:** $k=5, w=4$ Winnowing Disruption
    - **Format Safety:** In-Place DOCX & LaTeX Math Masking
    - **Execution:** 100% In-Memory RAM (Zero Cache Leaks)
    """)

# ------------------------------------------------------------------------------
# Main Header Banner
# ------------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="brand-row">
        <div>
            <div class="hero-title">UNBOTIFY</div>
            <div class="hero-tagline">Less formula. More expression.</div>
        </div>
    </div>
    <div class="hero-subtitle">
        The premier deterministic humanization and structural expression suite.
        Transform predictable AI patterns into authentic, fluid scholarly prose across academic manuscripts,
        LaTeX papers, Word documents, and source code without altering equations, facts, or layout.
    </div>
    <div class="badge-bar">
        <span class="badge-pill badge-accent">✨ Less formula. More expression.</span>
        <span class="badge-pill">🔒 100% Zero Generative AI</span>
        <span class="badge-pill">⚡ Sub-50ms Processing</span>
        <span class="badge-pill">📄 In-Place DOCX & LaTeX Math Preservation</span>
        <span class="badge-pill">💻 Multi-Language Code Comment AST</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Navigation Tabs
# ------------------------------------------------------------------------------
tab_humanizer, tab_code, tab_citations, tab_checker, tab_similarity, tab_api = st.tabs([
    "⚡ Expressive Humanizer",
    "💻 Code Comment Studio",
    "📜 Citation & BibTeX Studio",
    "🔍 Unbotify AI Signature Audit",
    "⚖️ Pairwise Similarity Audit",
    "🌐 Enterprise REST API"
])

# ==============================================================================
# TAB 1: EXPRESSIVE HUMANIZER
# ==============================================================================
with tab_humanizer:
    col_input, col_output = st.columns([1, 1])

    # Sample Academic Text
    SAMPLE_AI_TEXT = (
        "In conclusion, it is important to delve into the comprehensive tapestry of modern neural networks. "
        "This study plays a pivotal role in illustrating that artificial intelligence stands as a testament to human innovation. "
        "Furthermore, the interplay between stochastic optimization and computational scalability provides a robust framework "
        "for subsequent empirical inquiries. In order to delve into the multifaceted dimensions of this phenomenon, "
        "previous studies have shown that distributed clusters achieve significant acceleration."
    )

    with col_input:
        st.markdown("#### 📝 Input Text or Document Upload")

        input_mode = st.radio("Input Source:", ["Plaintext Input", "File Upload (.docx, .tex, .md, .zip)"], horizontal=True)

        if input_mode == "Plaintext Input":
            user_text = st.text_area(
                "Enter text to humanize:",
                value=SAMPLE_AI_TEXT,
                height=260,
                key="humanizer_input_text"
            )
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                btn_humanize = st.button("🚀 Unbotify Text Now", type="primary", use_container_width=True)
            with col_b2:
                if st.button("🔄 Reset to Benchmark AI Sample", use_container_width=True):
                    st.rerun()
            uploaded_file = None
        else:
            uploaded_file = st.file_uploader(
                "Choose document to process:",
                type=["docx", "tex", "md", "txt", "zip"],
                help="Supported formats: Word (.docx), LaTeX (.tex), Markdown (.md), Plaintext (.txt), or ZIP archives."
            )
            btn_humanize = st.button("🚀 Process Document with Unbotify", type="primary", use_container_width=True)
            user_text = ""

        # Advanced 14 Knobs Accordion
        with st.expander("🛠️ Advanced Transformation Knobs (14 Operators)", expanded=False):
            st.caption("Fine-tune individual linguistic operators. Zero-expansion mode automatically disables word-inflating stages.")
            c1, c2, c3 = st.columns(3)
            with c1:
                t_syn = st.checkbox("1. Synonym Swapping", value=True)
                t_phrase = st.checkbox("2. Phrase Rewriting (AI Scrubber)", value=True)
                t_det = st.checkbox("3. Determiner Swapping", value=True)
                t_voice = st.checkbox("4. Voice Inversion (Active↔Passive)", value=True)
                t_ngram = st.checkbox("12. Residual N-Gram Audit", value=True)
            with c2:
                t_fusion = st.checkbox("5. Sentence Fusion (Anti-Burstiness)", value=not zero_expansion)
                t_trans = st.checkbox("6. Transition Injection", value=not zero_expansion)
                t_reorder = st.checkbox("7. Clause Topicalization", value=True)
                t_nom = st.checkbox("8. Nominalization (Verb↔Noun)", value=True)
                t_split = st.checkbox("Compound Clause Splitting", value=True)
            with c3:
                t_appositive = st.checkbox("9. Appositive Insertion", value=not zero_expansion)
                t_discourse = st.checkbox("10. Discourse Marker Rotation", value=True)
                t_contraction = st.checkbox("11. Contraction Swapping", value=True)
                t_bridge = st.checkbox("13. Conceptual Bridging", value=False)
                t_adjunct = st.checkbox("14. Info Reordering (Given-Before-New)", value=True)

        with st.expander("🎙️ Empirical Voice Matching (Beta)", expanded=False):
            voice_matching_on = st.toggle("Enable Empirical Voice Calibration", value=False, help="Calibrate sentence length variance, clause depth, and contraction frequency against an authentic writing sample.")
            voice_sample_input = st.text_area(
                "Paste an authentic reference writing sample (100+ words):",
                value="",
                height=100,
                help="Unbotify analyzes the standard deviation of sentence lengths and calibrates probabilities to match your personal authorial cadence."
            )

    with col_output:
        st.markdown("#### 🎯 Unbotified Expression & Telemetry")

        if btn_humanize:
            start_t = time.time()
            config = UnbotifyConfig(
                INTENSITY=intensity,
                STYLE=style_choice,
                ZERO_EXPANSION=zero_expansion,
                PROTECTED_TERMS=user_protected,
                ENABLE_SYNONYMS=t_syn,
                ENABLE_PHRASE_REWRITE=t_phrase,
                ENABLE_DETERMINER_SWAP=t_det,
                ENABLE_VOICE_TRANSFORM=t_voice,
                ENABLE_SENTENCE_FUSION=t_fusion and not zero_expansion,
                ENABLE_TRANSITION_INJECT=t_trans and not zero_expansion,
                ENABLE_CLAUSE_REORDER=t_reorder,
                ENABLE_NOMINALIZATION=t_nom,
                ENABLE_APPOSITIVE=t_appositive and not zero_expansion,
                ENABLE_DISCOURSE_ROTATE=t_discourse,
                ENABLE_NGRAM_AUDIT=t_ngram,
                ENABLE_SPLIT_COMPOUND=t_split,
                ENABLE_INFO_REORDER=t_adjunct,
                ENABLE_CONTRACTION=t_contraction,
                ENABLE_CONCEPTUAL_BRIDGE=t_bridge and not zero_expansion
            )

            if input_mode == "Plaintext Input" and user_text.strip():
                modifier = TextModifier(config)
                if voice_matching_on and voice_sample_input.strip():
                    modifier.calibrate_voice_from_sample(voice_sample_input)
                humanized_result = modifier.modify_text(user_text)
                elapsed_ms = (time.time() - start_t) * 1000.0

                orig_words = len(user_text.split())
                new_words = len(humanized_result.split())
                telemetry = modifier.get_telemetry()

                # Metric Cards
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{new_words}</div><div class="metric-label">Word Count (Delta: {new_words - orig_words:+d})</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{telemetry["total_modifications"]}</div><div class="metric-label">Total Transforms</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{telemetry["synonym_swaps"]}</div><div class="metric-label">Synonym Swaps</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{elapsed_ms:.1f}ms</div><div class="metric-label">Latency</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.text_area("Unbotified Output:", value=humanized_result, height=200, key="humanized_output_area")

                # Visual Diff View
                with st.expander("🔍 Interactive Color-Coded Diff View", expanded=True):
                    words_orig = user_text.split()
                    words_new = humanized_result.split()
                    matcher = difflib.SequenceMatcher(None, words_orig, words_new)
                    diff_html = []
                    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                        if tag == 'equal':
                            diff_html.append(" ".join(words_orig[i1:i2]))
                        elif tag == 'replace':
                            diff_html.append(f'<span class="diff-del">{" ".join(words_orig[i1:i2])}</span><span class="diff-ins">{" ".join(words_new[j1:j2])}</span>')
                        elif tag == 'delete':
                            diff_html.append(f'<span class="diff-del">{" ".join(words_orig[i1:i2])}</span>')
                        elif tag == 'insert':
                            diff_html.append(f'<span class="diff-ins">{" ".join(words_new[j1:j2])}</span>')
                    st.markdown(" ".join(diff_html), unsafe_allow_html=True)

                # Instant AI Neutralization Verification
                ai_check_result = ZipPyDetector.analyze(humanized_result)
                risk_val = ai_check_result["risk_score"]
                badge_bg = "#10B981" if risk_val == 0.0 else ("#F59E0B" if risk_val <= 30.0 else "#EF4444")
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid {badge_bg}; border-radius: 12px; padding: 14px 20px; margin: 12px 0; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 800; color: {badge_bg}; font-size: 1.25rem;">{risk_val}% AI</span>
                        <span style="font-size: 0.95rem; font-weight: 600; color: #E2E8F0; margin-left: 8px;">— {ai_check_result['classification']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8;">
                        Human Authenticity: <b>{ai_check_result['trilateral_split']['human_written']}%</b> | Entropy: <b>{ai_check_result['entropy_score']}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.download_button(
                    label="💾 Download Unbotified Text (.txt)",
                    data=humanized_result,
                    file_name="Unbotify_Humanized.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            elif input_mode == "File Upload (.docx, .tex, .md, .zip)" and uploaded_file is not None:
                processor = DocumentProcessor(config)
                if voice_matching_on and voice_sample_input.strip():
                    processor.modifier.calibrate_voice_from_sample(voice_sample_input)
                raw_bytes = uploaded_file.read()
                filename = uploaded_file.name

                if filename.lower().endswith(".zip"):
                    out_bytes, out_name = processor.process_zip_package(raw_bytes)
                    mime = "application/zip"
                else:
                    out_bytes, mime = processor.process_file_bytes(filename, raw_bytes)
                    base, ext = os.path.splitext(filename)
                    out_name = f"Unbotify_Processed_{base}{ext}"

                st.success(f"✓ Successfully processed document: **{filename}**")
                telemetry = processor.modifier.get_telemetry()

                m1, m2 = st.columns(2)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{telemetry["total_modifications"]}</div><div class="metric-label">Total Transforms Applied</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-val">{len(out_bytes):,} B</div><div class="metric-label">Output Archive Size</div></div>', unsafe_allow_html=True)

                st.download_button(
                    label=f"💾 Download Processed Document ({out_name})",
                    data=out_bytes,
                    file_name=out_name,
                    mime=mime,
                    use_container_width=True
                )
        else:
            st.info("👈 Enter text or upload a document and click **Unbotify Text Now** to transform formulaic AI prose into authentic expression.")

# ==============================================================================
# TAB 2: CODE COMMENT & DOCSTRING STUDIO
# ==============================================================================
with tab_code:
    st.markdown("### 💻 AST String-Aware Code Comment Studio")
    st.markdown("""
    Humanize AI-generated comments and docstrings across **Python, C/C++, Java, JavaScript, TypeScript, Go, Rust, and SQL**
    while preserving **100% of executable logic, function signatures, variables, and indentation**.
    """)

    col_c_in, col_c_out = st.columns([1, 1])

    SAMPLE_PYTHON_CODE = '''import numpy as np

def compute_loss(y_true, y_pred):
    """
    Computes the mean squared error loss between true and predicted values.
    It is of paramount importance to delve into the comprehensive error vectors.
    """
    # checks if list is empty
    if len(y_true) == 0:
        return 0.0

    # loops through all items and calculates score
    squared_diff = (np.array(y_true) - np.array(y_pred)) ** 2
    return float(np.mean(squared_diff))
'''

    with col_c_in:
        code_lang = st.selectbox("Programming Language:", ["python", "c", "cpp", "java", "javascript", "typescript", "go", "rust", "csharp", "sql", "shell"])
        persona = st.selectbox("Developer Persona:", ["intermediate", "beginner", "senior"], index=0, help="Adapts comment style and vocabulary.")
        convert_docs = st.checkbox('Convert AI Triple-Quoted Docstrings (""") to # Comments', value=True)

        input_code = st.text_area("Source Code:", value=SAMPLE_PYTHON_CODE, height=280)
        btn_code = st.button("⚡ Unbotify Code Comments", type="primary", use_container_width=True)

    with col_c_out:
        if btn_code and input_code.strip():
            cfg_code = UnbotifyConfig(INTENSITY=intensity, DEVELOPER_PERSONA=persona, CONVERT_DOCSTRINGS=convert_docs)
            modifier_code = TextModifier(cfg_code)

            transformed_code = CodeCommentParser.process_code(
                code=input_code,
                lang=code_lang,
                persona=persona,
                convert_docstrings=convert_docs,
                transform_fn=modifier_code.modify_text
            )

            st.success("✓ Code humanized with 100% executable syntax protection!")
            st.code(transformed_code, language=code_lang)

            st.download_button(
                label="💾 Download Unbotified Code",
                data=transformed_code,
                file_name=f"unbotified_code.{code_lang if code_lang != 'python' else 'py'}",
                use_container_width=True
            )
        else:
            st.info("Enter source code and click **Unbotify Code Comments** to inspect the transformed syntax.")

# ==============================================================================
# TAB 3: CITATION INSERTER & BIBTEX STUDIO
# ==============================================================================
with tab_citations:
    st.markdown("### 📜 Decoupled Academic Citation Inserter & BibTeX Studio")
    st.markdown("Contextually injects peer-reviewed citation anchors and generates self-executing BibTeX companion packages.")

    col_cit_in, col_cit_out = st.columns([1, 1])

    SAMPLE_CITATION_TEXT = (
        "Machine learning architectures provide notable improvements in analyzing genomic sequences "
        "and predicting protein tertiary structures. Furthermore, stochastic optimization algorithms "
        "guarantee convergence under non-convex loss surfaces."
    )

    with col_cit_in:
        cit_text = st.text_area("Manuscript Text:", value=SAMPLE_CITATION_TEXT, height=180)
        c_count = st.slider("Citation Count:", min_value=1, max_value=10, value=2)
        c_fmt = st.selectbox("Citation Format:", ["IEEE [1]", "APA (Author, Year)", "LaTeX \\cite{key}"])
        c_disc = st.selectbox(
            "Academic Discipline:",
            ["auto", "computer_science", "engineering_physics", "mathematics_statistics", "quantitative_finance", "medical_life_sciences"],
            format_func=lambda x: "✨ Auto-Detect Field" if x == "auto" else x.replace("_", " ").title()
        )
        btn_cite = st.button("📚 Insert Citations & Build BibTeX", type="primary", use_container_width=True)

    with col_cit_out:
        if btn_cite and cit_text.strip():
            c_engine = CitationEngine()
            c_result = c_engine.insert_citations(
                text=cit_text,
                citation_count=c_count,
                citation_format=c_fmt,
                discipline=c_disc
            )

            st.markdown(f"**Discipline Resolved:** `{c_result['discipline']}` | **Citations Inserted:** `{c_result['citation_count']}`")
            st.text_area("Cited Manuscript:", value=c_result["cited_text"], height=120)
            st.text_area("Generated BibTeX Package (with AI Auto-Fill Prompt Header):", value=c_result["bib_text"], height=160)

            st.download_button(
                label="💾 Download Unbotify citations.bib Package",
                data=c_result["bib_text"],
                file_name="Unbotify_citations.bib",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Configure citation parameters and click **Insert Citations & Build BibTeX**.")

# ==============================================================================
# TAB 4: UNBOTIFY AI SIGNATURE CHECKER
# ==============================================================================
with tab_checker:
    st.markdown("### 🔍 Unbotify Dual-Engine Entropic AI Detector")
    st.markdown("Measures Kolmogorov compression entropy using `zlib` and `lzma` to score AI predictability in milliseconds.")

    col_chk_in, col_chk_out = st.columns([1, 1])

    with col_chk_in:
        chk_input = st.text_area(
            "Enter text to evaluate for AI footprints:",
            value=SAMPLE_AI_TEXT,
            height=200
        )
        btn_check = st.button("📊 Audit AI Probability", type="primary", use_container_width=True)

    with col_chk_out:
        if btn_check and chk_input.strip():
            res = ZipPyDetector.analyze(chk_input)

            # Risk Score Banner
            risk = res["risk_score"]
            risk_color = "#EF4444" if risk > 65 else ("#F59E0B" if risk >= 35 else "#10B981")

            st.markdown(f"""
            <div style="background: rgba(17,24,39,0.7); border: 2px solid {risk_color}; border-radius: 14px; padding: 20px; text-align: center; margin-bottom: 16px;">
                <div style="font-size: 2.3rem; font-weight: 800; color: {risk_color};">{risk}%</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #E2E8F0;">{res["classification"]}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">Normalized Compression Entropy: {res["entropy_score"]} | Latency: {res["latency_ms"]}ms</div>
            </div>
            """, unsafe_allow_html=True)

            # Trilateral Split
            st.markdown("##### Trilateral Categorization Breakdown:")
            ts = res["trilateral_split"]
            st.progress(ts["ai_generated"] / 100.0, text=f"AI-Generated: {ts['ai_generated']}%")
            st.progress(ts["ai_refined"] / 100.0, text=f"AI-Refined: {ts['ai_refined']}%")
            st.progress(ts["human_written"] / 100.0, text=f"Human-Written: {ts['human_written']}%")

            if res["highlighted_spans"]:
                st.markdown("##### ⚠️ Predictable Spans Requiring Attention:")
                for item in res["highlighted_spans"]:
                    st.warning(f"**[{item['risk']}% Risk - {item['status']}]**: \"{item['sentence']}\"")
        else:
            st.info("Enter text to run the real-time Unbotify compression entropy scanner.")

# ==============================================================================
# TAB 5: PAIRWISE SIMILARITY AUDIT
# ==============================================================================
with tab_similarity:
    st.markdown("### ⚖️ Multi-Pass Pairwise Similarity & Plagiarism Audit")
    st.markdown("Simultaneously audits **5-gram exact overlap, Winnowing MinHash ($k=5, w=4$), TF-IDF Cosine, and LCS**.")

    col_sim_a, col_sim_b = st.columns([1, 1])

    with col_sim_a:
        st.markdown("##### Document A (Original / Source)")
        doc_a = st.text_area("Document A Content:", value=SAMPLE_AI_TEXT, height=180, key="sim_doc_a")
    with col_sim_b:
        st.markdown("##### Document B (Paraphrased / Modified)")
        doc_b = st.text_area(
            "Document B Content:",
            value="To wrap up, we look closely at the broad range of modern neural networks. This study clearly shows that artificial intelligence reflects human innovation. Also, balancing stochastic optimization gives a solid basis for subsequent empirical inquiries.",
            height=180,
            key="sim_doc_b"
        )

    if st.button("⚖️ Run Full Cross-Audit Comparison", type="primary", use_container_width=True):
        sim_res = SimilarityChecker.compare_documents(doc_a, doc_b)

        c_metric = sim_res["composite_score"]
        c_color = "#10B981" if c_metric < 15 else ("#F59E0B" if c_metric <= 40 else "#EF4444")

        st.markdown(f"""
        <div style="background: rgba(17,24,39,0.7); border: 2px solid {c_color}; border-radius: 14px; padding: 20px; text-align: center; margin: 16px 0;">
            <div style="font-size: 2.3rem; font-weight: 800; color: {c_color};">{c_metric}% Composite Similarity</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #E2E8F0;">{sim_res["risk_tier"]}</div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-val">{sim_res["metrics"]["ngram_overlap_pct"]}%</div><div class="metric-label">5-Gram Overlap</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-val">{sim_res["metrics"]["winnowing_fingerprint_pct"]}%</div><div class="metric-label">Winnowing MinHash</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-val">{sim_res["metrics"]["tfidf_cosine_pct"]}%</div><div class="metric-label">TF-IDF Cosine</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><div class="metric-val">{sim_res["metrics"]["lcs_structural_pct"]}%</div><div class="metric-label">LCS Structural Drift</div></div>', unsafe_allow_html=True)

        if sim_res["matching_snippets"]:
            st.markdown("##### 🔗 Exact Matching 5-Gram Snippets Caught by Winnowing:")
            for snip in sim_res["matching_snippets"]:
                st.code(snip, language="text")

# ==============================================================================
# TAB 6: ENTERPRISE REST API & LOCAL INTEGRATION
# ==============================================================================
with tab_api:
    st.markdown("### 🌐 Unbotify Enterprise REST API Documentation & Local Server")
    st.markdown("""
    Integrate Unbotify directly into programmatic pipelines, CI/CD runners, or custom LMS portals.
    The local FastAPI server implements the complete specification from `ENTERPRISE_API.md`.
    """)

    st.markdown("#### 🚀 Starting the Local API Server")
    st.code("python api.py", language="bash")

    st.markdown("#### 📡 Endpoint Reference & Curl Samples")

    t_api_1, t_api_2, t_api_3 = st.tabs(["POST /v1/humanize", "POST /v1/citations", "GET /v1/health"])

    with t_api_1:
        st.code("""curl -X POST http://127.0.0.1:8000/v1/humanize \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Furthermore, our experimental findings demonstrate that deep learning models frequently introduce formulaic syntax.",
    "intensity": 75.0,
    "style": "academic",
    "enable_synonyms": true,
    "enable_voice_transform": true
  }'""", language="bash")

    with t_api_2:
        st.code("""curl -X POST http://127.0.0.1:8000/v1/citations \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Machine learning architectures provide notable improvements in analyzing genomic sequences and predicting protein structures.",
    "citation_count": 2,
    "citation_format": "IEEE [1]",
    "discipline": "medical_life_sciences"
  }'""", language="bash")

    with t_api_3:
        st.code("curl -X GET http://127.0.0.1:8000/v1/health", language="bash")

# ------------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------------
st.markdown("""
<div class="footer-bar">
    <b>UNBOTIFY</b> • Less formula. More expression. • 100% In-Memory RAM Execution • Zero Data Retention • Free & Open Source
</div>
""", unsafe_allow_html=True)
