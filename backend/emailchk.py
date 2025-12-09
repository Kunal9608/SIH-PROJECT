import sys, os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# FIX PATH (works even with "sih finale")
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

SRC = os.path.join(BASE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# IMPORT ONLY BERT MODEL
from src.ml.email_predict import EmailPhishingDetector

# FASTAPI APP
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

print("\n📌 Loading BERT Email Phishing Model...")
bert_model = EmailPhishingDetector()
print("✅ BERT Model Loaded Successfully!\n")


class TextInput(BaseModel):
    text: str


@app.post("/check_text")
async def check_text(data: TextInput):
    text = data.text.strip()

    print("\n==================== EMAIL/TEXT SCAN ====================")
    print("INPUT:", text)

    if len(text) < 5:
        print("❌ Too short, cannot classify")
        return {
            "final": "unknown",
            "reason": "Text too short",
            "text": text
        }

    # BERT MODEL PREDICTION
    bert_res = bert_model.predict(text)
    label = bert_res.get("label", "unknown")

    print("🤖 BERT RESULT:", bert_res)
    print("FINAL:", label.upper())
    print("==========================================================\n")

    return {
        "text": text,
        "final": label,
        "bert_result": bert_res
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)