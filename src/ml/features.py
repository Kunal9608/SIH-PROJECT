import tldextract
import math
import re
from urllib.parse import urlparse

def entropy(string):
    """Calculate the Shannon entropy of a string."""
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])

def extract_features(url: str):
    """Extract numeric features from a URL."""
    try:
        parsed = urlparse(url)
        ext = tldextract.extract(url)
        
        features = {
            "url_length": len(url),
            "num_dots": url.count("."),
            "num_slashes": url.count("/"),
            "num_hyphens": url.count("-"),
            "num_question": url.count("?"),
            "has_https": 1 if parsed.scheme == "https" else 0,
            "domain_length": len(parsed.netloc),
            "entropy": entropy(url),
            "is_ip": 1 if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0,
            "subdomain_length": len(ext.subdomain),
        }
        return features
    except:
        return {
            "url_length": 0,
            "num_dots": 0,
            "num_slashes": 0,
            "num_hyphens": 0,
            "num_question": 0,
            "has_https": 0,
            "domain_length": 0,
            "entropy": 0,
            "is_ip": 0,
            "subdomain_length": 0,
        }