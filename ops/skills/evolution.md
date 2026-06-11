# Constraint And Skill Evolution

Project constraints and local skill overlays should evolve automatically through evidence, but not silently.

## Evolution Loop

```text
1. Observe a repeated issue, review finding, user request, or release lesson.
2. Record it in the knowledge base.
3. Decide whether it should become:
   - a rule
   - a constraint
   - a role overlay
   - a test fixture
   - documentation
4. Add or update the local file.
5. Add a decision note when the change affects future work.
6. Keep the public README unchanged unless users need it for first-run success.
```

## What Can Evolve

```text
- rule severity guidance
- false-positive handling
- report contract expectations
- QA fixture requirements
- local role overlays
- release gates
- project knowledge
```

## What Cannot Evolve Automatically

```text
- global OPT skill source files
- public security claims
- runtime enforcement promises
- destructive behavior
- telemetry or network behavior
```

Those require explicit review and approval.

## Review Trigger

Update local constraints or overlays when any of these happen:

```text
- the same review comment appears twice
- a false positive affects a real user
- a rule severity is disputed
- a release misses a production constraint
- a contributor is confused by the same docs twice
```
