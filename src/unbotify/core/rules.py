"""
Rule loader and validator for Unbotify Engine.
Loads decoupled JSON dictionaries and strips __prompt__ metadata headers.
"""

import os
import json
import re
from typing import Dict, List, Tuple, Any

class RuleManager:
    _instance = None

    def __init__(self, rules_dir: str = None):
        if rules_dir is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_dir = os.path.join(base, "rules")
        self.rules_dir = rules_dir

        self.synonyms: Dict[str, List[str]] = {}
        self.phrases: List[Tuple[re.Pattern, str]] = []
        self.hedge_words: List[str] = []
        self.determiners: Dict[str, List[str]] = {}
        self.conjunctions: List[str] = []
        self.protected_terms: List[str] = []
        self.discourse_markers: Dict[str, List[str]] = {}
        self.appositives: Dict[str, str] = {}
        self.nominalizations: Dict[str, str] = {}
        self.voice_verbs: Dict[str, Dict[str, str]] = {}
        self.taxonomies: Dict[str, Dict[str, Any]] = {}

        self.load_all()

    @classmethod
    def get_instance(cls) -> "RuleManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _strip_metadata(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k != "__prompt__"}
        elif isinstance(data, list):
            cleaned = []
            for item in data:
                if isinstance(item, dict) and "__prompt__" in item:
                    continue
                cleaned.append(item)
            return cleaned
        return data

    def _load_json(self, filename: str) -> Any:
        filepath = os.path.join(self.rules_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return self._strip_metadata(json.load(f))

    def load_all(self):
        # 1. synonyms
        syn = self._load_json("synonyms.json") or {}
        self.synonyms = {k.lower(): v for k, v in syn.items()}

        # 2. phrases
        raw_phrases = self._load_json("phrases.json") or []
        self.phrases = []
        for item in raw_phrases:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                pattern_str, replacement = item
                try:
                    compiled = re.compile(pattern_str, re.IGNORECASE)
                    self.phrases.append((compiled, replacement))
                except re.error:
                    pass

        # 3. hedge words
        self.hedge_words = self._load_json("hedge_words.json") or []

        # 4. determiners
        self.determiners = self._load_json("determiners.json") or {}

        # 5. conjunctions
        self.conjunctions = [c.lower() for c in (self._load_json("conjunctions.json") or [])]

        # 6. protected terms
        self.protected_terms = self._load_json("protected_terms.json") or []

        # 7. discourse markers
        self.discourse_markers = self._load_json("discourse_markers.json") or {}

        # 8. appositives
        self.appositives = self._load_json("appositives.json") or {}

        # 9. nominalizations
        self.nominalizations = self._load_json("nominalizations.json") or {}

        # 10. voice verbs
        self.voice_verbs = self._load_json("voice_verbs.json") or {}

        # 11. taxonomy
        tax_dir = os.path.join(self.rules_dir, "taxonomy")
        self.taxonomies = {}
        if os.path.exists(tax_dir):
            for fname in os.listdir(tax_dir):
                if fname.endswith(".json"):
                    key = fname[:-5]
                    tax_path = os.path.join(tax_dir, fname)
                    with open(tax_path, "r", encoding="utf-8") as f:
                        self.taxonomies[key] = self._strip_metadata(json.load(f))

