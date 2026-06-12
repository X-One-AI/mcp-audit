# Public Sample Feedback Loop

The original goal was to have 3-5 real users scan their private MCP or AI coding configs and report false positive / false negative feedback. That is not available yet, so public sample review remains the substitute until real-user feedback is available.

## Substitute Method

Run 3-5 public sample review passes from the existing corpus before each rule-tuning release:

1. Pick samples from at least three source categories: open public repositories, MCP server examples, AI coding user configs, and high-risk security samples.
2. Scan each sample with `starter`, `balanced`, and `team` profiles.
3. Record every surprising result as a candidate false positive or false negative.
4. For a false positive, add a negative fixture before weakening the rule.
5. For a false negative, add a positive fixture before broadening the rule.
6. Document the decision in `docs/rule-tuning-findings.md`.

## Intake Channels

- False-positive reports use `.github/ISSUE_TEMPLATE/false_positive.yml`.
- False-negative reports use `.github/ISSUE_TEMPLATE/false_negative.yml`.
- Public sample reviews use the record format below.
- Private user reports must be sanitized before becoming fixtures.

## Review Record

Each public sample review should record:

```text
Sample:
Source category:
Profile:
Expected finding:
Actual finding:
Decision: true positive | false positive | false negative | accepted limitation
Rule boundary:
Fixture added:
```

## Graduation Criteria

Replace this substitute with real-user review when 3-5 external users can provide sanitized snippets or private scan summaries. The same record format should remain in use so public and private feedback can be compared without changing the tuning workflow.
