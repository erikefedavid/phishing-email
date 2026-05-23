import re
from bs4 import BeautifulSoup


def strip_html(text: str) -> str:
    return BeautifulSoup(text, "html.parser").get_text(separator=" ")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def lowercase(text: str) -> str:
    return text.lower()


def remove_stop_words(text: str, stop_words: set | None = None) -> str:
    if stop_words is None:
        import nltk
        try:
            stop_words = set(nltk.corpus.stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = text.split()
    return " ".join(t for t in tokens if t not in stop_words)


def preprocess(text: str, strip_html_tags: bool = True) -> str:
    if strip_html_tags:
        text = strip_html(text)
    text = lowercase(text)
    text = normalize_whitespace(text)
    text = remove_stop_words(text)
    return text
