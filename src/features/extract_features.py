"""Static URL Feature Extraction Engine for LinkShield.

IMPORTANT SAFETY MANDATE:
This module operates strictly via static string parsing and Regular Expressions.
It NEVER issues network requests, DNS lookups, or webpage downloads.
"""


import re
from urllib.parse import urlparse
from typing import Dict, Any


class URLLexicalFeatureExtractor:
    """Extracts deterministic lexical, host, and structural features from raw URLs."""

    SUSPICIOUS_KEYWORDS = [
        "login", "verify", "account", "update", "banking", "secure",
        "confirm", "signin", "password", "paypal", "admin", "service",
        "free", "bonus", "ebay", "amazon", "apple", "google", "microsoft"
    ]

    SHORTENER_DOMAINS = {
        "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd",
        "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "su.pr"
    }

    SPECIAL_CHARS = set("!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~")

    def __init__(self):
        self.ip_pattern = re.compile(
            r"^(?:http[s]?://)?(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:[:/].*)?$"
        )

    def extract(self, url: str) -> Dict[str, Any]:
        """Extracts static numerical features from a raw URL string.

        Args:
            url: Raw target URL string.

        Returns:
            Dictionary containing numeric lexical and structural feature values.
        """
        if not isinstance(url, str) or not url.strip():
            raise ValueError("Input URL must be a non-empty string.")

        parsed = urlparse(url)
        hostname = parsed.netloc or parsed.path.split('/')[0]
        clean_host = hostname.split(':')[0].lower()
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment

        url_len = len(url)
        domain_len = len(hostname)
        path_len = len(path)
        query_len = len(query)

        num_digits = sum(c.isdigit() for c in url)
        digit_ratio = float(num_digits) / url_len if url_len > 0 else 0.0
        num_special_chars = sum(1 for c in url if c in self.SPECIAL_CHARS)

        # Count subdomains
        host_parts = [p for p in clean_host.split('.') if p]
        num_subdomains = max(0, len(host_parts) - 2) if len(host_parts) > 2 else 0

        # Path depth
        path_components = [p for p in path.split('/') if p]
        path_depth = len(path_components)

        suspicious_count = sum(
            1 for kw in self.SUSPICIOUS_KEYWORDS if kw in url.lower()
        )

        has_ip = 1 if self.ip_pattern.match(url) else 0
        has_https = 1 if parsed.scheme.lower() == "https" else 0
        has_shortener = 1 if clean_host in self.SHORTENER_DOMAINS else 0
        has_at_symbol = 1 if "@" in url else 0
        has_query = 1 if len(query) > 0 else 0
        has_fragment = 1 if len(fragment) > 0 else 0

        features: Dict[str, Any] = {
            "url_length": url_len,
            "domain_length": domain_len,
            "path_length": path_len,
            "query_length": query_len,
            "num_dots": url.count("."),
            "num_hyphens": url.count("-"),
            "num_underscores": url.count("_"),
            "num_slashes": url.count("/"),
            "num_question_marks": url.count("?"),
            "num_equal_signs": url.count("="),
            "num_at_symbols": url.count("@"),
            "num_digits": num_digits,
            "digit_ratio": round(digit_ratio, 4),
            "num_special_chars": num_special_chars,
            "num_subdomains": num_subdomains,
            "path_depth": path_depth,
            "has_ip": has_ip,
            "has_https": has_https,
            "has_shortener_domain": has_shortener,
            "has_at_symbol": has_at_symbol,
            "has_query": has_query,
            "has_fragment": has_fragment,
            "suspicious_keyword_count": suspicious_count,
        }

        return features
