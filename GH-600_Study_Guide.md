# GH-600 Study Guide: Developing in Agentic AI Systems
### GitHub Certified: Agentic AI Developer

Prepared August 2026. Based on the official Microsoft study guide (updated May 13, 2026), the official Learn modules, and the GitHub Copilot documentation the exam draws from.

---

## 1. Exam Facts

| Item | Detail |
|---|---|
| Exam | GH-600: Developing in Agentic AI Systems |
| Certification earned | GitHub Certified: Agentic AI Developer |
| Passing score | 700 (scaled) |
| Level | Intermediate |
| Related instructor-led course | GH-600T00-A (1 day, ~24 hours self-paced equivalent) |
| Feature coverage | Mostly GA features; Preview features can appear if commonly used |
| Extra time | +30 minutes available if the exam is not in your preferred language |

The core framing that runs through every domain: **GitHub is the system of record and control plane** for agent activity. Almost every question resolves to "which GitHub-native control, artifact, or configuration achieves this." If two answers seem right, pick the one that uses a GitHub platform mechanism (PR, issue, branch protection, ruleset, Actions, agent profile) over a generic or external one.

---

## 2. Domain Weightings and Time Budget

| Domain | Weight | Suggested share of study time |
|---|---|---|
| 1. Prepare agent architecture and SDLC processes | 15–20% | 15% |
| 2. Implement tool use and environment interaction | 20–25% | 25% |
| 3. Manage memory, state, and execution | 10–15% | 10% |
| 4. Perform evaluation, error analysis, and tuning | 15–20% | 15% |
| 5. Orchestrate multi-agent coordination | 15–20% | 15% |
| 6. Implement guardrails and accountability | 10–15% | 20% |

Domain 2 is the heaviest and the most configuration-specific — budget accordingly. Domain 6 gets extra time here despite its lower weight because its questions come almost verbatim from the risks-and-mitigations documentation, which rewards close reading.

---

## 3. Official Learning Material Map

### Learning Path: Developing in Agentic AI Systems Part 1 of 2
Covers Domains 1 and 2.

**Module 1 — Foundations of Agentic AI in GitHub** (8 units)
- Define agentic AI in the SDLC; distinguish agents from assistants
- The plan → act → evaluate lifecycle
- GitHub as system of record and control plane
- Responsibilities, risks, anti-patterns, traceability requirements
- The contributor model applied to agent-generated work
- Prerequisites it assumes: GitHub Actions, status checks, CODEOWNERS, branch protection, rulesets

**Module 2 — Designing Agent Architecture and SDLC Integration**
- Separating planning, reasoning, and execution
- Structured plan output and plan validation
- Gating action behind checks and approvals

**Module 3 — Tooling, MCP, and Agent Execution Environments**
- Tool selection, configuration, and permissions
- MCP servers, registries, allow lists
- Execution contexts, repository scoping, CI invocation, branch-based scope

### Learning Path Part 2 of 2
A second path (learn.github.developing-agentic-systems-2) covers the remaining domains: memory/state, evaluation and tuning, multi-agent orchestration, and guardrails. It is referenced by the GH-600T00 course syllabus. If its modules are not yet visible in your Learn catalog, the GitHub documentation in section 4 is the substitute — the exam bullets for Domains 3–6 map directly to those docs.

### Official documentation linked from the study guide
| Domain | Doc |
|---|---|
| 1 | Preparing to use custom agents in your organization (docs.github.com: administer-copilot → prepare-for-custom-agents) |
| 2, 5 | Custom agents via the Copilot SDK (docs.github.com: copilot-sdk → custom-agents) |
| 3 | About GitHub Copilot Memory (docs.github.com: concepts/agents/copilot-memory) |
| 4 | Implementation planner tutorial (customization library, custom agents) |
| 6 | Building guardrails for Copilot cloud agent + Risks and mitigations for Copilot cloud agent (the study guide mashes these two URLs into one broken link; they are separate pages, read both) |

