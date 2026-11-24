import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(?<![\w+])(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}(?!\w)"
)


def check(text, policy):
    """Find emails and phone numbers in text and apply a policy.

    policy "redact": replace each match with [EMAIL] or [PHONE].
    policy "block":  return decision "blocked" and no text.

    Returns a dict: types (sorted list), decision, redaction_count, text.
    """
    if policy not in ("redact", "block"):
        raise ValueError(f"unknown policy: {policy!r}")

    emails = EMAIL_RE.findall(text)
    redacted = EMAIL_RE.sub("[EMAIL]", text)
    phones = PHONE_RE.findall(redacted)
    redacted = PHONE_RE.sub("[PHONE]", redacted)

    types = []
    if emails:
        types.append("email")
    if phones:
        types.append("phone")
    found = len(emails) + len(phones)

    if policy == "block" and found:
        return {"types": types, "decision": "blocked", "redaction_count": 0, "text": None}
    if found:
        return {"types": types, "decision": "redacted", "redaction_count": found, "text": redacted}
    return {"types": [], "decision": "allowed", "redaction_count": 0, "text": text}
