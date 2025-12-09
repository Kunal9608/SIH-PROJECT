import requests
import json

API_KEY = "10FcY7t9nI2nmdT4esKlHHXiRaV2nQEc"
URL = "https://api.apilayer.com/risk_detection"

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

def check_risk_api(text: str):
    """Risk detection (scam, fraud, threat analysis)"""
    try:
        payload = json.dumps({"text": text})
        r = requests.post(URL, headers=headers, data=payload, timeout=10)
        
        try:
            data = r.json()
        except:
            return {"label": "unknown", "safe": False}

        print("⚠️ RISK API RESULT:", data)

        if "fraud_probability" not in data:
            return {"label": "unknown", "safe": False}

        risk_score = float(data["fraud_probability"])

        if risk_score > 0.5:
            return {"label": "phishing", "safe": False, "score": risk_score}
        else:
            return {"label": "safe", "safe": True, "score": risk_score}

    except Exception as e:
        print("❌ RISK API ERROR:", e)
        return {"label": "unknown", "safe": False}