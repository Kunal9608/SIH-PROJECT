import sys, os, time, urllib.parse, importlib

# ---------------------------------------------------------
# FIX PYTHON PATHS (VERY IMPORTANT)
# ---------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

ML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/ml"))
sys.path.insert(0, ML_PATH)

# ---------------------------------------------------------
# IMPORT SECURITY APIS
# ---------------------------------------------------------
from google_safebrowsing import google_safe_check
from virustotal import vt_check
from ipqs import ipqs_check


# ---------------------------------------------------------
# LOAD ML MODEL
# ---------------------------------------------------------
def load_ml():
    try:
        mod = importlib.import_module("predict")
        return mod.predict
    except:
        mod = importlib.import_module("src.ml.predict")
        return mod.predict


ml_predict = load_ml()


# ---------------------------------------------------------
# URL NORMALIZATION
# ---------------------------------------------------------
def normalize(url: str):
    url = url.strip()
    if not url.startswith("http"):
        return "https://" + url
    return url


# ---------------------------------------------------------
# GENERATE HTTP/HTTPS VARIANTS
# ---------------------------------------------------------
def versions(url: str):
    parsed = urllib.parse.urlparse(url)
    v = []

    if parsed.scheme:
        v.append(url)
        swap = ("http://" if parsed.scheme == "https" else "https://") + parsed.netloc + parsed.path
        v.append(swap)
    else:
        v.append("https://" + url)
        v.append("http://" + url)

    base = parsed.netloc + parsed.path if parsed.scheme else url
    v.append(base)

    # Remove duplicates
    return list(dict.fromkeys(v))


# ---------------------------------------------------------
# MAIN CHECK
# ---------------------------------------------------------
def check_all(url: str):
    url_norm = normalize(url)
    vers = versions(url_norm)

    print("\n======================================================")
    print(f"🔍 CHECKING URL : {url}")
    print("Variants:", vers)
    print("======================================================")

    # STRUCTURED RESULTS
    results = {
        "google": {"safe": None},
        "vt": {"safe": None},
        "ipqs": {"safe": None},
        "ml": {"safe": None},
    }

    # GOOGLE SAFE BROWSING
    print("\n--- GOOGLE SAFE BROWSING ---")
    for v in vers:
        try:
            r = google_safe_check(v)
            print(f"{v} → {r}")
        except Exception as e:
            r = {"safe": None, "reason": f"ERR:{e}"}

        if r["safe"] is not None:
            results["google"] = r
            break

    # VIRUSTOTAL
    print("\n--- VIRUSTOTAL ---")
    for v in vers:
        try:
            r = vt_check(v)
            print(f"{v} → {r}")
        except Exception as e:
            r = {"safe": None, "reason": f"ERR:{e}"}

        if r["safe"] is not None:
            results["vt"] = r
            break

    # IPQS
    print("\n--- IPQS API ---")
    for v in vers:
        try:
            r = ipqs_check(v)
            print(f"{v} → {r}")
        except Exception as e:
            r = {"safe": None, "reason": f"ERR:{e}"}

        if r["safe"] is not None:
            results["ipqs"] = r
            break

    # ML MODEL RESULT
    print("\n--- ML MODEL ---")
    try:
        ml = ml_predict(url_norm)
        print("ML Raw:", ml)

        label = ml["label"].lower()
        conf = ml.get("confidence", 0)

        if label in ("phish", "phishing", "malicious", "adult"):
            results["ml"] = {"safe": False, "reason": label, "confidence": conf}
        elif label in ("benign", "safe", "legit"):
            results["ml"] = {"safe": True, "reason": label, "confidence": conf}
        else:
            results["ml"] = {"safe": None, "reason": "unknown"}

    except Exception as e:
        print("ML Error:", e)
        results["ml"] = {"safe": None, "reason": f"ERR:{e}"}

    # SUMMARY
    print("\n==================== SUMMARY ====================")
    print(results)

    # FINAL VERDICT
    votes_safe = sum(1 for k in results if results[k]["safe"] is True)
    votes_bad = sum(1 for k in results if results[k]["safe"] is False)

    print("\n==================== FINAL RESULT ====================")

    if votes_safe >= 2:
        print("🟢 SAFE — MAJORITY CLEAN")
        return "SAFE"
    elif votes_bad >= 1:
        print("🔴 PHISHING — DETECTED BY MULTIPLE SOURCES")
        return "PHISHING"
    else:
        print("🟡 UNKNOWN — INSUFFICIENT INFORMATION")
        return "UNKNOWN"


# ---------------------------------------------------------
# TEST RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    TEST_URLS = [
        "https://google.com",
        "http://example.com",
        "http://testsafebrowsing.appspot.com/s/phishing.html",
        "paypal.com.fake-login-update.info",
    ]

    for u in TEST_URLS:
        check_all(u)
        print("\n\n")
        time.sleep(1)