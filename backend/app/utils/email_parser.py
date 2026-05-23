import email
from email import policy


def parse_raw_email(raw: str) -> dict:
    msg = email.message_from_string(raw, policy=policy.default)
    headers = []
    for key, value in msg.items():
        headers.append(f"{key}: {value}")
    subject = msg.get("Subject", "")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break
    else:
        body = msg.get_content()
    return {
        "subject": subject,
        "body": body or "",
        "headers": "\n".join(headers),
    }
