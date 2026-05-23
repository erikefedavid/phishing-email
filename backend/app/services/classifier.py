import os
import joblib
import numpy as np
from app.config import settings
from app.utils.logger import logger


class ClassifierService:
    def __init__(self):
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        path = settings.MODEL_PATH
        if os.path.exists(path):
            self.pipeline = joblib.load(path)
            logger.info(f"Model loaded from {path}")
        else:
            logger.warning(f"Model not found at {path}. Using fallback classifier.")

    def predict(self, text: str) -> tuple[str, float]:
        if self.pipeline:
            proba = self.pipeline.predict_proba([text])[0]
            confidence = float(max(proba))
            label = "phishing" if self.pipeline.classes_[proba.argmax()] == 1 else "legitimate"
            return label, confidence

        return "legitimate", 0.0

    def predict_proba(self, text: str) -> list[float]:
        if self.pipeline:
            return self.pipeline.predict_proba([text])[0].tolist()
        return [0.5, 0.5]

    def get_top_features(self, features: dict) -> list[dict]:
        weights = [
            ("url_count", features.get("url_count", 0) * 0.3),
            ("sender_anomaly", features.get("sender_anomaly_score", 0) * 0.25),
            ("urgency_keywords", features.get("urgency_score", 0) * 0.3),
            ("html_ratio", features.get("html_ratio", 0) * 0.15),
        ]
        weights.sort(key=lambda x: x[1], reverse=True)
        return [{"feature": f, "weight": round(w, 4)} for f, w in weights[:5]]
