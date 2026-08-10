# Lab 11 (D6): hooks

The provided script scripts/hooks/block-push.sh denies any shell command
containing "git push". Wire it up, then answer the concept questions; both
files are graded.

For block-push.json:
- Blank 1, the event name: which hook event fires BEFORE a tool executes and
  can allow, deny, ask, or modify? (Not permissionRequest: that one is
  CLI-only and never the cloud-agent answer.)
- Blank 2, the filter key: which field filters this hook to shell execution
  only? Note its regex is ANCHORED: "bash" matches exactly the tool named
  bash. Hook tool names are lower-level than agent tools: view/grep/glob map
  to read/search, edit/create map to edit, bash/powershell map to execute,
  task maps to agent.

Questions (replace each blank):

1. The script returns {"permissionDecision": "deny", ...} to block. In the
   interactive CLI a hook may also return "ask". What does the cloud agent
   do with "ask", and why?
   ____FILL_ME____

2. Where must this JSON file live for BOTH Copilot CLI and the cloud agent
   to load it? Name the path pattern, and explain why a hook defined only in
   ~/.copilot/hooks/ never affects the cloud agent.
   ____FILL_ME____

3. The cloud agent runs on Linux with working directory /workspace. A
   teammate ships this hook with only a "powershell" command entry. What
   happens on the cloud agent, and which one or two fields make a command
   hook portable there?
   ____FILL_ME____

4. Hook failures generally fail OPEN (empty output means default behavior
   continues). Name the two repository-level controls that must therefore
   still exist even with this hook in place, and the control type of each
   (preventive, detective, corrective).
   ____FILL_ME____
