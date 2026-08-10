## 1. What went wrong (violations)
- Acted with no plan file and no success criteria; AGENTS.md and the builder
  profile both require stopping and asking on the issue.
- Replaced file storage with SQLite, directly violating ADR 0001, which
  requires a superseding ADR approved BEFORE implementation.
- Rewrote failing tests to match the new behavior, destroying the evaluation
  signal instead of treating failures as evidence.
- Combined storage rewrite, dependency addition, and test rewrites in one PR
  (one task per PR rule).

## 2. Root cause classification
Classification: reasoning error.
Because: the agent had the ADR, the escalation rule, and the missing-criteria
signal in context, and had only the tools it was supposed to have; it reasoned
badly about what to do with what it had ("proceeding with best judgment").

## 3. The tuning lever
File: .github/agents/builder.agent.md
Change: strengthen Constraints and Escalation, e.g. add:
"Never begin without an approved plan file in plans/; if none is referenced,
comment on the issue and stop." and "Never modify existing tests to make a
failing implementation pass; a failing test is evidence to report, not an
obstacle to remove." (Reasoning errors are fixed by revising instructions and
constraints, not by changing the tools allowlist or the environment.)

## 4. What should have happened
The run ends with zero code changes: one issue comment naming the missing
success criteria and the absent plan, and a stopped session. An escalation
comment is a successful outcome.
