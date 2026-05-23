import re
import tldextract


def count_urls(text: str) -> int:
    pattern = r"https?://[^\s]+|www\.[^\s]+"
    return len(re.findall(pattern, text, re.IGNORECASE))


def extract_domains(text: str) -> list[str]:
    urls = re.findall(r"https?://([^\s/]+)", text, re.IGNORECASE)
    return [tldextract.extract(u).registered_domain for u in urls]


def check_sender_anomaly(headers: str | None) -> float:
    if not headers:
        return 0.0
    anomalies = 0
    checks = [
        r"from:\s*[^@]*@[^.]*\.[^a-z]",  # suspicious TLD
        r"reply-to:\s*[^@]*@",  # mismatched reply-to
    ]
    for pattern in checks:
        if re.search(pattern, headers, re.IGNORECASE):
            anomalies += 1
    return min(anomalies / len(checks), 1.0)


def urgency_keyword_density(text: str) -> float:
    keywords = {
        "urgent", "immediately", "suspended", "deactivated", "verify",
        "click here", "act now", "limited time", "account", "password",
        "update your", "confirm", "expires", "expired", "security",
        "unauthorized", "login", "restore", "blocked",
    }
    words = text.lower().split()
    if not words:
        return 0.0
    count = sum(1 for w in words if w.strip(".,!?") in keywords)
    return count / len(words)


def html_to_text_ratio(text: str) -> float:
    html_tags = re.findall(r"<[^>]+>", text)
    if not html_tags:
        return 0.0
    return len("".join(html_tags)) / max(len(text), 1)


def extract_features(subject: str, body: str, headers: str | None = None) -> dict:
    combined = f"{subject} {body}"
    return {
        "url_count": count_urls(combined),
        "sender_anomaly_score": check_sender_anomaly(headers),
        "urgency_score": urgency_keyword_density(combined),
        "html_ratio": html_to_text_ratio(body),
        "text_length": len(combined),
    }
