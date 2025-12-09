import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_ROOT = r"bert_email_model"

class EmailPhishingDetector:
    def __init__(self):
        print("🔍 Loading BERT Email model...")

        base_path = os.path.join(os.getcwd(), MODEL_ROOT)

        # detect latest checkpoint
        checkpoints = []
        for name in os.listdir(base_path):
            if name.startswith("checkpoint-") and name.split("-")[-1].isdigit():
                checkpoints.append(int(name.split("-")[-1]))

        if checkpoints:
            latest = max(checkpoints)
            model_path = os.path.join(base_path, f"checkpoint-{latest}")
            print(f"✨ Using latest checkpoint: checkpoint-{latest}")
        else:
            model_path = base_path
            print("⚠ No checkpoints found, using model.safetensors")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

        print("✅ BERT Email model loaded successfully!\n")

    def predict(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        score = float(probs[0][1])

        label = "phishing" if score >= 0.50 else "safe"
        return {"label": label, "score": round(score, 4)}