### Supplemental documentation worth adding
The official list is thin. These pages fill gaps the exam bullets clearly touch:
- About custom agents + Custom agents configuration reference (agent profiles, YAML frontmatter, tools property, mcp-servers block)
- Configure MCP server access for your organization or enterprise (registry URL, Allow all vs Registry only)
- MCP allowlist enforcement reference
- About Copilot cloud agent (branch behavior, PR workflow, Actions execution)
- Responsible use of Copilot cloud agent
- Customizing or disabling the firewall for Copilot
- Custom instructions docs: AGENTS.md, .github/copilot-instructions.md, .instructions.md files, copilot-setup-steps.yml

---

## 4. Domain-by-Domain Study Notes

### Domain 1 — Prepare agent architecture and SDLC processes (15–20%)

**Core ideas to internalize**
- Agents differ from assistants: assistants suggest inside your editing loop; agents plan, act, and produce reviewable artifacts autonomously across the SDLC.
- The agent lifecycle is plan → act → evaluate. Exam questions test that planning is configured as a distinct phase from execution, with a human or automated gate between them.
- Structured plans: configure the agent to emit an inspectable plan artifact (issue comment, plan file, draft PR description) that can be validated before any action runs.
- Suitable tasks for agents: repetitive, well-bounded, verifiable work (scaffolding, test generation, dependency upkeep, documentation). Anti-patterns: vague open-ended goals, tasks without success criteria, unbounded permission grants, letting the agent self-approve, skipping review because output "looks right."
- Every agent task needs defined inputs, outputs, and success criteria before the agent starts.
- Observability without slowing delivery: inspectable artifacts inside standard tooling (PRs, session logs, checks) rather than added manual approval steps that don't reduce risk.

**The contributor model** — agent-generated work is treated like any other contributor's work: it arrives on a branch, in a PR, subject to reviews, required checks, CODEOWNERS, and branch protection. This is the single most quotable concept in the exam's framing.

