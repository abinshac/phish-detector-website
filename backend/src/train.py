# Improved training script for phishing detector
import pandas as pd
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
data_path = ROOT / "data" / "sample_emails.csv"
model_dir = ROOT / "models"
model_dir.mkdir(parents=True, exist_ok=True)

# --- Load data ---
df = pd.read_csv(data_path)
df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna("")).str.lower()

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# --- Features: word + char TF-IDF ---
features = FeatureUnion([
    ("word", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), max_features=10000, sublinear_tf=True)),
    ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000, sublinear_tf=True)),
])

pipe = Pipeline([
    ("features", features),
    ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear")),
])

# --- Train ---
pipe.fit(X_train, y_train)

# --- Evaluate ---
print("\nTrain score:", pipe.score(X_train, y_train))
print("Test score:", pipe.score(X_test, y_test))
y_pred = pipe.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, digits=4))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# --- Save ---
out_path = model_dir / "pipeline.joblib"
joblib.dump(pipe, out_path)
print(f"\n✅ Saved model to {out_path}")
