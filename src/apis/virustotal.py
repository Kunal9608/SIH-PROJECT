import time
import requests
VT_API_KEY = "11ef724727a069bbbd423cf7d133cdfd4259d398f09697f3461dbd8f8d2908"
VT_URL = "https://www.virustotal.com/api/v3/urls"
def vt_check(url: str) -> dict:
    if not VT_API_KEY:
        return {"safe": None, "reason": "VT_API_KEY_NOT_SET"}
    headers = {"x-apikey": VT_API_KEY}
    try:
        submit = requests.post(VT_URL, data={"url": url}, headers=headers, timeout=8)
    except Exception as e:
        return {"safe": None, "reason": f"REQUEST_ERROR:{e}"}
    if submit.status_code != 200:
        return {"safe": None, "reason": f"HTTP_{submit.status_code}"}
    try:
        analysis_id = submit.json()["data"]["id"]
    except:
        return {"safe": None, "reason": "INVALID_RESPONSE"}
    analysis_api = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    for _ in range(8):
        try:
            result = requests.get(analysis_api, headers=headers, timeout=8)
        except Exception as e:
            return {"safe": None, "reason": f"RESULT_ERROR:{e}"}
        if result.status_code != 200:
            return {"safe": None, "reason": f"HTTP_{result.status_code}"}
        try:
            data = result.json()
        except:
            return {"safe": None, "reason": "JSON_PARSE_ERROR"}
        status = data["data"]["attributes"]["status"]
        if status != "completed":
            time.sleep(1)
            continue
        stats = data["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        if malicious > 0 or suspicious > 0:
            return {
                "safe": False, 
                "reason": f"{malicious} malicious, {suspicious} suspicious"
            }
        return {"safe": True, "reason": "CLEAN"}
    return {"safe": None, "reason": "PENDING_ANALYSIS"}
