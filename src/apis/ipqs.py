import requests
import urllib.parse

def ipqs_check(url: str) -> dict:
    try:
        API_KEY = "nNzdrMWAkAILCcPwIzURYiNRjoY4r6XG"
        encoded = urllib.parse.quote_plus(url)
        api_url = f"https://ipqualityscore.com/api/json/url/{API_KEY}/{encoded}"

        r = requests.get(api_url, timeout=10)

        if r.status_code != 200:
            return {"safe": None, "reason": f"HTTP_{r.status_code}"}

        data = r.json()
        if data.get("success") is False:
            return {"safe": None, "reason": data.get("message", "API_FAIL")}

        if data.get("phishing") or data.get("malware") or data.get("unsafe"):
            return {
                "safe": False,
                "reason": "IPQS_THREAT",
                "risk": data.get("risk_score", 0)
            }
        return {
            "safe": True,
            "reason": "IPQS_SAFE",
            "risk": data.get("risk_score", 0)
        }
    except Exception as e:
        return {"safe": None, "reason": f"ERROR_{str(e)}"}