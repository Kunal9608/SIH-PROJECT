import requests

# 🔥 Paste your Google API key here
API_KEY = "AIzaSyCHmPRhrNziKLLZhCdp-KunbDamWQAnhyQ"

GSB_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"


def google_safe_check(url: str) -> dict:
    if not API_KEY or API_KEY.strip() == "":
        return {"safe": None, "reason": "GOOGLE_API_KEY_NOT_SET"}

    payload = {
        "client": {
            "clientId": "sih-project",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    try:
        response = requests.post(
            f"{GSB_URL}?key={API_KEY}",
            json=payload,
            timeout=6
        )
    except Exception as e:
        return {"safe": None, "reason": f"REQUEST_ERROR:{str(e)}"}

    if response.status_code != 200:
        return {"safe": None, "reason": f"HTTP_{response.status_code}"}

    try:
        data = response.json()
    except:
        return {"safe": None, "reason": "JSON_ERROR"}

    # If Google detects threat
    if "matches" in data and data["matches"]:
        threat = data["matches"][0].get("threatType", "PHISHING")
        return {"safe": False, "reason": threat}

    # Clean
    return {"safe": True, "reason": "CLEAN"}