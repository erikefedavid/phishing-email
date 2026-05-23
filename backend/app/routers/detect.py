import time
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.email_model import EmailRequest
from app.models.prediction import PredictionResult, FeatureWeight
from app.services.preprocessor import preprocess
from app.services.feature_extractor import extract_features
from app.services.classifier import ClassifierService
from app.utils.email_parser import parse_raw_email

router = APIRouter()
classifier = ClassifierService()


@router.post("/detect", response_model=PredictionResult)
async def detect_email(request: EmailRequest):
    start = time.perf_counter()

    try:
        cleaned_body = preprocess(request.body)
        cleaned_subject = preprocess(request.subject) if request.subject else ""

        combined_text = f"{cleaned_subject} {cleaned_body}"
        features = extract_features(cleaned_subject, cleaned_body, request.headers)

        label, confidence = classifier.predict(combined_text)
        top_features_raw = classifier.get_top_features(features)

        elapsed = round((time.perf_counter() - start) * 1000, 2)

        return PredictionResult(
            label=label,
            confidence=round(confidence, 4),
            is_phishing=label == "phishing",
            top_features=[
                FeatureWeight(feature=f["feature"], weight=f["weight"])
                for f in top_features_raw
            ],
            processing_ms=elapsed,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")


@router.post("/detect/file", response_model=PredictionResult)
async def detect_email_file(file: UploadFile = File(...)):
    start = time.perf_counter()

    try:
        raw = (await file.read()).decode("utf-8", errors="replace")
        parsed = parse_raw_email(raw)
        cleaned_body = preprocess(parsed["body"])
        cleaned_subject = preprocess(parsed["subject"])

        combined_text = f"{cleaned_subject} {cleaned_body}"
        features = extract_features(cleaned_subject, cleaned_body, parsed["headers"])

        label, confidence = classifier.predict(combined_text)
        top_features_raw = classifier.get_top_features(features)

        elapsed = round((time.perf_counter() - start) * 1000, 2)

        return PredictionResult(
            label=label,
            confidence=round(confidence, 4),
            is_phishing=label == "phishing",
            top_features=[
                FeatureWeight(feature=f["feature"], weight=f["weight"])
                for f in top_features_raw
            ],
            processing_ms=elapsed,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
