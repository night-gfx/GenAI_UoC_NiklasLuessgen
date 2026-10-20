# Task 01: Collect and verify data

## GOAL

Verify the already downloaded Kenneth French daily datasets and create a
reproducible inventory for the January 1990 onward analysis. Preserve the
original files and their recorded retrieval date.

## FILES

- **Read-only:** `proposal.md`, `AGENTS.md`, this specification,
  `.agents/skills/research-task-workflow/SKILL.md`, `requirements.txt`,
  `data/README.md`, `data/12_Industry_Portfolios_Daily.csv`,
  `data/F-F_Research_Data_Factors_daily.csv`, `tests/researcher/`.
- **May create or modify:** `code/collect_data.py`,
  `data/source_inventory.json`,
  `tests/agent/test_collect_data.py`, `tests/agent/01_*`, `tasks/README.md`.
- **Expected branch:** `agent/01_collect_data`.

## CONSTRAINTS

- Expose calculation functions or destination arguments for isolated reruns
  under `tests/agent/05_reproduction/` in Task 05, without overwriting accepted
  artifacts; ordinary execution writes only the paths authorized here.
- Use the existing sources defined in `proposal.md`; do not download newer
  versions, replace originals, or substitute portfolios without approval.
- Use only value-weighted `Utils` and `BusEq`, plus daily `Mkt-RF` and `RF`.
  Distinguish the value-weighted block from other blocks in the industry file.
- Record the original download timestamp from `data/README.md` separately
  from the inventory creation timestamp; do not invent a download timezone.
- Do not choose a sample cutoff based on estimated outcomes. Task 02 determines
  the final common complete week after the weekly convention is approved.

## STEPS

1. **Inventory:** Implement a read-only inspection entry point in
   `code/collect_data.py`. Record source paths, documented URLs, original retrieval
   timestamp, SHA-256 hashes, source metadata, selected blocks and columns,
   return units, missing-value markers, date ranges and row counts.
   Check that both originals are readable and both hashes remain unchanged.
2. **Validate inputs:** Add tests for block selection, valid unique dates,
   numeric fields, units, source missing markers and overlapping coverage from
   January 1990. Report gaps and invalid observations without silent repair.
   Run the relevant tests; resolve parsing errors within scope.
3. **Freeze handoff:** Write `data/source_inventory.json`, including
   the latest common daily date, quality issues and unresolved weekly-convention
   decisions. Re-run the inventory and tests to verify deterministic source
   fields and unchanged raw hashes. Complete the final checks before review.

## CHECK

- Run `.venv/bin/python code/collect_data.py` after implementing the entry point.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/agent/test_collect_data.py`.
- Run relevant researcher tests, if any, with bytecode and pytest caches disabled.
- Verify required provenance fields, correct value-weighted selection, explicit
  missing-marker handling and a nonempty common daily sample beginning in 1990.
- Record commands, actual outcomes and original-file hash verification in
  `tests/agent/01_checks.txt` and `tasks/README.md`.

## OUTPUT

- Read-only inventory script, source inventory JSON, validation tests and check log.
- A documented input freeze for Task 02, with unresolved construction choices
  explicitly listed; no weekly sample date asserted before construction.
- One descriptive commit per verified step; final status `In Review`.

## STOP

- Stop on the wrong branch, incomplete predecessors or unrelated staged changes.
- Stop and ask if originals, provenance or required columns are missing or
  contradictory, or data-quality problems cannot be resolved within scope.
- Stop before downloading, editing raw files, changing sources or adding
  dependencies. Leave methodological decisions to the researcher.
