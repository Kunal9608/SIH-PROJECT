# src/ml/predict.py
import joblib
import pandas as pd
from pathlib import Path

# <-- RELATIVE imports (works reliably when project run as package)
from .features import extract_features
from .url_normalizer import simple_clean

MODEL_PATH = Path("models/url_model.pkl")


class URLPredictor:
    def __init__(self):
        print("Loading ML model...")
        self.model = joblib.load(MODEL_PATH)
        print("Model loaded!\n")

    def generate_versions(self, url: str):
        # normalize and generate http/https/www variants as you had
        url = simple_clean(url)

        versions = set()
        versions.add(url)

        if url.startswith("http://"):
            base = url.replace("http://", "")
            versions.add(base)
            versions.add("https://" + base)
        elif url.startswith("https://"):
            base = url.replace("https://", "")
            versions.add(base)
            versions.add("http://" + base)
        else:
            base = url
            versions.add("http://" + base)
            versions.add("https://" + base)

        versions.add(base.replace("www.", ""))
        return versions

    def predict(self, url: str):
        # For each generated version, extract features and predict
        versions = self.generate_versions(url)
        for v in versions:
            features = extract_features(v)
            # turn features into dataframe / row in same order as your training
            try:
                df = pd.DataFrame([features])
                prob = self.model.predict_proba(df)[0].max()  # or whatever you used
                label = self.model.predict(df)[0]
                # convert label/prob to safe boolean depending on your model mapping
                safe = label == "benign" or label == 0  # adjust to your labels
                return {"safe": bool(safe), "confidence": float(prob), "label": str(label)}
            except Exception as e:
                # if this version fails, continue to next version
                continue

        # If nothing returned, unknown
        return {"safe": None, "confidence": 0.0, "label": "ML_NO_LABEL"}