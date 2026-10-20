# Task 02: Prepare weekly excess returns

## GOAL

Construct reproducible, aligned weekly utilities, technology and market excess
returns from the verified daily inputs, using the fixed research sample.

## FILES

- **Read-only:** `proposal.md`, `AGENTS.md`, this specification,
  `.agents/skills/research-task-workflow/SKILL.md`, `requirements.txt`,
  `code/collect_data.py`, `data/raw/`, `data/adjusted/source_inventory.json`,
  `tests/researcher/`.
- **May create or modify:** `code/prepare_returns.py`,
  `data/adjusted/daily_returns.csv`, `data/adjusted/weekly_returns.csv`,
  `data/adjusted/sample_metadata.json`, `tests/agent/test_prepare_returns.py`,
  `tests/agent/02_*`, `tasks/README.md`.
- **Expected branch:** `agent/02_prepare_returns`.

## CONSTRAINTS

- Expose calculation functions or destination arguments for isolated reruns
  under `tests/agent/05_reproduction/` in Task 05, without overwriting accepted
  artifacts; ordinary execution writes only the paths authorized here.
- Task 01 must be `Completed`. Use its frozen input hashes; do not refresh data.
- Follow `proposal.md`. It does not explicitly fix a weekday anchor or the
  treatment of partial boundary weeks: obtain researcher confirmation of these
  choices before construction and record it in the progress log and metadata.
- Convert source percentage returns to decimal simple returns exactly once;
  treat documented sentinels as missing before conversion or compounding.
- Use one common daily calendar for all required series. Do not forward-fill,
  interpolate, fill missing returns with zero or silently drop mismatches.
- Compound daily total sector returns and RF separately. Reconstruct daily
  market total return as `Mkt-RF + RF` before weekly compounding:
  `R_X,w = product_d(1 + R_X,d) - 1`, for `X = U, T, M, f`.
  Then compute `R_X,w^e = R_X,w - R_f,w` for `X = U, T, M`.
  Do not compound daily excess returns as if they were total returns.
- Start in January 1990 and end at the latest common complete week in the
  frozen inputs under the approved convention; retain legitimate holiday weeks.

## STEPS

1. **Confirm calendar and parse:** Record researcher approval of weekly labels,
   holiday handling and boundary-week rules. Implement parsing and daily
   alignment; produce `daily_returns.csv` and a missingness/alignment audit.
   Test block selection, percentage conversion, sentinels and duplicate dates.
2. **Construct weekly returns:** Implement the approved aggregation and create
   `weekly_returns.csv` with unique `week_end`, `utilities_excess`,
   `technology_excess` and `market_excess` columns, all in decimal units.
   Test by hand on a small daily example, including market reconstruction,
   RF subtraction, a holiday week and an incomplete boundary week.
3. **Assign periods and freeze sample:** Record the first/final included week,
   retrieval provenance, input hashes, units, calendar convention, exclusions
   and period definitions in `sample_metadata.json`. Assign observations by
   their approved week-ending labels to the exact proposal boundaries. Verify
   the eight disjoint subperiods partition the full weekly sample.
4. **Validate handoff:** Run all task checks and relevant researcher tests.
   Confirm re-runs reproduce the same returns, cutoff and period membership.
   Record results and prepare the task for review.

## CHECK

- Run `.venv/bin/python code/prepare_returns.py` after implementation.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/agent/test_prepare_returns.py`.
- Verify finite aligned values, unique sorted weekly labels, identical
  observations across all three excess-return series and no unexplained gaps.
- Independently verify compounding and excess-return arithmetic on the small
  fixture; verify every proposal period boundary, including December 2022.
- Recheck frozen raw hashes and run relevant researcher tests without caches.
- Save actual commands, decisions and outcomes in `tests/agent/02_checks.txt`
  and `tasks/README.md`.

## OUTPUT

- Parsing/aggregation script, daily and weekly decimal-return datasets, sample
  metadata, tests and recorded check results.
- One reproducible weekly sample and period mapping for Tasks 03–05.
- One descriptive commit per verified step; final status `In Review`.

## STOP

- Stop on a branch mismatch or before Task 01 is `Completed`.
- Ask before selecting an unapproved weekly convention, changing boundaries,
  replacing sources or excluding observations without documented quality reasons.
- Stop on unresolved calendar discrepancies, hash changes, invalid returns,
  insufficient common coverage or validation failures outside the allowed scope.
