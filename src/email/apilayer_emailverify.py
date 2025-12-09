import requests

API_KEY = "10FcY7t9nI2nmdT4esKlHHXiRaV2nQEc"

def verify_email_api(email: str):
    """Checks whether email inside the text is real or disposable."""
    try:
        # Extract email from message
        import re
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email)
        if not match:
            return {"label": "safe", "safe": True, "reason": "No valid email found"}

        extracted_email = match.group(0)
        print("📧 EXTRACTED EMAIL:", extracted_email)

        url = f"https://api.apilayer.com/email_verification/{extracted_email}"
        headers = {"apikey": API_KEY}

        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        print("📩 EMAIL VERIFY RESULT:", data)

        if data.get("disposable") is True:
            return {"label": "phishing", "safe": False}

        if data.get("format_valid") and data.get("smtp_check"):
            return {"label": "safe", "safe": True}

        return {"label": "phishing", "safe": False}

    except Exception as e:
        print("❌ EMAIL VERIFY ERROR:", e)
        return {"label": "unknown", "safe": False}