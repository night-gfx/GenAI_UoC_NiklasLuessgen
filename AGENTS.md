# Agent Rules

## Project

Study U.S. utilities' market beta and market-adjusted correlation with technology stocks since 1990.

## Conventions

### Paths

- **`README.md`:** Project overview, setup, and execution.
- **`proposal.md`:** Research question, data, methods, and validation.
- **`AGENTS.md`:** Persistent agent instructions.
- **`code/`:** Python analysis scripts.
- **`data/`:** Original datasets.
- **`tasks/`:** Written agent task specifications.
- **`literature/`:** References and research notes.
- **`output/`:** Generated tables and figures.
- **`.gitignore`:** Files excluded from Git.
- **`.codex/`:** Project-specific Codex configuration.
- **`.venv/`:** Local Python virtual environment.
- **`logs/`:** Execution logs for individual research tasks.
- **`.agents/skills/`:** Reusable Codex workflow skills.


### Packages

- **Python:** Use Python for data processing and statistical analysis.
- **Dependencies:** Record dependencies in `requirements.txt`.

### Code Documentation

- **Code Changes:** Identify and explain code changes in the completion summary; add concise comments for non-obvious logic.
- **Git Commits:** Set Codex as the author of agent-created commits: `Codex <codex@openai.com>`.

## Restrictions (Task Boundaries)


- **Authorization:** Create and modify files only in
  `code/`,
  `tasks/README.md`, and the current task's log in `logs/`,
  within the approved task scope. Additional paths
  require explicit researcher authorization.
- **Protected Files:** All other files and directories are read-only unless the researcher explicitly authorizes changes, including `data/`, `README.md`, `proposal.md`, `AGENTS.md`, `requirements.txt`, `tasks/`, `literature/`, `output/`, `.gitignore`, `.gitattributes`, `.codex/`, `.venv/`, `.git/`, and `.DS_Store`; Git metadata updates through the permitted Git workflow are allowed, but direct edits to `.git/` are prohibited; never modify, overwrite, delete, or move raw-data originals without explicit approval.
- **Git Workflow:** Work only on the feature branch prepared by the researcher and create descriptive commits for completed task steps; do not push or open pull requests without explicit approval, and leave all merges to the researcher.
- **Human Control:** The researcher independently reviews changes, reruns checks, and accepts or rejects the work; only the researcher approves and performs merges into `main` and decides whether to update GitHub.
- **Methodology:** Follow the predefined research design. Obtain approval before changing data sources, variables, sample periods, or estimation methods.
- **Validation:** Fix implementation errors within the approved task scope and rerun the task's CHECK criteria. Never weaken CHECK criteria merely to make them pass.
- **Stop Conditions:** Stop and ask if requirements are unclear, protected files must change, or validation failures cannot be resolved within the approved scope.
- **Security:** Never commit credentials or sensitive data.

## Completion

- **Checks:** Run all CHECK criteria of the task.
- **Check Results:** Record actual check results in the task log and report failures or unresolved issues.
- **Summary:** Summarize code changes, validation results, remaining issues, and items requiring human verification.
- **Review Handoff:** Commit only approved task changes on the prepared feature branch, report the commit hashes, and leave the branch for researcher review without pushing or merging.