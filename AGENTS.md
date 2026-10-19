# Agent Rules

- Follow `proposal.md`. Use Python in `code/` for analysis and Streamlit for the dashboard.
- Never modify `proposal.md`, raw data, or research decisions without approval. Fix and document period-selection rules **before** estimating risk metrics.
- Work on a separate Git branch; follow task-specific scope and approval limits in `tasks/`.
- Add and run relevant tests in `tests/`. Report failures; passing agent-written tests do not replace independent human review.
- After each substantial task, write a brief `logs/YYYY-MM-DD-task.md` with task, changed files, tests/results, issues, and `Human review: pending`. Record dependency versions when relevant.
- Keep generated tables and figures in `output/`; never commit credentials or sensitive data.
- Stop and ask when requirements are unclear, checks fail, or protected changes are needed.
