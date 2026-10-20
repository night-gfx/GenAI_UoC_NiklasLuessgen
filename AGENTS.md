# Agent Rules

## Project

Study U.S. utilities' market beta and market-adjusted correlation with technology stocks since 1990.

## Conventions

### Paths

- **`README.md`:** Project overview, setup, and execution.
- **`proposal.md`:** Research question, data, methods, and validation.
- **`AGENTS.md`:** Persistent agent instructions.
- **`code/`:** Python analysis scripts.
- **`data/`:** Original and adjusted datasets.
- **`data/raw/`:** Read-only original datasets.
- **`data/adjusted/`:** Working copies and processed datasets; agent edits permitted within the task scope.
- **`tests/`:** Validation tests and saved test outputs.
- **`tests/researcher/`:** Researcher-maintained tests and their outputs; protected from agent edits.
- **`tests/agent/`:** Agent-written tests and their outputs.
- **`tasks/`:** Written agent task specifications.
- **`literature/`:** References and research notes.
- **`output/`:** Generated tables and figures.
- **`.gitignore`:** Files excluded from Git.
- **`.codex/`:** Project-specific Codex configuration.
- **`.venv/`:** Local Python virtual environment.

### Packages

- **Python:** Use Python for data processing and statistical analysis.
- **Dependencies:** Record dependencies in `requirements.txt`.

### Code Documentation

- **Code Changes:** Identify and explain code changes in the completion summary; add concise comments for non-obvious logic.

## Restrictions (Task Boundaries)

- **Authorization:** Create and modify files only in `code/`, `tests/agent/`, and `data/adjusted/` within the approved task scope; read and copy raw data into `data/adjusted/` for processing, and save agent test outputs in `tests/agent/`.
- **Protected Files:** All other files and directories are read-only unless the researcher explicitly authorizes changes, including `data/raw/`, `tests/researcher/`, all other contents of `data/` and `tests/`, `README.md`, `proposal.md`, `AGENTS.md`, `requirements.txt`, `tasks/`, `literature/`, `output/`, `.gitignore`, `.gitattributes`, `.codex/`, `.venv/`, `.git/`, and `.DS_Store`; Git metadata updates through the permitted Git workflow are allowed, but direct edits to `.git/` are prohibited; never modify, overwrite, delete, or move raw-data originals without explicit approval.
- **Git Workflow:** Work only on the feature branch prepared by the researcher and create descriptive commits for completed task steps; do not push or open pull requests without explicit approval, and leave all merges to the researcher.
- **Human Control:** The researcher independently reviews changes, reruns tests, and accepts or rejects the work; only the researcher approves and performs merges into `main` and decides whether to update GitHub.
- **Methodology:** Follow the predefined research design. Obtain approval before changing data sources, variables, sample periods, or estimation methods.
- **Validation:** Fix implementation errors within the approved task scope and rerun relevant tests. Never weaken existing tests merely to make them pass.
- **Stop Conditions:** Stop and ask if requirements are unclear, protected files must change, or validation failures cannot be resolved within the approved scope.
- **Security:** Never commit credentials or sensitive data.

## Completion

- **Tests:** Run relevant researcher-maintained and agent-written tests without modifying researcher-maintained tests.
- **Test Results:** Record actual test results and report failures or unresolved issues. Save test outputs only in approved locations.
- **Summary:** Summarize code changes, validation results, remaining issues, and items requiring human verification.
- **Review Handoff:** Commit only approved task changes on the prepared feature branch, report the commit hashes, and leave the branch for researcher review without pushing or merging.

## Research Task Workflow

The following rules refine the task-boundary and completion rules above for the numbered research tasks. Explicit researcher authorization remains necessary for any other protected-file change.

- **Skill:** Read and follow `.agents/skills/research-task-workflow/SKILL.md` when executing or resuming a numbered research task. The skill defines the execution procedure; `proposal.md` defines the research design; each task specification defines its permitted files and checks.
- **Authorization:** Modify only paths authorized by the current task specification, within `code/`, `tests/agent/` and `data/adjusted/`. Read raw originals without modifying them. The agent may additionally update `tasks/README.md` solely to track task status, progress, check results and blockers; this is an explicit exception to the protection of `tasks/` above. All other task specifications and skill files remain read-only unless the researcher explicitly authorizes changes.
- **Branches:** Execute each task only on the researcher-prepared branch `agent/<task-filename-without-extension>`; for example, `tasks/02_prepare_returns.md` requires `agent/02_prepare_returns`. Never execute a numbered task on `main`, detached HEAD or another branch. Stop and ask the researcher to prepare or switch branches on a mismatch.
- **Sequence:** Select the single `In Progress` task, otherwise the first `Planned` task in `tasks/README.md`. Require all predecessors to be `Completed`. Stop when a task awaits review; do not automatically execute the next task.
- **Step Commits:** Follow the task's `STEPS` in order. Run the relevant checks, fix in-scope errors, record actual results and progress in `tasks/README.md`, and create one descriptive commit per verified step. Stage only task changes; preserve unrelated researcher edits. Do not advance after unresolved failures.
- **Review Status:** Use `Planned`, `In Progress`, `In Review` and `Completed`. `In Review` means **Ready for Review** and may be set by the agent only after successful final checks. Include this status update and final check evidence in the final step's commit. Only the researcher may set `Completed` after independent review.
- **Human Control:** Stop for researcher review after each task. Do not push or open pull requests without explicit approval; leave all merges to the researcher. Report commit hashes, actual test outcomes, remaining issues and items requiring human verification.
