import requests
import json

API_KEY = "10FcY7t9nI2nmdT4esKlHHXiRaV2nQEc"
URL = "https://api.apilayer.com/textmoderation"

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

def check_text_mod(text: str):
    """Content moderation API"""
    try:
        payload = json.dumps({"text": text})
        r = requests.post(URL, headers=headers, data=payload, timeout=10)

        try:
            data = r.json()
        except:
            return {"label": "unknown", "score": 0, "safe": False}

        print("🟦 TEXT MOD RESPONSE:", data)

        if "error" in data:
            return {"label": "unknown", "score": 0, "safe": False}

        # Score logic
        score = float(data.get("sexual_suggestiveness", 0))

        if score > 0.5:
            return {"label": "phishing", "score": score, "safe": False}
        else:
            return {"label": "safe", "score": score, "safe": True}

    except Exception as e:
        print("❌ TEXTMOD ERROR:", e)
        return {"label": "unknown", "score": 0, "safe": False}