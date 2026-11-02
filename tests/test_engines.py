import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from unbotify.core.ai_detector import ZipPyDetector
from unbotify.core.similarity_checker import SimilarityChecker
from unbotify.core.citation_engine import CitationEngine

class TestEngines(unittest.TestCase):
    def test_zippy_ai_detector(self):
        repetitive_ai_text = "In conclusion, it is important to delve into the comprehensive tapestry of neural networks. " * 5
        res = ZipPyDetector.analyze(repetitive_ai_text)
        self.assertIn("risk_score", res)
        self.assertIn("trilateral_split", res)
        self.assertGreater(res["risk_score"], 40.0)

        human_style_text = "We measured 4.2 ms latency on node 3, but the GPU crashed on batch 12 due to memory fragmentation."
        res_human = ZipPyDetector.analyze(human_style_text)
        self.assertLess(res_human["risk_score"], 60.0)

    def test_winnowing_and_similarity(self):
        doc_a = "The algorithm demonstrates substantial efficacy in mitigating network latency across distributed clusters."
        doc_b = "The algorithm demonstrates substantial efficacy in mitigating network latency across distributed clusters."
        res_identical = SimilarityChecker.compare_documents(doc_a, doc_b)
        self.assertEqual(res_identical["composite_score"], 100.0)
        self.assertEqual(res_identical["metrics"]["winnowing_fingerprint_pct"], 100.0)

        doc_c = "A completely different sentence discussing biological cellular signaling in plants."
        res_diff = SimilarityChecker.compare_documents(doc_a, doc_c)
        self.assertLess(res_diff["composite_score"], 20.0)

    def test_citation_engine(self):
        engine = CitationEngine()
        text = "Deep learning architectures significantly reduce computational latency in distributed systems."
        result = engine.insert_citations(text, citation_count=1, citation_format="IEEE [1]", discipline="computer_science")
        self.assertEqual(result["citation_count"], 1)
        self.assertIn("[1]", result["cited_text"])
        self.assertIn("@article{", result["bib_text"])
        self.assertIn("AI AUTO-FILL INSTRUCTIONS", result["bib_text"])

if __name__ == "__main__":
    unittest.main()

