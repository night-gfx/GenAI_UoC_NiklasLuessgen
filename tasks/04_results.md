# Task 04: Generate comparison results and final checks

## GOAL

Generate the proposal's nine-row comparison table and a reproducibility handoff,
with utilities beta, technology beta and market-adjusted correlation for each
period. Verify the complete pipeline before researcher review.

## FILES

- **Read-only:** `proposal.md`, `AGENTS.md`, this specification,
  `.agents/skills/research-task-workflow/SKILL.md`, `requirements.txt`,
  `data/12_Industry_Portfolios_Daily.csv`,
  `data/F-F_Research_Data_Factors_daily.csv`, `data/README.md`, `code/prepare_returns.py`,
  `code/estimate_beta.py`, `code/partial_correlation.py`,
  `data/source_inventory.json`, `data/sample_metadata.json`,
  `data/weekly_returns.csv`, `data/beta_estimates.csv`,
  `data/market_residuals.csv`,
  `data/partial_correlations.csv`, `tests/researcher/`.
- **May create or modify:** `code/results.py`,
  `output/comparison_table.csv`,
  `output/comparison_table.md`,
  `output/reproducibility.json`,
  `tests/agent/test_results.py`, `tests/agent/04_*`, `tasks/README.md`.
- **Expected branch:** `agent/04_results`.

## CONSTRAINTS

- Tasks 01–03 must be `Completed`. Preserve their accepted inputs and outputs.
- Use the exact period boundaries and row order from `proposal.md`: Full Sample,
  Pre-Dot-Com, Dot-com Crash, Pre Financial Crisis, Financial Crisis, Pre-COVID,
  COVID, Pre-AI boom and AI boom. Normalize only the proposal's inconsistent
  `Covid`/`COVID` spelling, not its dates.
- Keep full precision in the numeric CSV. Round only the Markdown presentation
  and state its display precision. Join by period with one-to-one validation.
- Keep the core table columns `Comparison period`, `Utilities Beta`,
  `Technology Beta` and `Partial Correlation`. Put observation counts and sample
  dates in reproducibility metadata or accompanying table notes.
- Save final script results directly in `output/`, without subdirectories.
  This folder is ignored by Git; do not stage or force-add its contents.
  This destination is explicitly researcher-authorized.
- Do not edit the proposal or introduce statistical
  significance or causal conclusions. Report descriptive differences only.

## STEPS

1. **Build comparison table:** Implement `code/results.py` to validate and join
   the accepted estimates, generate the numeric CSV and readable Markdown table,
   and test row order, exact values, formatting and rejection of missing or
   duplicate period rows.
2. **Prepare reproducibility record:** Write input/artifact hashes, original
   retrieval date, fixed sample cutoff, approved weekly rules, periods, counts,
   package versions, execution commands and limitations to
   `output/reproducibility.json`. Obtain Git revision information from Git; distinguish
   the input revision from the final handoff commit reported after committing.
3. **Run final checks:** Re-run all agent tests and relevant researcher tests.
   Reproduce calculations from the frozen raw inputs using isolated directories
   under `tests/agent/04_reproduction/`; require script functions or destination
   arguments so this does not overwrite accepted upstream artifacts. Compare
   recreated returns, coefficients, residuals and correlations with the accepted
   artifacts within declared tolerances. Recheck raw hashes. Record results,
   handoff notes and `In Review` in the final step's commit.

## CHECK

- Run `.venv/bin/python code/results.py` after implementation.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/agent/`.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/researcher/`
  if researcher tests exist; otherwise explicitly report their absence.
- Verify all nine rows and all three metrics against upstream files, metadata
  consistency, fixed cutoff, unchanged originals and reproducibility results.
- Save exact commands, environment information, pass/fail/skip counts and any
  unresolved limitations in `tests/agent/04_checks.txt` and `tasks/README.md`.

## OUTPUT

- Results script, full-precision CSV, formatted comparison table, reproducibility
  record, validation tests and final check log in the authorized paths above.
- Final handoff with changes, per-step commit hashes, actual test results,
  remaining issues and items for independent human verification.
- One descriptive commit per verified step; final status `In Review`.

## STOP

- Stop on branch mismatch, incomplete predecessors, any unresolved validation
  failure, changed raw hashes or nonreproducible accepted results.
- Ask before modifying accepted upstream scripts/artifacts: record the needed
  correction for researcher-directed reopening rather than silently fixing it
  outside this task's file scope.
- Ask before changing dependencies or methodology.
- Stop for researcher review after the final commit; do not mark `Completed`,
  push, open a pull request or merge.
