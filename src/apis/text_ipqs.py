import requests

IPQS_API_KEY = "10FcY7t9nI2nmdT4esKlHHXiRaV2nQEc"   # paste your API key here

def check_ipqs_text(text: str):
    try:
        url = f"https://ipqualityscore.com/api/json/email/{IPQS_API_KEY}"

        payload = {
            "email": "test@example.com",     # required param even for text-only scans
            "strictness": 1,
            "fast": True,
            "additional_info": text          # WE PASS TEXT HERE!
        }

        res = requests.post(url, json=payload, timeout=10).json()

        # Extract threat signals
        fraud = res.get("fraudulent", False)
        spam = res.get("spam", False)
        suspicious = res.get("suspicious", False)
        score = res.get("overall_score", 0)

        # Convert into a unified structure
        if fraud or spam or suspicious or score >= 50:
            return {
                "safe": False,
                "label": "phishing",
                "score": score / 100
            }

        return {
            "safe": True,
            "label": "safe",
            "score": score / 100
        }

    except Exception as e:
        return {"safe": True, "label": "unknown", "score": 0, "error": str(e)}