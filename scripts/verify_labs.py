#!/usr/bin/env python3
"""Structural lab checker. No spoilers: it checks shape, not wording.
Run from the repo root: python3 scripts/verify_labs.py [lab-number ...]
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MARK = "____FILL_ME____"
results = []


def check(lab, name, ok, hint=""):
    results.append((lab, name, ok, hint))


def text(p):
    return (ROOT / p).read_text()


def no_blanks(lab, p):
    t = text(p)
    check(lab, "all blanks filled", MARK not in t,
          f"{t.count(MARK)} blank(s) remain in {p}")
    return t


def load_yaml(lab, p):
    if yaml is None:
        check(lab, "yaml parse (pyyaml not installed)", True, "pip install pyyaml for full checks")
        return None
    try:
        docs = list(yaml.safe_load_all(text(p)))
        check(lab, "yaml parses", True)
        return docs[0] if docs else None
    except Exception as e:
        check(lab, "yaml parses", False, str(e))
        return None


def lab01():
    t = no_blanks("lab-01", "labs/lab-01-agent-task/task-issue.md")
    check("lab-01", "names at least 3 in-scope files", t.count("/") >= 3,
          "list concrete file paths under In scope")
    check("lab-01", "criteria mention 404", "404" in t,
          "unknown-id behavior must be a criterion")
    check("lab-01", "criteria mention tests", "pytest" in t.lower() or "test" in t.lower())


def lab02():
    t = no_blanks("lab-02", "labs/lab-02-plan/plan-1-delete-task.md")
    rows = [l for l in t.splitlines() if l.strip().startswith("|") and "Task" not in l and "---" not in l]
    check("lab-02", "at least 2 breakdown rows", len(rows) >= 2)
    check("lab-02", "backend and frontend are separate tasks",
          not any(("main.py" in r or "storage.py" in r) and "App.jsx" in r for r in rows),
          "one PR per task: do not mix backend and frontend files in one row")


def lab03():
    t = no_blanks("lab-03", "labs/lab-03-builder-profile/builder.agent.md")
    m = re.search(r"^tools:\s*(\[.*\])", t, re.M)
    check("lab-03", "tools is an explicit list", bool(m), "e.g. tools: [\"read\", ...]")
    if m:
        check("lab-03", "allowlist is minimal (no '*')", "*" not in m.group(1),
              "['*'] grants all tools; list the minimum")
        check("lab-03", "includes execute for running tests", "execute" in m.group(1),
              "canonical tool names: read, search, edit, execute, agent")
        check("lab-03", "includes agent tool for delegation", "agent" in m.group(1),
              "the builder delegates to security-reviewer; subagent invocation needs the agent tool")
    check("lab-03", "description filled meaningfully",
          len(re.search(r"^description:\s*(.+)$", t, re.M).group(1)) > 40)


def lab04():
    t = no_blanks("lab-04", "labs/lab-04-subagent-profile/security-reviewer.agent.md")
    check("lab-04", "subagent-only flag present", re.search(r"^user-invocable:\s*false", t, re.M) is not None,
          "one frontmatter property, value false")
    m = re.search(r"^tools:\s*(\[.*\])", t, re.M)
    check("lab-04", "read-only toolset (no edit/execute)",
          bool(m) and "edit" not in m.group(1) and "execute" not in m.group(1) and "shell" not in m.group(1),
          "a reviewer that can edit or execute is a design smell")
    check("lab-04", "output returns to parent, not user",
          "parent" in t.lower(), "state the return path explicitly")


def lab05():
    t = no_blanks("lab-05", "labs/lab-05-setup-steps/copilot-setup-steps.yml")
    d = load_yaml("lab-05", "labs/lab-05-setup-steps/copilot-setup-steps.yml")
    if d:
        jobs = d.get("jobs", {})
        check("lab-05", "job named copilot-setup-steps", "copilot-setup-steps" in jobs,
              "the platform matches on this exact job name")
        job = jobs.get("copilot-setup-steps", {})
        perms = job.get("permissions", {})
        check("lab-05", "least privilege: contents read only",
              perms == {"contents": "read"}, "permissions: contents: read")
        steps = str(job.get("steps", ""))
        check("lab-05", "python setup present", "setup-python" in steps and "requirements.txt" in steps)
        check("lab-05", "node setup present", "setup-node" in steps and "npm" in steps)


def lab06():
    t = no_blanks("lab-06", "labs/lab-06-adr/0002-created-at-timestamp.md")
    check("lab-06", "respects ADR 0001 (no database)",
          not re.search(r"\b(sqlite|postgres|database migration to|sqlalchemy)\b", t, re.I)
          or "0001" in t, "extend the record shape; do not reopen storage")
    check("lab-06", "commits to a format", "8601" in t or re.search(r"\d{4}-\d{2}-\d{2}T", t) is not None)
    check("lab-06", "handles legacy records", "null" in t.lower() or "backfill" in t.lower() or "existing" in t.lower())


def lab07():
    t = no_blanks("lab-07", "labs/lab-07-forensics/FORENSICS.md")
    m = re.search(r"Classification:\s*(.+)", t)
    check("lab-07", "uses one of the three categories",
          bool(m) and any(k in m.group(1).lower() for k in ["reasoning", "tool misuse", "context"]))
    check("lab-07", "tuning lever names a file", ".agent.md" in t or "AGENTS.md" in t,
          "the lever is a versioned file change, not a chat message")


def lab08():
    no_blanks("lab-08", "labs/lab-08-registry/tasks-backup.yaml")
    d = load_yaml("lab-08", "labs/lab-08-registry/tasks-backup.yaml")
    if d:
        check("lab-08", "status is proposed (not approved)",
              d["metadata"].get("status") == "proposed")
        refs = d["spec"]["auth"].get("secretRefs")
        check("lab-08", "secret referenced by name in a list",
              isinstance(refs, list) and len(refs) >= 1 and all(isinstance(x, str) and " " not in x for x in refs))
        tools = {t["name"]: t for t in d["spec"]["tools"]}
        rb = tools.get("restore-backup", {})
        check("lab-08", "restore tagged irreversible + gated",
              rb.get("access") == "irreversible" and rb.get("requiresGate") is True,
              "overwriting live data destroys the old state")
        cb = tools.get("create-backup", {})
        check("lab-08", "create-backup tagged honestly (write, no gate)",
              cb.get("access") == "write" and cb.get("requiresGate") is False)


def lab09():
    t = no_blanks("lab-09", "labs/lab-09-plan-workflow/plan-agent.yml")
    d = load_yaml("lab-09", "labs/lab-09-plan-workflow/plan-agent.yml")
    check("lab-09", "copilot-requests: write permission", "copilot-requests" in t)
    check("lab-09", "defensive gate on label", "needs-plan" in t and "workflow_dispatch" in t)
    check("lab-09", "step output via GITHUB_OUTPUT", "GITHUB_OUTPUT" in t)
    check("lab-09", "--yolo for non-interactive CI", "--yolo" in t)
    check("lab-09", "spend cap flag present", "--max-ai-credits" in t)
    if d:
        jobs = d.get("jobs", {})
        gate = jobs.get("await-plan-approval", {})
        check("lab-09", "downstream declares needs: plan", gate.get("needs") in ("plan", ["plan"]))
        env = gate.get("environment")
        check("lab-09", "environment gate plan-approval",
              env == "plan-approval" or (isinstance(env, dict) and env.get("name") == "plan-approval"))
        plan = jobs.get("plan", {})
        outs = plan.get("outputs", {})
        check("lab-09", "job output wired from step", "steps.emit.outputs" in str(outs.get("plan_ready", "")))


def lab10():
    t = no_blanks("lab-10", "labs/lab-10-agentic-workflow/issue-triage.md")
    fm = t.split("---")[1] if t.count("---") >= 2 else ""
    check("lab-10", "trigger on opened only", "opened" in fm)
    check("lab-10", "permissions read-all", "read-all" in fm)
    check("lab-10", "safe-output add-comment declared", "add-comment" in fm)
    check("lab-10", "final constraint bounds comments", "one comment" in t.lower() or "more than one" in t.lower())




def lab11():
    t = no_blanks("lab-11", "labs/lab-11-hooks/block-push.json")
    q = no_blanks("lab-11", "labs/lab-11-hooks/QUESTIONS.md")
    import json as _json
    try:
        d = _json.loads(text("labs/lab-11-hooks/block-push.json"))
        check("lab-11", "json parses", True)
        hooks = d.get("hooks", {})
        check("lab-11", "event is preToolUse", "preToolUse" in hooks,
              "the pre-execution event; permissionRequest is CLI-only")
        entry = (hooks.get("preToolUse") or [{}])[0]
        check("lab-11", "matcher filters to bash", entry.get("matcher") == "bash",
              "anchored regex on the hook toolName")
    except Exception as e:
        check("lab-11", "json parses", False, str(e))
    ql = q.lower()
    check("lab-11", "Q1 explains ask->deny in cloud", "deny" in ql and ("non-interactive" in ql or "noninteractive" in ql or "no user" in ql))
    check("lab-11", "Q2 names .github/hooks", ".github/hooks" in q)
    check("lab-11", "Q4 falls back to branch protection", "branch protection" in ql or "ruleset" in ql,
          "hooks fail open; name the enforceable repo policy")


def lab12():
    t = no_blanks("lab-12", "labs/lab-12-orchestration/agent-pipeline.yml")
    d = load_yaml("lab-12", "labs/lab-12-orchestration/agent-pipeline.yml")
    check("lab-12", "concurrency groups by workflow+head_ref", "github.workflow" in t and "github.head_ref" in t and "github.run_id" in t)
    check("lab-12", "cancel-in-progress true", re.search(r"cancel-in-progress:\s*true", t) is not None)
    check("lab-12", "fail-fast false", re.search(r"fail-fast:\s*false", t) is not None,
          "one failed matrix leg must not cancel the other")
    check("lab-12", "matrix lists reviewer and auditor", "reviewer" in t and "auditor" in t)
    check("lab-12", "artifact upload with if-no-files-found error", "upload-artifact" in t and re.search(r"if-no-files-found:\s*error", t) is not None)
    check("lab-12", "consolidate needs agent-check", re.search(r"needs:\s*(\[\s*)?agent-check", t) is not None)
    check("lab-12", "download-artifact used", "download-artifact" in t)
    check("lab-12", "writes to GITHUB_STEP_SUMMARY", "GITHUB_STEP_SUMMARY" in t)
    check("lab-12", "bonus answered: queue max, never combined", "queue" in t.lower())


LABS = {"1": lab01, "2": lab02, "3": lab03, "4": lab04, "5": lab05,
        "6": lab06, "7": lab07, "8": lab08, "9": lab09, "10": lab10, "11": lab11, "12": lab12}


def main():
    picks = [a.lstrip("lab-0").lstrip("lab-") or a for a in sys.argv[1:]] or list(LABS)
    for k in picks:
        fn = LABS.get(str(int(k)) if str(k).isdigit() else k)
        if fn:
            try:
                fn()
            except FileNotFoundError as e:
                check(f"lab-{k}", "file present", False, str(e))
    width = max(len(n) for _, n, _, _ in results) if results else 0
    fails = 0
    cur = None
    for lab, name, ok, hint in results:
        if lab != cur:
            print(f"\n== {lab} ==")
            cur = lab
        mark = "PASS" if ok else "FAIL"
        fails += 0 if ok else 1
        line = f"  [{mark}] {name.ljust(width)}"
        if not ok and hint:
            line += f"   hint: {hint}"
        print(line)
    print(f"\n{len(results) - fails} passed, {fails} failed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
