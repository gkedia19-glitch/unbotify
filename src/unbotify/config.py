"""
Configuration management for Unbotify Engine.
Tagline: "Less formula. More expression."
Supports JSON configs, environment variable overrides (UNBOTIFY_* / TURNITOUT_*),
and dynamic intensity power-curve scaling.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class UnbotifyConfig:
    # Core Pipeline Aggressiveness & Intensity
    INTENSITY: float = 75.0  # User slider (10.0 to 100.0)
    SYNONYM_ALIGNMENT: float = 0.85  # Semantic threshold (0.50 to 1.00)
    RANDOM_ALIGNMENT: bool = False
    STYLE: str = "academic"  # "academic", "conversational", "casual", "technical"
    ZERO_EXPANSION: bool = False  # Strictly 1:1 token parity
    
    # 14 Transformation Stage Toggles
    ENABLE_SYNONYMS: bool = True
    ENABLE_PHRASE_REWRITE: bool = True
    ENABLE_DETERMINER_SWAP: bool = True
    ENABLE_VOICE_TRANSFORM: bool = True
    ENABLE_SENTENCE_FUSION: bool = True
    ENABLE_TRANSITION_INJECT: bool = True
    ENABLE_CLAUSE_REORDER: bool = True
    ENABLE_NOMINALIZATION: bool = True
    ENABLE_APPOSITIVE: bool = True
    ENABLE_DISCOURSE_ROTATE: bool = True
    ENABLE_CONTRACTION: bool = True
    ENABLE_NGRAM_AUDIT: bool = True
    ENABLE_CONCEPTUAL_BRIDGE: bool = False
    ENABLE_INFO_REORDER: bool = True
    ENABLE_SPLIT_COMPOUND: bool = True
    ENABLE_AI_TELL_SCRUBBER: bool = True
    
    # Per-Stage Fire Rates (Base Probabilities)
    SYNONYM_AGGRESSIVENESS: float = 0.65
    VOICE_TRANSFORM_RATE: float = 0.30
    SENTENCE_FUSION_RATE: float = 0.25
    TRANSITION_INJECT_RATE: float = 0.25
    WORD_REORDER_RATE: float = 0.20
    NOMINALIZATION_RATE: float = 0.20
    APPOSITIVE_RATE: float = 0.35
    DISCOURSE_ROTATE_RATE: float = 0.50
    HEDGE_WORD_RATE: float = 0.20
    DETERMINER_RATE: float = 0.35
    
    # Citation Inserter Settings
    ENABLE_CITATIONS: bool = False
    MAX_CITATIONS: int = 0
    CITATION_FORMAT: str = "IEEE [1]"  # "IEEE [1]", "APA", "LaTeX \cite{}"
    CITATION_DISCIPLINE: str = "computer_science"
    
    # Code Comment Engine Settings
    CONVERT_DOCSTRINGS: bool = False
    DEVELOPER_PERSONA: str = "intermediate"  # "beginner", "intermediate", "senior"
    
    # Protected Terms Whitelist
    PROTECTED_TERMS: List[str] = field(default_factory=list)
    SEED: Optional[int] = None

    def get_internal_aggressiveness(self) -> float:
        """
        Non-linear power curve mapping: A = (Intensity / 100)^0.75
        Provides natural sensitivity at mid-range (70-75% maps to ~80% power).
        """
        clamped = max(10.0, min(100.0, self.INTENSITY))
        return (clamped / 100.0) ** 0.75

    @classmethod
    def from_env_or_dict(cls, data: Optional[dict] = None) -> "UnbotifyConfig":
        d = data or {}
        cfg = cls()

        def _get_val(primary_key: str, fallback_key: str):
            v = os.getenv(primary_key)
            if v is not None:
                return v
            return os.getenv(fallback_key)

        def _get_bool(primary_env: str, fallback_env: str, dict_key: str, default: bool) -> bool:
            val = _get_val(primary_env, fallback_env)
            if val is not None:
                return val.lower() in ("true", "1", "yes")
            return bool(d.get(dict_key, default))

        def _get_float(primary_env: str, fallback_env: str, dict_key: str, default: float) -> float:
            val = _get_val(primary_env, fallback_env)
            if val is not None:
                try:
                    return float(val)
                except ValueError:
                    pass
            return float(d.get(dict_key, default))

        def _get_int(primary_env: str, fallback_env: str, dict_key: str, default: int) -> int:
            val = _get_val(primary_env, fallback_env)
            if val is not None:
                try:
                    return int(val)
                except ValueError:
                    pass
            return int(d.get(dict_key, default))

        def _get_str(primary_env: str, fallback_env: str, dict_key: str, default: str) -> str:
            val = _get_val(primary_env, fallback_env)
            if val is not None:
                return val
            return str(d.get(dict_key, default))

        cfg.INTENSITY = _get_float("UNBOTIFY_INTENSITY", "TURNITOUT_INTENSITY", "intensity", 75.0)
        cfg.SYNONYM_ALIGNMENT = _get_float("UNBOTIFY_SYNONYM_ALIGNMENT", "TURNITOUT_SYNONYM_ALIGNMENT", "synonym_alignment", 0.85)
        cfg.RANDOM_ALIGNMENT = _get_bool("UNBOTIFY_RANDOM_ALIGNMENT", "TURNITOUT_RANDOM_ALIGNMENT", "random_alignment", False)
        cfg.STYLE = _get_str("UNBOTIFY_STYLE", "TURNITOUT_STYLE", "style", "academic")
        cfg.ZERO_EXPANSION = _get_bool("UNBOTIFY_ZERO_EXPANSION", "TURNITOUT_ZERO_EXPANSION", "zero_expansion", False)

        cfg.ENABLE_SYNONYMS = _get_bool("UNBOTIFY_SYNONYMS", "TURNITOUT_SYNONYMS", "enable_synonyms", True)
        cfg.ENABLE_PHRASE_REWRITE = _get_bool("UNBOTIFY_PHRASE_REWRITE", "TURNITOUT_PHRASE_REWRITE", "enable_phrase_rewrite", True)
        cfg.ENABLE_DETERMINER_SWAP = _get_bool("UNBOTIFY_DETERMINER_SWAP", "TURNITOUT_DETERMINER_SWAP", "enable_determiner_swap", True)
        cfg.ENABLE_VOICE_TRANSFORM = _get_bool("UNBOTIFY_VOICE_TRANSFORM", "TURNITOUT_VOICE_TRANSFORM", "enable_voice_transform", True)
        cfg.ENABLE_SENTENCE_FUSION = _get_bool("UNBOTIFY_SENTENCE_FUSION", "TURNITOUT_SENTENCE_FUSION", "enable_sentence_fusion", True)
        cfg.ENABLE_TRANSITION_INJECT = _get_bool("UNBOTIFY_TRANSITION_INJECT", "TURNITOUT_TRANSITION_INJECT", "enable_transition_inject", True)
        cfg.ENABLE_CLAUSE_REORDER = _get_bool("UNBOTIFY_CLAUSE_REORDER", "TURNITOUT_CLAUSE_REORDER", "enable_clause_reorder", True)
        cfg.ENABLE_NOMINALIZATION = _get_bool("UNBOTIFY_NOMINALIZATION", "TURNITOUT_NOMINALIZATION", "enable_nominalization", True)
        cfg.ENABLE_APPOSITIVE = _get_bool("UNBOTIFY_APPOSITIVE", "TURNITOUT_APPOSITIVE", "enable_appositive", True)
        cfg.ENABLE_DISCOURSE_ROTATE = _get_bool("UNBOTIFY_DISCOURSE_ROTATE", "TURNITOUT_DISCOURSE_ROTATE", "enable_discourse_rotate", True)
        cfg.ENABLE_CONTRACTION = _get_bool("UNBOTIFY_CONTRACTION", "TURNITOUT_CONTRACTION", "enable_contraction", True)
        cfg.ENABLE_NGRAM_AUDIT = _get_bool("UNBOTIFY_NGRAM_AUDIT", "TURNITOUT_NGRAM_AUDIT", "enable_ngram_audit", True)
        cfg.ENABLE_CONCEPTUAL_BRIDGE = _get_bool("UNBOTIFY_CONCEPTUAL_BRIDGE", "TURNITOUT_CONCEPTUAL_BRIDGE", "enable_conceptual_bridge", False)
        cfg.ENABLE_INFO_REORDER = _get_bool("UNBOTIFY_INFO_REORDER", "TURNITOUT_INFO_REORDER", "enable_info_reorder", True)
        cfg.ENABLE_SPLIT_COMPOUND = _get_bool("UNBOTIFY_SPLIT_COMPOUND", "TURNITOUT_SPLIT_COMPOUND", "enable_split_compound", True)
        cfg.ENABLE_AI_TELL_SCRUBBER = _get_bool("UNBOTIFY_AI_TELL_SCRUBBER", "TURNITOUT_AI_TELL_SCRUBBER", "enable_ai_tell_scrubber", True)

        cfg.VOICE_TRANSFORM_RATE = _get_float("UNBOTIFY_VOICE_RATE", "TURNITOUT_VOICE_RATE", "voice_transform_rate", 0.30)
        cfg.SENTENCE_FUSION_RATE = _get_float("UNBOTIFY_FUSION_RATE", "TURNITOUT_FUSION_RATE", "sentence_fusion_rate", 0.25)
        cfg.TRANSITION_INJECT_RATE = _get_float("UNBOTIFY_TRANSITION_RATE", "TURNITOUT_TRANSITION_RATE", "transition_inject_rate", 0.25)
        cfg.WORD_REORDER_RATE = _get_float("UNBOTIFY_REORDER_RATE", "TURNITOUT_REORDER_RATE", "word_reorder_rate", 0.20)
        cfg.NOMINALIZATION_RATE = _get_float("UNBOTIFY_NOMINAL_RATE", "TURNITOUT_NOMINAL_RATE", "nominalization_rate", 0.20)
        cfg.APPOSITIVE_RATE = _get_float("UNBOTIFY_APPOSITIVE_RATE", "TURNITOUT_APPOSITIVE_RATE", "appositive_rate", 0.35)
        cfg.DISCOURSE_ROTATE_RATE = _get_float("UNBOTIFY_DISCOURSE_RATE", "TURNITOUT_DISCOURSE_RATE", "discourse_rotate_rate", 0.50)

        cfg.ENABLE_CITATIONS = _get_bool("UNBOTIFY_ENABLE_CITATIONS", "TURNITOUT_ENABLE_CITATIONS", "enable_citations", False)
        cfg.MAX_CITATIONS = _get_int("UNBOTIFY_MAX_CITATIONS", "TURNITOUT_MAX_CITATIONS", "max_citations", 0)
        cfg.CITATION_FORMAT = _get_str("UNBOTIFY_CITATION_FORMAT", "TURNITOUT_CITATION_FORMAT", "citation_format", "IEEE [1]")
        cfg.CITATION_DISCIPLINE = _get_str("UNBOTIFY_CITATION_DISCIPLINE", "TURNITOUT_CITATION_DISCIPLINE", "citation_discipline", "computer_science")

        cfg.CONVERT_DOCSTRINGS = _get_bool("UNBOTIFY_CONVERT_DOCSTRINGS", "TURNITOUT_CONVERT_DOCSTRINGS", "convert_docstrings", False)
        cfg.DEVELOPER_PERSONA = _get_str("UNBOTIFY_DEVELOPER_PERSONA", "TURNITOUT_DEVELOPER_PERSONA", "developer_persona", "intermediate")

        terms = d.get("protected_terms", [])
        if isinstance(terms, list):
            cfg.PROTECTED_TERMS = list(terms)
        elif isinstance(terms, str):
            cfg.PROTECTED_TERMS = [t.strip() for t in terms.split(",") if t.strip()]

        if "seed" in d and d["seed"] is not None:
            cfg.SEED = int(d["seed"])

        # Zero-expansion overrides: disable expanding stages
        if cfg.ZERO_EXPANSION:
            cfg.ENABLE_SENTENCE_FUSION = False
            cfg.ENABLE_TRANSITION_INJECT = False
            cfg.ENABLE_APPOSITIVE = False
            cfg.ENABLE_CONCEPTUAL_BRIDGE = False

        return cfg

# Backwards compatibility alias
TurnitoutConfig = UnbotifyConfig
