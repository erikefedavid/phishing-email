import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.preprocessor import preprocess

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
MODEL_DIR = os.path.dirname(__file__)


def load_data():
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in data/raw/.")
        sys.exit(1)
    dfs = []
    for f in csv_files:
        df = pd.read_csv(os.path.join(DATA_DIR, f), on_bad_lines="skip")
        if "text_combined" in df.columns and "label" in df.columns:
            df = df.rename(columns={"text_combined": "text"})
            dfs.append(df)
            print(f"  {f}: using text_combined column")
        elif "body" in df.columns and "label" in df.columns:
            if "subject" in df.columns:
                df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")
            else:
                df["text"] = df["body"]
            dfs.append(df)
            print(f"  {f}: using body (+ subject) column")
        elif "text" in df.columns and "label" in df.columns:
            dfs.append(df)
            print(f"  {f}: using text column")
        else:
            print(f"  {f}: skipping (no text+label columns)")
    if not dfs:
        print("No dataset with usable columns found.")
        sys.exit(1)
    df = pd.concat(dfs, ignore_index=True)
    print(f"  Total rows loaded: {len(df)}")
    return df


def balanced_sample(df, n=8000):
    pos = df[df["label"] == 1]
    neg = df[df["label"] == 0]
    n_per = min(n // 2, len(pos), len(neg))
    pos = pos.sample(n_per, random_state=42)
    neg = neg.sample(n_per, random_state=42)
    return pd.concat([pos, neg], ignore_index=True)


def main():
    df = load_data()
    if df["label"].dtype == "object":
        df["label"] = df["label"].map({"phishing": 1, "legitimate": 0, "ham": 0, "spam": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    df = balanced_sample(df, n=6000)
    print(f"  Balanced to {len(df)} rows ({len(df[df['label']==1])} phishing, {len(df[df['label']==0])} legitimate)")

    df["cleaned"] = df["text"].apply(preprocess)

    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])
    pipeline.fit(X_train, y_train)

    accuracy = pipeline.score(X_test, y_test)
    print(f"Test accuracy: {accuracy:.4f}")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    pd.DataFrame({"cleaned": X_test, "label": y_test}).to_csv(
        os.path.join(PROCESSED_DIR, "test.csv"), index=False
    )

    joblib.dump(pipeline, os.path.join(MODEL_DIR, "pipeline.pkl"))
    print(f"Model saved to {os.path.join(MODEL_DIR, 'pipeline.pkl')}")


if __name__ == "__main__":
    main()
