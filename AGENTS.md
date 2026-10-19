# Agent Rules

## Project
Study U.S. utilities' market beta and market-adjusted correlation with technology stocks since 1990.
## Conventions

### Paths
- `README.md`: Project overview, setup, and execution.
- `proposal.md`: Research question, data, methods, and validation.
- `AGENTS.md`: Persistent agent instructions.
- `code/`: Python analysis scripts.
- `data/`: Original datasets.
- `tests/`: Automated validation tests.
- `tasks/`: Written agent task specifications.
- `logs/`: Optional supplementary logs.
- `literature/`: References and research notes.
- `paper/`: Research drafts and interpretation.
- `output/`: Generated tables and figures.
- `.gitignore`: Files excluded from Git.

### Packages
- Use Python for data processing and statistical analysis.
- Use Streamlit for interactive visualization.
- Record dependencies in `requirements.txt`.

### Logging
- Document code changes through descriptive Git commits and pull requests.
- Report executed tests, failures, and unresolved issues upon task completion.

## Restrictions
- Follow the permitted scope of the current task, whether in `tasks/` or directly specified by the user.
- Work on a separate Git branch; do not commit directly to `main`.
- Ask before modifying `proposal.md`, raw data, tests, or research methods.
- - Never commit credentials or sensitive data; stop and ask when requirements are unclear or validation fails.

## Completion
- Run relevant tests and report actual results; agent-written tests do not replace independent human review.
- Summarize changes, remaining issues, and items requiring human verification.
