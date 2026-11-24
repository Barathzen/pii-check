import pytest

from pii_check import check


def test_redact_email_and_phone():
    r = check("Mail bob@example.com or call (415) 555-0134.", "redact")
    assert r["text"] == "Mail [EMAIL] or call [PHONE]."
    assert r["types"] == ["email", "phone"]
    assert r["decision"] == "redacted"
    assert r["redaction_count"] == 2


def test_redact_multiple_items():
    r = check("a@x.io, b@y.org, 415-555-0134", "redact")
    assert r["text"] == "[EMAIL], [EMAIL], [PHONE]"
    assert r["redaction_count"] == 3


def test_block_returns_no_text():
    r = check("Mail bob@example.com", "block")
    assert r["decision"] == "blocked"
    assert r["text"] is None
    assert r["types"] == ["email"]


def test_clean_text_is_allowed():
    r = check("nothing here", "redact")
    assert r == {"types": [], "decision": "allowed", "redaction_count": 0, "text": "nothing here"}


def test_unknown_policy_raises():
    with pytest.raises(ValueError):
        check("x", "shred")


def test_block_redacts_nothing_but_lists_types():
    r = check("Mail bob@example.com or call 415-555-0134", "block")
    assert r["decision"] == "blocked"
    assert r["text"] is None
    assert r["types"] == ["email", "phone"]
    assert r["redaction_count"] == 0
