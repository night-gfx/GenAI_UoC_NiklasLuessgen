---
name: log-agent-work
description: On explicit invocation, record the current Codex task, changes, checks, and review status in a short project log.
---

# Log Agent Work

1. Review the current task and its actual file changes (`git diff`); do not invent results.
2. Run relevant existing tests when feasible. Record commands, results, and failures; otherwise say "Not run".
3. Create `logs/YYYY-MM-DD-short-task.md` with: **Task**, **Files changed**, **Tests/results**, **Issues**, **Human review: pending**.
4. Keep the log concise. Never include secrets or sensitive data. Do not change research methods or protected files.
5. Report the log path. Do not claim independent validation or approval.
