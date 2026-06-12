from pathlib import Path


def test_release_docs_cover_maturity_gates():
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    checklist = Path("docs/release-checklist.md").read_text(encoding="utf-8")
    release_notes = Path("docs/releases/v0.2.0.md").read_text(encoding="utf-8")
    stable_notes = Path("docs/releases/v0.3.0.md").read_text(encoding="utf-8")
    package_notes = Path("docs/releases/v0.3.1.md").read_text(encoding="utf-8")

    assert "0.3.1" in changelog
    assert "0.3.0" in changelog
    assert "0.2.0" in changelog
    assert "0.1.0" in changelog
    assert "mcp-audit policy check" in changelog
    assert "Baseline creation and suppression" in changelog
    assert "GitHub URL to sanitized fixture workflow" in changelog
    assert "GitHub CI is green" in checklist
    assert "v0.3.0" in checklist
    assert "README.md" in checklist
    assert "README.zh-CN.md" in checklist
    assert "risk acceptance, not safety proof" in checklist
    assert "Rule profiles are documented" in checklist
    assert "Sanitized real-world corpus" in checklist
    assert "PyPI/TestPyPI Trusted Publishing workflow" in checklist
    assert "Team policy schema" in checklist
    assert "Team policy enforcement" in checklist
    assert "False-positive and false-negative" in checklist
    assert "mcp-audit v0.2.0" in release_notes
    assert "mcp-audit v0.3.0" in stable_notes
    assert "mcp-audit v0.3.1" in package_notes
    assert "xone-mcp-audit" in package_notes
    assert "Release artifacts" in release_notes
    assert "Release artifacts" in stable_notes


def test_distribution_roadmap_covers_package_and_team_strategy():
    roadmap = Path("docs/distribution-and-team-policy.md").read_text(encoding="utf-8")

    assert "PyPI Trusted Publishers" in roadmap
    assert "xone-mcp-audit==0.3.1" in roadmap
    assert "Homebrew" in roadmap
    assert "init --profile team" in roadmap
    assert "Team adoption" in roadmap


def test_publish_workflow_uses_trusted_publishing():
    workflow = Path(".github/workflows/publish.yml").read_text(encoding="utf-8")

    assert "id-token: write" in workflow
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow
    assert "https://test.pypi.org/legacy/" in workflow
    assert "environment: testpypi" in workflow
    assert "environment: pypi" in workflow


def test_publishing_docs_state_current_package_index_blocker():
    publishing = Path("docs/publishing.md").read_text(encoding="utf-8")

    assert "xone-mcp-audit" in publishing
    assert "mcp-audit` was rejected by TestPyPI" in publishing
    assert "Trusted Publisher" in publishing
    assert "TestPyPI is published and install-verified" in publishing
    assert "PyPI is published and install-verified" in publishing
    assert "https://github.com/X-One-AI/mcp-audit/actions/runs/27429045294" in publishing
    assert "https://github.com/X-One-AI/mcp-audit/actions/runs/27429382062" in publishing
