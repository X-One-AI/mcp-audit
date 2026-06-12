from pathlib import Path


def test_release_docs_cover_maturity_gates():
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    checklist = Path("docs/release-checklist.md").read_text(encoding="utf-8")

    assert "0.1.0" in changelog
    assert "Baseline creation and suppression" in changelog
    assert "GitHub CI is green" in checklist
    assert "README.md" in checklist
    assert "README.zh-CN.md" in checklist
    assert "risk acceptance, not safety proof" in checklist
    assert "Rule profiles are documented" in checklist
    assert "Sanitized real-world corpus" in checklist


def test_distribution_roadmap_covers_package_and_team_strategy():
    roadmap = Path("docs/distribution-and-team-policy.md").read_text(encoding="utf-8")

    assert "PyPI Trusted Publishers" in roadmap
    assert "Homebrew" in roadmap
    assert "init --profile team" in roadmap
    assert "Team adoption" in roadmap
