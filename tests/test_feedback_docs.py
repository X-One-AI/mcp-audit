from pathlib import Path


def test_false_positive_feedback_workflow_exists():
    template = Path(".github/ISSUE_TEMPLATE/false_positive.yml").read_text(encoding="utf-8")
    false_negative = Path(".github/ISSUE_TEMPLATE/false_negative.yml").read_text(encoding="utf-8")
    tuning = Path("docs/rule-tuning.md").read_text(encoding="utf-8")
    substitute = Path("docs/public-sample-feedback-loop.md").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "False positive report" in template
    assert "False negative report" in false_negative
    assert "Minimal config snippet" in template
    assert "Minimal sanitized config snippet" in false_negative
    assert "Rule ID" in template
    assert "Do not include real secrets" in template
    assert "False-positive reports are product feedback" in tuning
    assert "Add a negative fixture" in tuning
    assert "public sample review" in substitute
    assert "false positive" in substitute
    assert "false negative" in substitute
    assert "False-negative reports" in substitute
    assert "3-5" in substitute
    assert "actions/upload-artifact@v7.0.1" in ci
    assert "mcp-audit-dist-python" in ci
