from urllib.error import URLError

from mcp_audit.sanitized_fixture import (
    _fetch_public_text_with_curl,
    build_sanitized_fixture,
    github_url_to_raw_url,
    sanitize_fixture_text,
)


def test_github_blob_url_converts_to_raw_url():
    raw_url = github_url_to_raw_url("https://github.com/X-One-AI/example/blob/main/.cursor/mcp.json")

    assert raw_url == "https://raw.githubusercontent.com/X-One-AI/example/main/.cursor/mcp.json"


def test_raw_github_url_is_accepted():
    url = "https://raw.githubusercontent.com/X-One-AI/example/main/mcp.json"

    assert github_url_to_raw_url(url) == url


def test_non_github_url_is_rejected():
    try:
        github_url_to_raw_url("https://example.com/mcp.json")
    except ValueError as error:
        assert "github.com" in str(error)
    else:
        raise AssertionError("expected non-GitHub URL to be rejected")


def test_sanitize_fixture_text_redacts_secrets_and_personal_paths():
    openai_key = "sk-" + "this-is-a-real-looking-secret"
    github_token = "ghp_" + "1234567890abcdef"
    access_key = "AKIA" + "1234567890ABCDEF"
    text = """
{
  "apiKey": "%s",
  "token": "%s",
  "authorization": "Bearer abcdefghijklmnopqrstuvwxyz",
  "aws": "%s",
  "root": "/Users/alice/project"
}
""" % (
        openai_key,
        github_token,
        access_key,
    )

    sanitized = sanitize_fixture_text(text)

    assert "sk-this" not in sanitized
    assert "ghp_" not in sanitized
    assert "abcdefghijklmnopqrstuvwxyz" not in sanitized
    assert "AKIA" not in sanitized
    assert "/Users/alice" not in sanitized
    assert "<redacted-api-key>" in sanitized
    assert "<redacted-github-token>" in sanitized
    assert "<redacted-access-key>" in sanitized
    assert "/Users/example/project" in sanitized


def test_build_sanitized_fixture_accepts_injected_text_without_network():
    fixture = build_sanitized_fixture(
        "https://github.com/X-One-AI/example/blob/main/config.json",
        fetched_text='{"password": "super-secret-value", "path": "/home/bob/.config"}',
    )

    assert fixture.raw_url == "https://raw.githubusercontent.com/X-One-AI/example/main/config.json"
    assert "super-secret-value" not in fixture.content
    assert "/home/example/.config" in fixture.content


def test_curl_fallback_reports_original_fetch_error_when_curl_fails(monkeypatch):
    def fail_curl(*args, **kwargs):
        raise FileNotFoundError("curl")

    monkeypatch.setattr("subprocess.run", fail_curl)

    try:
        _fetch_public_text_with_curl("https://raw.githubusercontent.com/X-One-AI/example/main/config.json", URLError("ssl failed"))
    except RuntimeError as error:
        assert "ssl failed" in str(error)
    else:
        raise AssertionError("expected curl fallback failure to raise RuntimeError")
