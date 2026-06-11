from mcp_audit.redaction import redact_text


def test_redact_text_masks_github_token_like_values():
    raw = "token=ghp_example_literal_token"

    redacted = redact_text(raw)

    assert "ghp_example_literal_token" not in redacted
    assert "ghp_" in redacted
    assert "********" in redacted


def test_redact_text_masks_bearer_tokens():
    raw = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456"

    redacted = redact_text(raw)

    assert "abcdefghijklmnopqrstuvwxyz123456" not in redacted
    assert "Bearer ********" in redacted
