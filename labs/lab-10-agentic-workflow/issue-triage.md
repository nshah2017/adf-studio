---
on:
  issues:
    # TODO(gh-aw): trigger on newly opened issues only.
    types: ____FILL_ME____
# TODO(D6): the security posture that makes agentic workflows safe by
# default: what permissions value grants read across the repo and nothing
# else?
permissions: ____FILL_ME____
# TODO(D6): the ONLY write this automation may perform is posting a comment,
# and only through the sanitized channel. Declare it.
safe-outputs:
  ____FILL_ME____
---

# Issue triage agent

Read the newly opened issue.

If it was NOT created with the "Agent task" template (it is missing a Goal,
Inputs and scope, or Success criteria section), post one polite comment that:
lists exactly which of the three sections are missing, links to the Agent
task template, and explains that agent work in this repository starts from
defined inputs, outputs, and success criteria.

If the issue does contain all three sections, post a one-line comment
confirming it is ready for planning and suggest adding the "needs-plan" label.

<!-- TODO(D6): add the final constraint sentence: bound how many comments it
     may post, and forbid it from modifying the issue. Instructions are part
     of the guardrail surface in natural-language automation. -->
____FILL_ME____
