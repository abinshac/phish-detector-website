from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd

app = FastAPI(title="DQCS5 Phish Detector - Starter API")

# --------------------------
# Enable CORS for frontend
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Model Loading
# --------------------------
MODEL_PATH = Path(__file__).resolve().parents[2] / "backend" / "models" / "pipeline.joblib"
model = None

try:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded from {MODEL_PATH}")
    else:
        print(f"⚠️ Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# --------------------------
# Request Schema
# --------------------------
class Email(BaseModel):
    id: str = ""
    sender: str = ""
    subject: str = ""
    body: str = ""
    urls: list = []


# --------------------------
# Routes
# --------------------------

@app.get("/")
def root():
    """Root endpoint to avoid 404 on homepage."""
    return {
        "message": "Phish Detector API is running! 🚀",
        "docs_url": "/docs",
        "health_url": "/health"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": model is not None
    }


@app.post("/score")
def score_email(email: Email):
    """Score an email for phishing risk."""
    text = (email.subject or "") + " " + (email.body or "")

    if model is None:
        return {"score": None, "error": "Model not trained. Run python src/train.py"}

    # Predict probability
    try:
        prob = model.predict_proba([text.lower()])[0][1]
    except Exception as e:
        return {"score": None, "error": f"Prediction failed: {str(e)}"}

    label = int(prob > 0.5)

    # Explainable reasons
    reasons = []
    if "urgent" in text.lower() or "asap" in text.lower():
        reasons.append("contains urgency cues")
    if email.urls:
        reasons.append("contains URLs")

    return {
        "score": float(prob),
        "label": label,
        "reasons": reasons,
        "email_id": email.id
    }



