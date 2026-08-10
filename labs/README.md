# How the labs work

The repository ships in a deliberately incomplete state. Exemplar files are
fully written for you to study (plan-architect, test-engineer, rca-analyst,
ci.yml, AGENTS.md, the instructions files, ADR 0001). Everything a learner is
supposed to internalize is a lab: a starter file with blanks you fill, guided
by TODO(Dn) comments that name the GH-600 domain concept the blank tests.

Rules:
- Every blank is the literal token ____FILL_ME____ next to a TODO(Dn) hint.
- Complete the lab file in place inside labs/.
- Check yourself two ways: run python3 scripts/verify_labs.py (structural
  checks, no spoilers), then diff against solutions/lab-NN/ (one good answer,
  not the only one; wording may differ, mechanics must not).
- Several labs end with "install": copy your completed file into the live
  path (.github/agents/, .github/workflows/, docs/adr/, registry/) so the
  following tutorial exercises can actually run. The tutorial tells you when.

Lab map:
  lab-01  D1  Write an agent task with defined inputs, outputs, success criteria
  lab-02  D1  Complete the implementation plan (task breakdown + criteria)
  lab-03  D2  Author the builder agent profile (tools allowlist, escalation)
  lab-04  D5  Author the security-reviewer as a subagent (invocability, contract)
  lab-05  D2  Configure the agent's ephemeral environment (setup steps)
  lab-06  D3  Write ADR 0002 without violating ADR 0001
  lab-07  D4  Classify a failure and pick the matching tuning lever
  lab-08  D2/D6  Register an MCP server with per-tool risk tags
  lab-09  Reliable workflows  Wire the plan agent into Actions with gates
  lab-10  Agentic workflows  Constrain a natural-language automation
  lab-11  D6  Wire a preToolUse hook and reason about cloud-agent hook behavior
  lab-12  D5  Orchestrate specialist agents in Actions (matrix, artifacts, concurrency)
