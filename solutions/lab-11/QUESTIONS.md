1. The cloud agent is non-interactive, so "ask" is treated like deny: there
   is no user present to answer, and failing closed on an unanswerable
   question is the safe behavior.

2. .github/hooks/*.json in the repository. The cloud agent only loads hooks
   from the cloned repository; it never loads user-level files from
   ~/.copilot/hooks/, local settings, or plugins, so a user-level hook
   exists only on that developer's machine.

3. Nothing runs: the cloud agent is Linux-only, so a powershell-only entry
   is ignored there. Portability requires a "bash" entry or the
   cross-platform "command" fallback.

4. Branch protection / rulesets requiring PR review (preventive) and
   required status checks such as CI and code scanning (preventive, with
   detective evidence in logs and scan results). Hooks intercept behavior
   but do not replace enforceable repository policy.
