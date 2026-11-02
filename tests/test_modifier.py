import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from unbotify.config import UnbotifyConfig
from unbotify.core.modifier import TextModifier
from unbotify.core.ai_detector import ZipPyDetector

class TestModifierPipeline(unittest.TestCase):
    def setUp(self):
        self.config = UnbotifyConfig(INTENSITY=80.0, SEED=42)
        self.modifier = TextModifier(self.config)

    def test_phrase_rewrites(self):
        text = "In conclusion, it is important to delve into the comprehensive tapestry of neural networks."
        transformed = self.modifier.modify_text(text)
        self.assertNotIn("delve into", transformed)
        self.assertNotIn("comprehensive tapestry", transformed)
        self.assertGreater(self.modifier.phrase_rewrite_count, 0)

    def test_synonym_substitution(self):
        text = "We analyze the method and compute the results to optimize accuracy."
        transformed = self.modifier.modify_text(text)
        self.assertNotEqual(text, transformed)
        self.assertGreater(self.modifier.synonym_swap_count, 0)

    def test_protected_terms(self):
        self.config.PROTECTED_TERMS = ["Navier-Stokes", "TensorFlow", "CRISPR-Cas9"]
        modifier = TextModifier(self.config)
        text = "We analyze Navier-Stokes equations using TensorFlow and CRISPR-Cas9 models."
        transformed = modifier.modify_text(text)
        self.assertIn("Navier-Stokes", transformed)
        self.assertIn("TensorFlow", transformed)
        self.assertIn("CRISPR-Cas9", transformed)

    def test_zero_expansion_mode(self):
        cfg = UnbotifyConfig(INTENSITY=75.0, ZERO_EXPANSION=True, SEED=42)
        modifier = TextModifier(cfg)
        text = "The algorithm demonstrates substantial efficacy in mitigating network latency across distributed clusters."
        transformed = modifier.modify_text(text)
        # Verify 1:1 token count parity
        self.assertEqual(len(text.split()), len(transformed.split()))

    def test_voice_transformation(self):
        cfg = UnbotifyConfig(INTENSITY=100.0, SEED=42)
        cfg.VOICE_TRANSFORM_RATE = 1.0
        modifier = TextModifier(cfg)
        text = "We analyzed the experimental results carefully and thoroughly for this evaluation."
        transformed = modifier._transform_voice(text)
        self.assertTrue("were analyzed" in transformed or "The experimental results" in transformed)

    def test_ai_neutralization_to_zero(self):
        raw_ai_sample = (
            "In conclusion, it is important to delve into the comprehensive tapestry of modern neural networks. "
            "This study plays a pivotal role in illustrating that artificial intelligence stands as a testament to human innovation. "
            "Furthermore, the interplay between stochastic optimization and computational scalability provides a robust framework "
            "for subsequent empirical inquiries. In order to delve into the multifaceted dimensions of this phenomenon, "
            "previous studies have shown that distributed clusters achieve significant acceleration."
        )
        before_detection = ZipPyDetector.analyze(raw_ai_sample)
        self.assertGreater(before_detection["risk_score"], 50.0)

        transformed = self.modifier.modify_text(raw_ai_sample)
        after_detection = ZipPyDetector.analyze(transformed)
        self.assertEqual(after_detection["risk_score"], 0.0)
        self.assertIn("Safe (100% Human-Authored", after_detection["classification"])

    def test_contractions_expansion_in_academic(self):
        text = "It's clear that the algorithm didn't encounter memory fragmentation and won't fail."
        transformed = self.modifier.modify_text(text)
        self.assertIn("it is", transformed.lower())
        self.assertIn("did not", transformed)
        self.assertIn("will not", transformed)

    def test_empirical_voice_matching_calibration(self):
        voice_sample = (
            "The experiment failed. The data showed anomalies. We repeated the run. "
            "The outcome remained identical. We halted the procedure."
        )
        self.modifier.calibrate_voice_from_sample(voice_sample)
        self.assertTrue(self.modifier.config.ENABLE_SPLIT_COMPOUND)
        self.assertEqual(self.modifier.config.STYLE, "academic")

    def test_clean_punctuation_and_no_double_words(self):
        dirty = "This is, , a test sentence  . It is evident that that method works  , perfectly."
        cleaned = self.modifier._clean_punctuation(dirty)
        self.assertNotIn(", ,", cleaned)
        self.assertNotIn("that that", cleaned)
        self.assertNotIn("  .", cleaned)
        self.assertNotIn("  ,", cleaned)

if __name__ == "__main__":
    unittest.main()
