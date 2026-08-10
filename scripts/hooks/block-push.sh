#!/usr/bin/env bash
# preToolUse command hook: blocks direct git push from any agent shell.
# Input arrives on stdin as JSON: {sessionId, timestamp, cwd, toolName, toolArgs}
# toolArgs is a JSON *string*; parse it before reading .command.
input=$(cat)
args=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.loads(d.get('toolArgs') or '{}').get('command',''))" 2>/dev/null)
if echo "$args" | grep -qE "git push"; then
  echo '{"permissionDecision":"deny","permissionDecisionReason":"Open a pull request instead of pushing directly."}'
else
  echo '{"permissionDecision":"allow"}'
fi
