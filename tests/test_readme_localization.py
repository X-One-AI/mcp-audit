from pathlib import Path


def test_readme_has_english_and_chinese_versions():
    english = Path("README.md").read_text(encoding="utf-8")
    chinese = Path("README.zh-CN.md").read_text(encoding="utf-8")

    assert "[中文](./README.zh-CN.md)" in english
    assert "[English](./README.md)" in chinese
    assert "mcp-audit doctor" in english
    assert "mcp-audit doctor" in chinese
    assert "mcp-audit scan --config ./mcp.json" in english
    assert "mcp-audit scan --config ./mcp.json" in chinese
    assert "mcp-audit init --profile team" in english
    assert "mcp-audit init --profile team" in chinese
