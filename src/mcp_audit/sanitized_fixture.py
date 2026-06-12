from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

GITHUB_BLOB_PREFIX = "https://github.com/"
GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/"

_ACCESS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
_BEARER_TOKEN = re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE)
_GITHUB_TOKEN = re.compile(r"gh[pousr]_[A-Za-z0-9_]{8,}")
_OPENAI_KEY = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
_PRIVATE_PATH = re.compile(r"(?P<prefix>/(?:Users|home)/)[A-Za-z0-9._-]+")
_SECRET_ASSIGNMENT = re.compile(
    r"(?P<prefix>[\"']?(?:api[_-]?key|access[_-]?key|private[_-]?key|token|secret|password)[\"']?\s*[:=]\s*)"
    r"(?P<quote>[\"']?)"
    r"(?P<value>[A-Za-z0-9._~+/=-]{8,})"
    r"(?P=quote)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SanitizedFixture:
    source_url: str
    raw_url: str
    content: str


def github_url_to_raw_url(url: str) -> str:
    if url.startswith(GITHUB_RAW_PREFIX):
        return url
    if not url.startswith(GITHUB_BLOB_PREFIX):
        raise ValueError("only public github.com blob URLs or raw.githubusercontent.com URLs are supported")

    path = url.removeprefix(GITHUB_BLOB_PREFIX)
    parts = path.split("/", 4)
    if len(parts) != 5 or parts[2] != "blob":
        raise ValueError("expected GitHub blob URL shape: https://github.com/<owner>/<repo>/blob/<ref>/<path>")

    owner, repo, _, ref, file_path = parts
    if not owner or not repo or not ref or not file_path:
        raise ValueError("GitHub URL must include owner, repo, ref, and file path")
    return f"{GITHUB_RAW_PREFIX}{owner}/{repo}/{ref}/{file_path}"


def sanitize_fixture_text(text: str) -> str:
    sanitized = _GITHUB_TOKEN.sub("<redacted-github-token>", text)
    sanitized = _OPENAI_KEY.sub("<redacted-api-key>", sanitized)
    sanitized = _ACCESS_KEY.sub("<redacted-access-key>", sanitized)
    sanitized = _BEARER_TOKEN.sub("Bearer <redacted-token>", sanitized)
    sanitized = _SECRET_ASSIGNMENT.sub(lambda match: f"{match.group('prefix')}{match.group('quote')}<redacted-secret>{match.group('quote')}", sanitized)
    sanitized = _PRIVATE_PATH.sub(lambda match: f"{match.group('prefix')}example", sanitized)
    return sanitized


def fetch_public_text(raw_url: str) -> str:
    request = Request(raw_url, headers={"User-Agent": "mcp-audit-sanitized-fixture"})
    try:
        with urlopen(request, timeout=20) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except HTTPError as error:
        raise RuntimeError(f"GitHub returned HTTP {error.code} for {raw_url}") from error
    except URLError as error:
        return _fetch_public_text_with_curl(raw_url, error)


def _fetch_public_text_with_curl(raw_url: str, original_error: URLError) -> str:
    try:
        result = subprocess.run(
            ["curl", "--fail", "--location", "--silent", "--show-error", raw_url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as curl_error:
        raise RuntimeError(f"Could not fetch {raw_url}: {original_error.reason}") from curl_error
    return result.stdout


def build_sanitized_fixture(source_url: str, fetched_text: str | None = None) -> SanitizedFixture:
    raw_url = github_url_to_raw_url(source_url)
    text = fetched_text if fetched_text is not None else fetch_public_text(raw_url)
    return SanitizedFixture(source_url=source_url, raw_url=raw_url, content=sanitize_fixture_text(text))


def write_sanitized_fixture(fixture: SanitizedFixture, output: str | Path, metadata_output: str | Path | None = None) -> Path:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(fixture.content, encoding="utf-8")
    if metadata_output is not None:
        metadata_path = Path(metadata_output)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.write_text(
            "\n".join(
                [
                    f"source_url: {fixture.source_url}",
                    f"raw_url: {fixture.raw_url}",
                    "sanitization: tokens, bearer values, secret assignments, and personal home paths are redacted",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch a public GitHub config URL and write a sanitized fixture.")
    parser.add_argument("url", help="Public github.com blob URL or raw.githubusercontent.com URL")
    parser.add_argument("--output", required=True, help="Path for the sanitized fixture")
    parser.add_argument("--metadata-output", help="Optional sidecar metadata file with source information")
    args = parser.parse_args(argv)

    fixture = build_sanitized_fixture(args.url)
    output_path = write_sanitized_fixture(fixture, args.output, args.metadata_output)
    print(f"wrote sanitized fixture: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
