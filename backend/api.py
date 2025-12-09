from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys, os
import uvicorn

# FIXED IMPORT ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.apis.google_safebrowsing import google_safe_check

try:
    from src.apis.virustotal import vt_check
except ModuleNotFoundError:
    from src.apis.virustotal_api import vt_check

try:
    from src.apis.ipqs_api import ipqs_check
except ModuleNotFoundError:
    from src.apis.ipqs import ipqs_check

from src.ml.predict import URLPredictor


# ML model
ml_model = URLPredictor()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLItem(BaseModel):
    url: str


# FINAL VERDICT LOGIC (ONLY SAFE OR PHISHING)
def final_verdict(results):
    safe = 0
    if results["google"].get("safe") is True:
        safe += 1
    if results["vt"].get("safe") is True:
        safe += 1
    if results["ipqs"].get("safe") is True:
        safe += 1
    if results["ml"].get("safe") is True:
        safe += 1

    if safe >= 2:
        return {"safe": True, "final": "SAFE"}

    return {"safe": False, "final": "PHISHING"}


# MAIN CHECK ROUTE
@app.post("/check")
def check(data: URLItem):
    url = data.url.strip()

    # Ignore extension internal URLs
    if url.startswith("chrome-extension://") or "block.html" in url:
        return {
            "results": {
                "google": {"safe": True},
                "vt": {"safe": True},
                "ipqs": {"safe": True},
                "ml": {"safe": True},
            },
            "final": {"safe": True, "final": "SAFE"}
        }

    google_res = google_safe_check(url)
    vt_res = vt_check(url)
    ipqs_res = ipqs_check(url)
    ml_res = ml_model.predict(url)

    results = {
        "google": google_res,
        "vt": vt_res,
        "ipqs": ipqs_res,
        "ml": ml_res
    }

    final = final_verdict(results)
    return {"results": results, "final": final}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)