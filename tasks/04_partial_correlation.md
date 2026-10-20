# Task 04: Calculate market-adjusted correlations

## GOAL

Calculate the utilities–technology partial correlation controlling for market
excess returns, separately for the full sample and every comparison period.

## FILES

- **Read-only:** `proposal.md`, `AGENTS.md`, this specification,
  `.agents/skills/research-task-workflow/SKILL.md`, `requirements.txt`,
  `data/weekly_returns.csv`, `data/sample_metadata.json`,
  `data/beta_estimates.csv`, `data/market_residuals.csv`,
  `tests/researcher/`.
- **May create or modify:** `code/partial_correlation.py`,
  `data/partial_correlations.csv`,
  `tests/agent/test_partial_correlation.py`, `tests/agent/04_*`, `tasks/README.md`.
- **Expected branch:** `agent/04_partial_correlation`.

## CONSTRAINTS

- Expose calculation functions or destination arguments for isolated reruns
  under `tests/agent/05_reproduction/` in Task 05, without overwriting accepted
  artifacts; ordinary execution writes only the paths authorized here.
- Tasks 01–03 must be `Completed`. Use Task 03's period-specific residuals
  without changing the regressions, sample or week assignments.
- Calculate Pearson `Corr(utilities_residual, technology_residual)` on identical
  `(period, week_end)` pairs. Never combine residuals from different fits.
- Independently verify with the analytic identity:
  `rho_UT.M = (r_UT - r_UM * r_TM) / sqrt((1 - r_UM^2) * (1 - r_TM^2))`,
  where the `r` values are Pearson correlations of the original excess returns
  on that same period sample and `M` denotes market excess returns.
- Use unrounded data and declared numerical tolerances. Never force an invalid
  result into range by clipping it. The analysis is descriptive, not causal.

## STEPS

1. **Calculate residual correlations:** Implement the script and save `period`,
   `n_obs`, `first_week`, `last_week` and `partial_correlation` for all nine
   periods. Test with synthetic data with known remaining co-movement and
   ensure joins reject duplicate or unmatched residual keys.
2. **Cross-check independently:** Reconstruct period samples from weekly returns
   and sample metadata, calculate the three pairwise correlations and verify
   the analytic identity independently of the saved residuals. Test that zero
   residual variance and degenerate denominators produce explicit failures.
3. **Validate handoff:** Verify finite correlations within `[-1, 1]` up to the
   stated numerical tolerance, exact sample agreement with Task 03 and residual
   orthogonality to the market. Run final checks and relevant researcher tests.

## CHECK

- Run `.venv/bin/python code/partial_correlation.py` after implementation.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/agent/test_partial_correlation.py`.
- Check one row per proposal period, identical observations to the beta fits,
  nonzero residual variance and a nondegenerate analytic denominator.
- Check agreement of residual correlation and the analytic expression for
  every period; a plausible range alone is insufficient validation.
- Run relevant researcher tests without caches. Record actual commands,
  tolerances and outcomes in `tests/agent/04_checks.txt` and `tasks/README.md`.

## OUTPUT

- Partial-correlation script, unrounded period estimates, independent validation
  tests and recorded check results.
- One descriptive commit per verified step; final status `In Review`.

## STOP

- Stop on branch mismatch or incomplete predecessors.
- Stop on inconsistent samples, zero residual variance, undefined analytic
  correlation, unexplained range violations or unresolved identity failures.
- Ask before changing regressions, periods, data exclusions or tolerances merely
  to make a failing check pass.
