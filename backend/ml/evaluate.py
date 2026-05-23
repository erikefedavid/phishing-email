import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)

MODEL_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(MODEL_DIR, "..", "data", "processed")


def main():
    pipeline = joblib.load(os.path.join(MODEL_DIR, "pipeline.pkl"))
    test = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    X_test, y_test = test["cleaned"], test["label"]

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    print("=== Evaluation Metrics ===")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))


if __name__ == "__main__":
    main()
