def simple_clean(url: str) -> str:
    if not url:
        return ""
    return url.strip().lower()