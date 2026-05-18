from __future__ import annotations

import re
from typing import Dict, List
from urllib.parse import urlparse

import pandas as pd

FEATURE_COLUMNS = [
    "url_length",
    "has_http",
    "has_at",
    "has_ip",
    "subdomain_count",
    "path_length",
    "query_length",
    "has_https",
    "has_shortener",
    "digit_ratio",
    "hyphen_count",
    "suspicious_keyword_count",
]

SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "adf.ly",
}

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "bank",
    "secure",
    "update",
    "free",
    "confirm",
    "billing",
    "recover",
    "alert",
    "signin",
    "bonus",
]

IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def _normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not urlparse(url).scheme:
        return f"http://{url}"
    return url


def extract_features(url: str) -> Dict[str, float]:
    normalized = _normalize_url(url)
    parsed = urlparse(normalized)
    netloc = parsed.netloc.lower()
    full = normalized.lower()

    digits = sum(ch.isdigit() for ch in full)
    digit_ratio = digits / max(len(full), 1)
    subdomain_count = max(netloc.count(".") - 1, 0)

    keyword_count = 0
    for word in SUSPICIOUS_KEYWORDS:
        if word in full:
            keyword_count += 1

    return {
        "url_length": len(normalized),
        "has_http": int(normalized.startswith("http://")),
        "has_at": int("@" in normalized),
        "has_ip": int(bool(IPV4_PATTERN.search(netloc) or IPV4_PATTERN.search(full))),
        "subdomain_count": subdomain_count,
        "path_length": len(parsed.path or ""),
        "query_length": len(parsed.query or ""),
        "has_https": int(normalized.startswith("https://")),
        "has_shortener": int(netloc in SHORTENERS),
        "digit_ratio": digit_ratio,
        "hyphen_count": normalized.count("-"),
        "suspicious_keyword_count": keyword_count,
    }


def build_feature_frame(urls: List[str]) -> pd.DataFrame:
    rows = [extract_features(url) for url in urls]
    return pd.DataFrame(rows, columns=FEATURE_COLUMNS)
