from textblob import TextBlob


def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return {
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
        "is_urgent": polarity < -0.3 and subjectivity > 0.5,
    }