**Org preparation** — custom agents can be defined at repository level (.github/agents/NAME.agent.md), organization level (agents folder in the org's .github or .github-private repository), and enterprise level (/agents/NAME.md in a designated .github-private repository). Know who can create each and how availability flows down.

### Domain 2 — Implement tool use and environment interaction (20–25%)

**Agent profiles (custom agents)**
- Defined in Markdown files with YAML frontmatter (.agent.md), located in .github/agents for a repo, or org/enterprise shared locations.
- Frontmatter properties: name (optional display name), description, tools, mcp-servers. The body is the prompt.
- Canonical tool names: read (file contents), search (repository search, not the internet), edit (modify/create files), execute (shell), agent (invoke another custom agent; aliases agent, custom-agent, Task). web and todo are not available on the cloud agent.
- Tools property behavior: omit it entirely or use tools: ["*"] to enable all available tools; tools: [] disables all tools; otherwise list specific tools, including MCP tools using the server/tool naming pattern (for example custom-mcp/tool-1). server/* exposes every tool on one server.
- MCP servers can be declared in the agent profile itself or inherited from repository-level MCP configuration. Secrets and environment variables are referenced from Agents secrets and variables at org or repo level, using ${{ secrets.NAME }}-style syntax.
- Custom agents are usable from the agents panel on GitHub.com, issue assignment, PRs, Copilot CLI (as subagents with their own context window), and IDEs.

**MCP configuration**
- Key naming by surface: mcp-servers in custom-agent YAML frontmatter; mcpServers in JSON MCP config files. Transport type is decided by config shape: command+args means local/stdio (a subprocess over stdin/stdout); a top-level url means remote, http for Streamable HTTP or sse for legacy Server-Sent Events; a url inside args behind a command like npx is a local bridge, so the type stays local. Cloud agent: MCP secret/variable names must start with COPILOT_MCP_, and remote servers requiring OAuth are not supported. GitHub's MCP server is read-only by default and scoped to the source repository; Playwright MCP defaults to localhost. Adapting .vscode/mcp.json for the cloud agent: add tools, replace inputs/envFile with env, store credentials as Agents secrets/variables. Firewall allowlist (network egress) and MCP allowlist (which servers may run) are different controls.
- Adding an MCP server as a tool: declare it in the agent profile's mcp-servers block (type, command/URL, args, env, tools) or in repository Copilot settings.
- GitHub remote MCP server: the hosted GitHub MCP server that gives agents access to GitHub APIs without local setup — know it exists and when to prefer remote over local.
- MCP registry: an internal catalog of approved MCP servers. Configured by admins at enterprise level (AI controls → MCP) or org level (Settings → Policies → Copilot). Serves discovery (approved servers appear as installable) and allowlisting.
- Allowlist policy has two settings: **Allow all** (default; registry servers are recommendations) and **Registry only** (servers not in the registry are blocked at runtime). Enforcement is tied to the org/enterprise that assigns the Copilot seat. Local servers must appear in the registry with an exactly matching server ID. Registry-only blocks at runtime; strict install-time prevention is not the mechanism.

**Execution environment**
- Copilot cloud agent runs in an ephemeral, sandboxed environment powered by GitHub Actions, with a firewall limiting internet access (customizable, can be disabled — but disabling is the risky answer, not the right one).
- Repository scoping: the agent only accesses the repository it's working in.
- Branch-based scope: the agent can only create and push to branches beginning with copilot/. It cannot push to main/master, cannot force-push, and cannot run arbitrary git commands against GitHub.
- CI invocation: agents can be invoked from workflows; Actions workflows triggered by agent-created PRs require approval from a user with write access before running.
- Environment constraints and dependencies are handled with copilot-setup-steps.yml and custom instructions (AGENTS.md, .github/copilot-instructions.md, path-scoped .instructions.md files).

**Safe execution and error handling**
- Error handling, retries with bounds, rollbacks (revert PRs, branch deletion — never history rewrites), and escalation paths (hand off to a human via issue comment, review request, or stopping with a reported failure state).
- Traceability: agent commits are authored by Copilot and co-authored with the developer who assigned the task; session logs record what the agent did and why.

### Domain 3 — Manage memory, state, and execution (10–15%)

**Memory types**
- Short-term: the session/context window for the current task.
- Long-term: Copilot Memory — repository-level facts and user-level preferences that persist across sessions.
- External: durable artifacts outside the model — issues, PR descriptions, plan files, committed docs.

**Copilot Memory specifics (public preview — still examinable)**
- Used by Copilot cloud agent, Copilot code review, and Copilot CLI. Memories captured by one feature can be used by another (cloud agent learns a DB connection pattern → code review flags inconsistencies with it).
- Scope rules: Copilot CLI applies repository-level facts plus the initiating user's preferences; Copilot code review uses repository-level facts only.
- Off by default, opt-in per user; memories are only created/used when enabled for the initiating user.
- Each memory is stored with citations to specific code locations that support it — this is the validity mechanism as code evolves.
- Managed and curated in Repository Settings → Copilot → Memory (review, delete).
- Central design challenge the docs emphasize: keeping stored knowledge valid as code changes across branches and time — expiration, pruning, and validation against current code state.

**State and drift**
- Persist task progress and decisions as durable artifacts (issues, plan files, PR bodies) so work can resume without repeating steps or contradicting earlier decisions.
- Context drift: detect divergence during long executions by comparing actions against the approved plan; correct by re-grounding on the plan artifact or escalating.
- Continuity across tools: share state through the repository (files, issues, PRs) rather than assuming shared context; prevent conflicting or stale context by scoping memory to task-relevant information and validating against the current branch.

### Domain 4 — Perform evaluation, error analysis, and tuning (15–20%)

- Success criteria: specify expected outcomes and operational constraints per task before running the agent. Align evaluation criteria with development intent, not just "code compiles."
- Evaluation signals: qualitative (review feedback, plan quality) and quantitative (test pass rates, scan findings, check outcomes). Generate signals with automated scanning — CodeQL/code scanning, secret scanning, dependency review, linters, required checks. Cloud agent by default checks its own generated code for security issues and gets a second opinion from Copilot code review before finalizing the PR (no GHAS license required for this built-in validation).
- Failure analysis inputs: session logs, emitted plans, traces, outputs, and workflow artifacts.
- Root cause classification — know these three buckets cold: **reasoning errors** (bad plan, wrong approach), **tool misuse** (wrong tool, bad parameters, missing permissions), **context/environment issues** (stale or missing context, dependency/setup failures).
- Tuning levers, matched to root cause: revise instructions/prompts and workflows or constraints (reasoning errors); refine tool access and configuration (tool misuse); refine memory usage and setup steps (context/environment issues).
- The implementation-planner tutorial is the worked example: a planning-only custom agent whose profile restricts it to producing structured plans, specs, and task breakdowns with acceptance criteria — no code changes. Understand why separating a planner agent improves evaluability.

### Domain 5 — Orchestrate multi-agent coordination (15–20%)

- Orchestration patterns: sequential handoff (planner → implementer → tester), parallel specialists with isolation, and coordinator/subagent (in Copilot CLI, custom agents run as subagents with their own context windows so the main agent keeps high-level coordination).
- Isolation for parallel execution: separate branches, separate ephemeral environments, scoped permissions per agent — so agents can't clobber each other.
- Conflict detection and resolution: overlapping code changes surface as merge conflicts in PRs; duplicated effort and contradictory outputs are caught in review and by comparing plan artifacts. Resolution goes through normal PR mechanics.
- Multi-agent observability: each agent produces reviewable artifacts (PRs, logs, plan files); document decisions, handoffs, and outcomes across agents; post-hoc analysis via session logs and PR history.
- Failure response: identify failed, partial, or stalled executions; recovery patterns include rollback (revert), retry, and human-in-the-loop takeover.
- Agent lifecycle: add agents by adding profiles; update or replace by editing profiles (versioned in git, so changes are auditable and don't disrupt in-flight work); retire by removing the profile while git history preserves auditability.

### Domain 6 — Implement guardrails and accountability (10–15%)

**Autonomy levels**
- Classify actions by operational, security, and compliance risk; right-size human intervention to risk. High-risk or irreversible actions get explicit authorization; low-risk actions run autonomously.
- Key principle the exam words carefully: preserve execution velocity by minimizing approvals that do not materially reduce risk. Adding approvals everywhere is a wrong answer; removing them everywhere is also wrong.

**Built-in mitigations for Copilot cloud agent — memorize this list**
- Only users with **write access** can trigger the agent (assign issues, leave actionable comments); comments from others are never presented to it.
- Pushes restricted to **copilot/ branches**; no pushes to main/master; no force-push or history rewriting; tokens strictly limited.
- Actions workflows on agent PRs **don't run until approved** by a user with write access.
- The person who assigned the task **cannot approve** the resulting PR — required-review and branch protection semantics are preserved.
- **Firewall** limits internet access to mitigate data exfiltration; customizable, disableable (with warnings).
- **Prompt injection mitigations**: hidden characters filtered from input; HTML comments in issues/PR comments are not passed to the agent.
- **Auditability**: commits authored by Copilot, co-authored with the assigning developer; session logs preserved.
- Built-in security validation: generated code is checked for vulnerabilities, hardcoded secrets, insecure dependencies, plus a Copilot code review pass, before the PR is finalized.

**Enterprise guardrail setup (build-guardrails tutorial)**
- Set policies at enterprise level as a baseline; org owners can restrict further (never loosen).
- Decide which orgs/repos enable the agent; which MCP servers are allowed (registry + Registry only for least privilege).
- Keep data the agent shouldn't see in Actions secrets/variables (agent can't access them); provide what it does need via Agents secrets and variables at org/repo level.
- Runners: prefer GitHub-hosted (fresh VM per session); if self-hosted, use ephemeral runners; orgs can pin the agent to a specific runner label.
- Least privilege throughout: scoped tool lists in agent profiles, scoped permissions, scoped execution contexts.

---

## 4.5 Deep-dive additions: CLI, sessions, hooks, and Actions orchestration

**Copilot CLI command surface.** copilot -p "..." is non-interactive prompt mode; --agent=NAME runs a custom agent; --allow-tool/--deny-tool/--available-tools scope capability per invocation; --no-ask-user prevents interactive questions hanging CI (GitHub's CI examples authenticate with COPILOT_GITHUB_TOKEN, while newer runs can use GITHUB_TOKEN with the copilot-requests: write permission); --autopilot continues autonomously locally; --resume <id> and --continue restore sessions; --output-format=json for machine consumption; copilot init generates repository instructions. Slash commands: /plan, /review, /pr, /mcp, /agent, /session, /ide, /delegate (hand off to the cloud agent; the & prompt prefix does the same), /fleet (split into parallel subagents).

**Session state and logs (Domain 3).** Everything lives under ~/.copilot/ (override with COPILOT_HOME; cache with COPILOT_CACHE_HOME): agents/ (user custom agents), config.json, mcp-config.json, logs/process-*.log, session-state/<id>/events.jsonl, session-store.db, settings.json. Log forensics: resume=true plus a loaded events.jsonl line means a resumed session; "Visual Studio Code connected" means an IDE is attached; "mcp loaded ... servers=[...]" means MCP is active, and --disable-builtin-mcps in argv means it is not. SDK: a stable sessionId enables resumeSession; disconnect() keeps session data, deleteSession() destroys it; provider keys and in-memory tool state are never persisted. Sharp boundary: session persistence is not Copilot Memory, and neither is secret storage.

**Hooks (Domain 6).** Repository hooks in .github/hooks/*.json apply to CLI and cloud agent; user hooks in ~/.copilot/hooks/ never reach the cloud agent. Events worth knowing: sessionStart/sessionEnd, userPromptSubmitted, preToolUse (the big one: returns allow, deny with permissionDecisionReason, or ask, and the non-interactive cloud agent treats ask as deny), postToolUse and postToolUseFailure, agentStop, subagentStart/subagentStop (matcher filters by agent name), errorOccurred; permissionRequest is CLI-only and never the cloud-agent answer. Command hooks: type command with bash, powershell, or cross-platform command, plus cwd, env, timeoutSec (default 30), and an anchored-regex matcher over the hook-level tool name. Hook tool names map to agent tools: view=read, grep/glob=search, edit/create=edit, bash/powershell=execute, task=agent, web_fetch=web. Cloud agent hooks run on Linux in /workspace, so powershell-only entries do nothing there. Hooks generally fail open: they complement, never replace, branch protection and required checks.

**Actions orchestration (Domain 5).** Pipeline pattern: specialist jobs run copilot --agent=X, upload findings as artifacts (upload-artifact inputs: name, path, retention-days, if-no-files-found warn/error/ignore, overwrite), a consolidate job declares needs: [review, audit], downloads both, and appends to $GITHUB_STEP_SUMMARY. Matrix fan-out: strategy.matrix.agent: [reviewer, auditor] with fail-fast: false so one leg's failure does not cancel the rest; up to 256 jobs per run. Concurrency for agents pushing to one PR branch: workflow-level group ${{ github.workflow }}-${{ github.head_ref || github.run_id }} with cancel-in-progress: true keeps only the latest run; queue: max preserves every run in order and must never be combined with cancel-in-progress. Contexts to keep straight: head_ref (PR source) vs base_ref (target), actor vs triggering_actor (rerun), run_id vs run_number vs run_attempt.

**Accountability evidence (Domains 4 and 6).** Control types: preventive (least privilege, rulesets, allowlists, firewall, reviews), detective (session/workflow logs, artifacts, CodeQL, secret scanning, dependency review, audit logs), corrective (revert PR, stop session, unassign/reassign Copilot, rotate secrets, narrow tools). Stalled-agent recovery: View session on the PR; @copilot comment (write access required); unassign then reassign for issue work; Approve and run workflows when a Copilot push leaves workflows pending, which is an accountability gate, not an error. Audit log: manual artifact deletion is the artifact.destroy event with actor, repo, created_at/@timestamp, operation_type, user_agent fields, found in the org or enterprise audit log.

**Extra file inventory.** Beyond the paths in section 4: .github/prompts/*.prompt.md (reusable prompts), .github/skills/<skill>/SKILL.md (agent skills), .github/hooks/*.json (hooks), .mcp.json / .github/mcp.json / .vscode/mcp.json / ~/.copilot/mcp-config.json (MCP config per surface). Frontmatter extras: disable-model-invocation prevents inferred invocation; metadata carries arbitrary extras; and the classic trap: description is the required field, name is not.

## 5. Four-Week Study Plan

Assumes roughly 5–7 hours per week. Compress to two weeks at double pace if needed — with your production agentic AI background, Domains 1, 4, and 5 are mostly vocabulary alignment.

**Week 1 — Foundations and framing (Domains 1)**
- Read the official study guide end to end; the exam uses its exact phrasing.
- Complete Module 1 (Foundations of Agentic AI in GitHub), including the knowledge check.
- Complete Module 2 (Designing Agent Architecture and SDLC Integration).
- Anchor the vocabulary: system of record, control plane, contributor model, plan → act → evaluate.

**Week 2 — Tooling and MCP (Domain 2, the big one)**
- Complete Module 3 (Tooling, MCP, and Agent Execution Environments).
- Read: About custom agents, Custom agents configuration reference, Configure MCP server access, MCP allowlist enforcement.
- Hands-on lab (see section 6): build two custom agents and wire up an MCP server with a restricted tools list.

**Week 3 — Memory, evaluation, multi-agent (Domains 3–5)**
- Read: About Copilot Memory (+ the GitHub blog post on the agentic memory system), the implementation-planner tutorial, custom agents SDK docs.
- Hands-on: enable Copilot Memory on a test repo, run cloud agent tasks, inspect and curate stored memories; run a planner agent → implementer agent handoff.
- Drill the root-cause taxonomy (reasoning / tool misuse / context-environment) against real session logs.

**Week 4 — Guardrails, review, and mock testing (Domain 6 + consolidation)**
- Read: Risks and mitigations, Building guardrails, Responsible use of Copilot cloud agent. Memorize the built-in mitigations list.
- Community resource: the jtur671/gh-600-study-guide repo on GitHub (free) has 67 flashcards, a 41-question mock exam, and 6 labs — use the mock exam as your readiness check.
- Try the exam sandbox (aka.ms/examdemo) to learn the question interface.
- Re-read the study guide bullets one final time; for any bullet you can't explain in one sentence, go back to the mapped doc.

---

## 6. Hands-On Labs (do these — the exam is written by practitioners)

1. **Custom agent basics.** In a test repo, create .github/agents/test-specialist.agent.md with name, description, a restricted tools list, and a prompt. Assign it an issue from the agents panel and watch the full flow: plan, copilot/ branch, draft PR, session log.
2. **Planner/implementer split.** Create an implementation-planner agent (documentation-only, no code tools) that outputs a structured plan file, then a second agent that implements from that plan. This exercises Domains 1, 4, and 5 in one lab.
3. **MCP wiring.** Add an MCP server to an agent profile with an env secret from Agents secrets and variables, and enable only one of its tools in the tools property. Then, if you have org admin on a test org, configure a registry URL and flip the policy from Allow all to Registry only and observe runtime blocking.
4. **Guardrails audit.** On the test repo: confirm the agent can't push outside copilot/, confirm Actions wait for approval on its PR, confirm the assigner can't approve the PR, and review the firewall settings.
5. **Memory curation.** Enable Copilot Memory, run several tasks, then review memories in Repository Settings → Copilot → Memory. Delete one and observe behavior.
6. **Failure forensics.** Deliberately give an agent a vague task with no success criteria. Read the session log and classify what went wrong using the three root-cause buckets, then fix it by revising the profile, not the prompt-of-the-day.

---

## 7. High-Yield Facts (quick recall list)

- Passing score: 700.
- GitHub = system of record and control plane; agent work follows the contributor model.
- Plan → act → evaluate; planning configured separately from execution; plans validated before action.
- Agent profiles: Markdown + YAML frontmatter; repo (.github/agents), org (.github or .github-private/agents), enterprise (.github-private /agents) levels.
- tools omitted or ["*"] = all tools; MCP tools named server/tool.
- MCP allowlist: Allow all vs Registry only; runtime blocking; server IDs must match exactly; tied to the seat-assigning org/enterprise.
- Cloud agent: ephemeral Actions environment, firewalled, repo-scoped, copilot/ branches only, no force-push, Actions gated on human approval, assigner can't approve, commits co-authored, hidden-character/HTML-comment prompt-injection filtering, built-in security validation without a GHAS license.
- Copilot Memory: preview, opt-in, off by default; used by cloud agent, code review, CLI; cross-feature sharing; citations back each memory; code review uses repo facts only; managed in repo settings.
- Root causes: reasoning errors, tool misuse, context/environment issues — and tuning levers map one-to-one.
- CLI custom agents run as subagents with their own context window; main agent keeps planning and coordination.
- Guardrails: enterprise policy baseline, orgs restrict further; secrets stay in Actions secrets; GitHub-hosted or ephemeral runners; minimize approvals that don't materially reduce risk.
- Tools: read/search/edit/execute/agent; tools:[] disables; omitted may enable all; server/tool vs server/*.
- mcp-servers (YAML) vs mcpServers (JSON); local/stdio = command+args, http/sse = url; COPILOT_MCP_ secret prefix; no OAuth remote MCP on cloud agent.
- Hooks: .github/hooks/*.json; preToolUse decisions allow/deny/ask (ask=deny on cloud agent); anchored matcher; Linux /workspace; fail open; permissionRequest is CLI-only.
- Orchestration: needs, matrix (fail-fast:false, 256 cap), artifacts (if-no-files-found), $GITHUB_STEP_SUMMARY, concurrency group workflow+head_ref||run_id, cancel-in-progress vs queue:max (never both).
- Sessions: ~/.copilot/session-state/<id>/events.jsonl; resume=true; --resume/--continue; COPILOT_HOME.
- Recovery: View session, @copilot, unassign/reassign, Approve and run workflows. Audit: artifact.destroy.

---

## 8. Resource Links

Official
- Study guide: learn.microsoft.com/credentials/certifications/resources/study-guides/gh-600
- Certification page: learn.microsoft.com/credentials/certifications/agentic-ai-developer
- Learning path part 1: learn.microsoft.com/training/paths/gh-developing-agentic-systems-1
- Course GH-600T00: learn.microsoft.com/training/courses/gh-600t00
- Exam sandbox: aka.ms/examdemo

GitHub docs (docs.github.com/en/copilot)
- concepts/agents/cloud-agent/about-custom-agents
- reference/custom-agents-configuration
- concepts/agents/copilot-memory
- concepts/agents/cloud-agent/risks-and-mitigations
- tutorials/cloud-agent/build-guardrails
- how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access
- reference/mcp-allowlist-enforcement
- responsible-use/copilot-cloud-agent
- tutorials/customization-library/custom-agents/implementation-planner

Community
- gist.github.com/naim149 GH-600 Public Study Guide (May 2026): strong artifact-reading workbook; the source of the hooks, CLI session, MCP transport, and concurrency depth in section 4.5
- github.com/jtur671/gh-600-study-guide — flashcards, 41-question mock exam, labs, Anki decks
- github.com/github/awesome-copilot — community custom agent examples
- github.blog — changelog entries for MCP registry/allowlist rollout and Copilot Memory
