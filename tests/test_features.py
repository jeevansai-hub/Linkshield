"""Unit tests for static URL feature extractor."""

import unittest
from src.features.extract_features import URLLexicalFeatureExtractor


class TestURLLexicalFeatureExtractor(unittest.TestCase):

    def test_feature_extractor_returns_valid_dict(self):
        extractor = URLLexicalFeatureExtractor()
        sample_url = "http://login.paypal.account-verify.com/update?id=123"
        features = extractor.extract(sample_url)

        self.assertIsInstance(features, dict)
        self.assertEqual(features["url_length"], len(sample_url))
        self.assertEqual(features["has_ip"], 0)
        self.assertEqual(features["has_https"], 0)
        self.assertGreaterEqual(features["suspicious_keyword_count"], 3)
        self.assertIn("num_dots", features)
        self.assertIn("digit_ratio", features)

    def test_ip_address_detection(self):
        extractor = URLLexicalFeatureExtractor()
        ip_url = "http://192.168.1.1/admin/login.php"
        features = extractor.extract(ip_url)

        self.assertEqual(features["has_ip"], 1)
        self.assertEqual(features["has_https"], 0)

    def test_shortener_detection(self):
        extractor = URLLexicalFeatureExtractor()
        short_url = "https://bit.ly/3xYz901"
        features = extractor.extract(short_url)

        self.assertEqual(features["has_shortener_domain"], 1)
        self.assertEqual(features["has_https"], 1)

    def test_invalid_input_raises_error(self):
        extractor = URLLexicalFeatureExtractor()
        with self.assertRaises(ValueError):
            extractor.extract("")



if __name__ == "__main__":
    unittest.main()

