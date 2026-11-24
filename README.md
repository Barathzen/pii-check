# pii-check

`check(text, policy)` finds email addresses and phone numbers in text and applies a policy.

```python
from pii_check import check

check("Mail bob@example.com or call (415) 555-0134.", "redact")
# {"types": ["email", "phone"], "decision": "redacted", "redaction_count": 2,
#  "text": "Mail [EMAIL] or call [PHONE]."}

check("Mail bob@example.com", "block")
# {"types": ["email"], "decision": "blocked", "redaction_count": 0, "text": None}
```

## Return value

| Field | Meaning |
|---|---|
| `types` | Sorted list of types found: `"email"`, `"phone"` |
| `decision` | `"redacted"`, `"blocked"`, or `"allowed"` (nothing found) |
| `redaction_count` | Number of items actually replaced in the returned text |
| `text` | Redacted text, the original text if nothing was found, or `None` when blocked |

## Policies

- `redact`: replaces each match with `[EMAIL]` or `[PHONE]`.
- `block`: returns `decision="blocked"` and no text. Nothing is redacted, so `redaction_count` is `0`. `types` still lists what was found.
- Any other policy raises `ValueError`.

## Tests

```bash
python -m pytest
```

## Change in this pull request

On `main`, a blocked call reported `redaction_count` equal to the number of items found, although it returned no redacted text. This branch:

1. Adds `test_block_redacts_nothing_but_lists_types`, which fails on `main` with `assert 2 == 0`.
2. Changes one line in `pii_check/check.py` so blocked calls return `redaction_count: 0`.
