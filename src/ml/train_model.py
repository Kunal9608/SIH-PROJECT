import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path
from features import extract_features
from tqdm import tqdm

DATA_FILE = Path("data/raw/merged.csv")
MODEL_PATH = Path("models/url_model.pkl")

print("\n==============================")
print("   LOADING DATASET")
print("==============================\n")

df = pd.read_csv(DATA_FILE)

# clean label text
df["label"] = df["label"].astype(str).str.lower().str.strip()

# MALICIOUS LABEL KEYWORDS
malicious_keywords = [
    "phish", "adult", "malware", "malicious", "fraud", 
    "harmful", "suspicious", "unsafe", "blacklist", "spam"
]

# SAFE LABEL KEYWORDS
benign_keywords = [
    "benign", "safe", "legit", "clean", "good"
]

# map labels
def map_label(x):
    for m in malicious_keywords:
        if m in x:
            return 1
    for b in benign_keywords:
        if b in x:
            return 0
    return 0   # default safe for unknown labels

df["label"] = df["label"].apply(map_label)

print(f"Total URLs Loaded: {len(df)}")
print("Malicious :", df[df['label'] == 1].shape[0])
print("Benign    :", df[df['label'] == 0].shape[0])


print("\n==============================")
print("   EXTRACTING URL FEATURES")
print("==============================\n")

feature_rows = []
for url in tqdm(df["url"], desc="Extracting", ncols=80):
    feature_rows.append(extract_features(url))

X = pd.DataFrame(feature_rows)
y = df["label"].astype(int)


print("\n==============================")
print("     SPLITTING DATASET")
print("==============================\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size :", len(X_test))


print("\n==============================")
print("       TRAINING MODEL")
print("==============================\n")

n_estimators = 200
model = RandomForestClassifier(
    n_estimators=n_estimators,
    max_depth=25,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

print("\n==============================")
print("        EVALUATING MODEL")
print("==============================\n")

acc = model.score(X_test, y_test)
print(f"Accuracy: {acc:.4f}")


print("\n==============================")
print("        SAVING MODEL")
print("==============================\n")

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)
print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")