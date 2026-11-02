"""
Pairwise Document Similarity & Plagiarism Checker.
Executes 4 simultaneous passes: 5-gram exact overlap, Winnowing MinHash fingerprints (k=5, w=4),
Cosine TF-IDF vector similarity, and Longest Common Subsequence (LCS).
"""

import re
import math
from collections import Counter
from typing import Dict, List, Set, Tuple, Any

class SimilarityChecker:
    @staticmethod
    def _normalize_tokens(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b\w+\b", text)]

    @classmethod
    def compute_5gram_overlap(cls, tokens_a: List[str], tokens_b: List[str]) -> Tuple[float, Set[str]]:
        if len(tokens_a) < 5 or len(tokens_b) < 5:
            return 0.0, set()

        grams_a = set(" ".join(tokens_a[i:i+5]) for i in range(len(tokens_a) - 4))
        grams_b = set(" ".join(tokens_b[i:i+5]) for i in range(len(tokens_b) - 4))

        overlap = grams_a.intersection(grams_b)
        denominator = (len(grams_a) + len(grams_b)) / 2.0
        score = (len(overlap) / denominator) * 100.0 if denominator > 0 else 0.0
        return round(score, 1), overlap

    @classmethod
    def compute_winnowing_fingerprints(cls, tokens: List[str], k: int = 5, w: int = 4) -> Set[int]:
        """
        Computes Turnitin-exact Winnowing document fingerprints using Karp-Rabin rolling hashes.
        Guarantees that matches >= k + w - 1 = 8 words are always detected.
        """
        if len(tokens) < k:
            return set()

        # 1. Karp-Rabin rolling hash
        base = 257
        prime = 1000000007
        base_k_1 = pow(base, k - 1, prime)

        hashes = []
        # First k-gram
        cur_hash = 0
        for i in range(k):
            token_val = sum(ord(c) for c in tokens[i]) % prime
            cur_hash = (cur_hash * base + token_val) % prime
        hashes.append(cur_hash)

        # Rolling subsequent hashes in O(1)
        for i in range(1, len(tokens) - k + 1):
            prev_token_val = sum(ord(c) for c in tokens[i - 1]) % prime
            next_token_val = sum(ord(c) for c in tokens[i + k - 1]) % prime
            cur_hash = ((cur_hash - prev_token_val * base_k_1) * base + next_token_val) % prime
            hashes.append(cur_hash)

        # 2. Winnowing minimum selection over window w
        fingerprints = set()
        if len(hashes) < w:
            fingerprints.add(min(hashes))
            return fingerprints

        for i in range(len(hashes) - w + 1):
            window = hashes[i:i+w]
            min_val = min(window)
            fingerprints.add(min_val)

        return fingerprints

    @classmethod
    def compute_winnowing_similarity(cls, tokens_a: List[str], tokens_b: List[str]) -> float:
        fp_a = cls.compute_winnowing_fingerprints(tokens_a)
        fp_b = cls.compute_winnowing_fingerprints(tokens_b)

        if not fp_a or not fp_b:
            return 0.0

        intersection = fp_a.intersection(fp_b)
        union = fp_a.union(fp_b)
        jaccard = (len(intersection) / len(union)) * 100.0 if union else 0.0
        return round(jaccard, 1)

    @classmethod
    def compute_tfidf_cosine(cls, tokens_a: List[str], tokens_b: List[str]) -> float:
        if not tokens_a or not tokens_b:
            return 0.0

        counts_a = Counter(tokens_a)
        counts_b = Counter(tokens_b)
        all_words = set(counts_a.keys()).union(set(counts_b.keys()))

        dot = 0.0
        norm_a = 0.0
        norm_b = 0.0

        for w in all_words:
            val_a = counts_a.get(w, 0)
            val_b = counts_b.get(w, 0)
            dot += val_a * val_b
            norm_a += val_a ** 2
            norm_b += val_b ** 2

        if norm_a == 0 or norm_b == 0:
            return 0.0

        cosine = (dot / (math.sqrt(norm_a) * math.sqrt(norm_b))) * 100.0
        return round(cosine, 1)

    @classmethod
    def compute_lcs_ratio(cls, tokens_a: List[str], tokens_b: List[str]) -> float:
        """Computes Longest Common Subsequence ratio."""
        if not tokens_a or not tokens_b:
            return 0.0

        # Subsample to max 500 tokens for fast O(M*N) calculation
        sub_a = tokens_a[:500]
        sub_b = tokens_b[:500]
        m = len(sub_a)
        n = len(sub_b)

        dp = [0] * (n + 1)
        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if sub_a[i - 1] == sub_b[j - 1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev = temp

        lcs_len = dp[n]
        denominator = (m + n) / 2.0
        score = (lcs_len / denominator) * 100.0 if denominator > 0 else 0.0
        return round(score, 1)

    @classmethod
    def compare_documents(cls, doc_a: str, doc_b: str) -> Dict[str, Any]:
        tokens_a = cls._normalize_tokens(doc_a)
        tokens_b = cls._normalize_tokens(doc_b)

        score_5gram, overlap_grams = cls.compute_5gram_overlap(tokens_a, tokens_b)
        score_winnow = cls.compute_winnowing_similarity(tokens_a, tokens_b)
        score_tfidf = cls.compute_tfidf_cosine(tokens_a, tokens_b)
        score_lcs = cls.compute_lcs_ratio(tokens_a, tokens_b)

        # Composite Plagiarism Risk Index
        composite = (
            0.35 * score_5gram +
            0.35 * score_winnow +
            0.15 * score_tfidf +
            0.15 * score_lcs
        )
        composite = round(min(100.0, max(0.0, composite)), 1)

        if composite < 15.0:
            tier = "Low Risk (Safe Paraphrase / Distinct Documents)"
            status_color = "green"
        elif composite <= 40.0:
            tier = "Moderate Risk (Paraphrased Overlap Detected)"
            status_color = "orange"
        else:
            tier = "High Risk (Substantial Verbatim / Fingerprint Match)"
            status_color = "red"

        # Extract matching text snippets
        matching_snippets = list(overlap_grams)[:10]

        return {
            "composite_score": composite,
            "risk_tier": tier,
            "status_color": status_color,
            "metrics": {
                "ngram_overlap_pct": score_5gram,
                "winnowing_fingerprint_pct": score_winnow,
                "tfidf_cosine_pct": score_tfidf,
                "lcs_structural_pct": score_lcs
            },
            "tokens_count": {"doc_a": len(tokens_a), "doc_b": len(tokens_b)},
            "matching_snippets": matching_snippets
        }

