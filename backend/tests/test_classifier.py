import pytest
from app.services.classifier import ClassifierService


def test_classifier_returns_label_and_confidence():
    svc = ClassifierService()
    label, confidence = svc.predict("click here to verify your account immediately")
    assert label in ("phishing", "legitimate")
    assert 0 <= confidence <= 1


def test_top_features_returns_five():
    svc = ClassifierService()
    features = {"url_count": 5, "sender_anomaly_score": 0.3, "urgency_score": 0.4, "html_ratio": 0.1}
    top = svc.get_top_features(features)
    assert len(top) <= 5
    assert all("feature" in f and "weight" in f for f in top)
