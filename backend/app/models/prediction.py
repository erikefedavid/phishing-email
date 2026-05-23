from pydantic import BaseModel


class FeatureWeight(BaseModel):
    feature: str
    weight: float


class PredictionResult(BaseModel):
    label: str
    confidence: float
    is_phishing: bool
    top_features: list[FeatureWeight]
    processing_ms: float
