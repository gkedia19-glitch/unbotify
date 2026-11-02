"""
Unbotify Enterprise REST API Implementation (FastAPI).
Tagline: "Less formula. More expression."
High-Throughput Programmatic AI Footprint Erasure & Academic Citation Engine.
"""

import time
import os
import sys
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Ensure src is on python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from unbotify.config import UnbotifyConfig
from unbotify.core.modifier import TextModifier
from unbotify.core.citation_engine import CitationEngine
from unbotify.core.ai_detector import ZipPyDetector

app = FastAPI(
    title="Unbotify Enterprise REST API",
    description="High-Throughput Deterministic Humanization & Structural Expression Suite. Less formula. More expression.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Request & Response Models
# ------------------------------------------------------------------------------
class HumanizeRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Plain-text string to humanize")
    intensity: float = Field(default=75.0, ge=10.0, le=100.0)
    style: str = Field(default="academic")
    protected_terms: List[str] = Field(default_factory=list)
    enable_synonyms: bool = True
    synonym_alignment: float = Field(default=0.85, ge=0.50, le=1.00)
    random_alignment: bool = False
    enable_phrase_rewrite: bool = True
    enable_determiner_swap: bool = True
    enable_voice_transform: bool = True
    enable_sentence_fusion: bool = True
    enable_transition_inject: bool = True
    enable_clause_reorder: bool = True
    enable_nominalization: bool = True
    enable_appositive: bool = True
    enable_discourse_rotate: bool = True
    enable_contraction: bool = True
    enable_ngram_audit: bool = True
    enable_conceptual_bridge: bool = False
    enable_info_reorder: bool = True
    enable_split_compound: bool = True
    enable_ai_tell_scrubber: bool = True
    enable_citations: bool = False
    max_citations: int = 0
    citation_format: str = "IEEE [1]"
    citation_discipline: str = "computer_science"
    convert_docstrings: bool = False
    seed: Optional[int] = None

class HumanizeResponse(BaseModel):
    success: bool
    humanized_text: str
    words_processed: int
    modifications_count: int
    latency_ms: float
    citation_count: int
    bib_text: str
    telemetry: dict

class CitationRequest(BaseModel):
    text: str = Field(..., min_length=10)
    citation_count: int = Field(default=2, ge=1, le=50)
    citation_format: str = "IEEE [1]"
    discipline: Optional[str] = "computer_science"

class CitationResponse(BaseModel):
    success: bool
    cited_text: str
    bib_text: str
    citation_count: int
    words_processed: int
    latency_ms: float

# ------------------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------------------
@app.get("/v1/health")
def health():
    return {
        "status": "healthy",
        "engine": "Unbotify Core 2.0",
        "brand": "Unbotify",
        "tagline": "Less formula. More expression.",
        "engine_ready": True,
        "version": "2.0.0+local",
        "timestamp": time.time()
    }

@app.get("/v1/quota")
def quota(x_api_key: Optional[str] = Header(None)):
    return {
        "client_name": "Personal Developer Workstation",
        "email": "developer@unbotify.internal",
        "is_active": True,
        "quota_limit": 1000000,
        "words_used": 1420,
        "words_remaining": 998580,
        "rate_per_1k": 0.00,
        "unlimited": True,
        "expires_at": None
    }

@app.post("/v1/humanize", response_model=HumanizeResponse)
def humanize_endpoint(req: HumanizeRequest, x_api_key: Optional[str] = Header(None)):
    start = time.time()
    config = UnbotifyConfig(
        INTENSITY=req.intensity,
        STYLE=req.style,
        PROTECTED_TERMS=req.protected_terms,
        ENABLE_SYNONYMS=req.enable_synonyms,
        SYNONYM_ALIGNMENT=req.synonym_alignment,
        RANDOM_ALIGNMENT=req.random_alignment,
        ENABLE_PHRASE_REWRITE=req.enable_phrase_rewrite,
        ENABLE_DETERMINER_SWAP=req.enable_determiner_swap,
        ENABLE_VOICE_TRANSFORM=req.enable_voice_transform,
        ENABLE_SENTENCE_FUSION=req.enable_sentence_fusion,
        ENABLE_TRANSITION_INJECT=req.enable_transition_inject,
        ENABLE_CLAUSE_REORDER=req.enable_clause_reorder,
        ENABLE_NOMINALIZATION=req.enable_nominalization,
        ENABLE_APPOSITIVE=req.enable_appositive,
        ENABLE_DISCOURSE_ROTATE=req.enable_discourse_rotate,
        ENABLE_CONTRACTION=req.enable_contraction,
        ENABLE_NGRAM_AUDIT=req.enable_ngram_audit,
        ENABLE_CONCEPTUAL_BRIDGE=req.enable_conceptual_bridge,
        ENABLE_INFO_REORDER=req.enable_info_reorder,
        ENABLE_SPLIT_COMPOUND=req.enable_split_compound,
        ENABLE_AI_TELL_SCRUBBER=req.enable_ai_tell_scrubber,
        ENABLE_CITATIONS=req.enable_citations,
        MAX_CITATIONS=req.max_citations,
        CITATION_FORMAT=req.citation_format,
        CITATION_DISCIPLINE=req.citation_discipline,
        CONVERT_DOCSTRINGS=req.convert_docstrings,
        SEED=req.seed
    )

    modifier = TextModifier(config)
    humanized = modifier.modify_text(req.text)
    telemetry = modifier.get_telemetry()
    words_count = len(req.text.split())

    bib_text = ""
    if req.enable_citations and req.max_citations > 0:
        c_engine = CitationEngine()
        c_res = c_engine.insert_citations(
            text=req.text,
            citation_count=req.max_citations,
            citation_format=req.citation_format,
            discipline=req.citation_discipline
        )
        bib_text = c_res["bib_text"]

    latency = (time.time() - start) * 1000.0

    return HumanizeResponse(
        success=True,
        humanized_text=humanized,
        words_processed=words_count,
        modifications_count=telemetry["total_modifications"],
        latency_ms=round(latency, 2),
        citation_count=telemetry["citations_inserted"],
        bib_text=bib_text,
        telemetry=telemetry
    )

@app.post("/v1/citations", response_model=CitationResponse)
def citations_endpoint(req: CitationRequest, x_api_key: Optional[str] = Header(None)):
    start = time.time()
    engine = CitationEngine()
    result = engine.insert_citations(
        text=req.text,
        citation_count=req.citation_count,
        citation_format=req.citation_format,
        discipline=req.discipline
    )
    latency = (time.time() - start) * 1000.0

    return CitationResponse(
        success=True,
        cited_text=result["cited_text"],
        bib_text=result["bib_text"],
        citation_count=result["citation_count"],
        words_processed=len(req.text.split()),
        latency_ms=round(latency, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
