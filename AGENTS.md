# Agent Rules

## Project
Research changes in U.S. utilities' market beta and market-adjusted correlation with technology stocks since 1990.
Follow `proposal.md` for data, methods, and checks.
Use Python for analysis and Streamlit for the dashboard.

## Conventions
- Python code: `code/`; tests: `tests/`; task specifications: `tasks/`; generated results: `output/`.
- After substantial tasks, save `logs/YYYY-MM-DD-task.md`: task, changed files, test commands and actual output, issues, dependency versions (if relevant), and `Human review: pending`.
- Never commit secrets or sensitive data.

## Restrictions
- Work on a separate branch; follow the permitted scope in `tasks/`. Do not commit directly to `main`.
- Ask before changing `proposal.md`, `data/`, `tests/`, or research methods.
- Fix and document period-selection rules before estimating risk metrics. Stop if decisions are unclear or tests fail.

## Completion
- Run relevant tests and report their actual results; do not claim success without output.
- Summarize changes, unresolved issues, and checks requiring independent human review.
