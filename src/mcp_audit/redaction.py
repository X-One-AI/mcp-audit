from __future__ import annotations

import re

_GITHUB_TOKEN = re.compile(r"gh[pousr]_[A-Za-z0-9_]{8,}")
_BEARER_TOKEN = re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE)
_KEY_VALUE_SECRET = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*([A-Za-z0-9._~+/=-]{12,})"
)


def redact_text(value: object) -> str:
    text = str(value)
    text = _GITHUB_TOKEN.sub(lambda match: f"{match.group(0)[:4]}********", text)
    text = _BEARER_TOKEN.sub("Bearer ********", text)
    text = _KEY_VALUE_SECRET.sub(lambda match: f"{match.group(1)}=********", text)
    return text


def looks_like_literal_secret(value: object) -> bool:
    if not isinstance(value, str):
        return False
    if value.startswith("${") and value.endswith("}"):
        return False
    if _GITHUB_TOKEN.search(value):
        return True
    if _BEARER_TOKEN.search(value):
        return True
    if _KEY_VALUE_SECRET.search(f"token={value}"):
        return any(marker in value.lower() for marker in ("key", "token", "secret", "ghp_"))
    return False
