# Task 03: Estimate market betas

## GOAL

Estimate utilities and technology market betas for the full sample and all eight
predefined comparison periods, using the same aligned weekly observations.

## FILES

- **Read-only:** `proposal.md`, `AGENTS.md`, this specification,
  `.agents/skills/research-task-workflow/SKILL.md`, `requirements.txt`,
  `data/adjusted/weekly_returns.csv`, `data/adjusted/sample_metadata.json`,
  `tests/researcher/`.
- **May create or modify:** `code/estimate_beta.py`,
  `data/adjusted/beta_estimates.csv`, `data/adjusted/market_residuals.csv`,
  `tests/agent/test_estimate_beta.py`, `tests/agent/03_*`, `tasks/README.md`.
- **Expected branch:** `agent/03_estimate_beta`.

## CONSTRAINTS

- Expose calculation functions or destination arguments for isolated reruns
  under `tests/agent/05_reproduction/` in Task 05, without overwriting accepted
  artifacts; ordinary execution writes only the paths authorized here.
- Tasks 01–02 must be `Completed`. Preserve the frozen sample and period mapping.
- Estimate separate OLS models with intercepts in every period:
  `utilities_excess = alpha_U + beta_U * market_excess + epsilon_U` and
  `technology_excess = alpha_T + beta_T * market_excess + epsilon_T`.
- Use the complete common sample within each period for both sectors. Refit for
  each period; do not reuse full-sample coefficients for subperiod residuals.
- Technology beta is a descriptive benchmark. Do not introduce factors, rolling
  windows, significance claims, causal claims or different estimators.
- Do not round intermediate results or silently drop observations. Declare
  numerical check tolerances before checking outcomes.

## STEPS

1. **Implement period OLS:** Create `code/estimate_beta.py` using the approved
   weekly input. Emit full-precision estimates with `period`, `n_obs`,
   `first_week`, `last_week`, `alpha_U`, `beta_U`, `alpha_T` and `beta_T`.
   Test known slopes/intercepts on synthetic aligned returns.
2. **Persist residuals and verify formulas:** Save residuals keyed by
   `(period, week_end)` with `utilities_residual`, `technology_residual` and
   `market_excess`. Include separate full-sample and subperiod fits. Verify
   each OLS slope against `Cov(sector_excess, market_excess) / Var(market_excess)`
   using consistent covariance/variance normalization and stated tolerances.
3. **Validate handoff:** Check exact period coverage, matching row counts,
   residual reconstruction and residual orthogonality to the intercept and
   market regressor. Run final task checks and relevant researcher tests.

## CHECK

- Run `.venv/bin/python code/estimate_beta.py` after implementation.
- Run `.venv/bin/python -B -m pytest -p no:cacheprovider tests/agent/test_estimate_beta.py`.
- Verify all nine period rows, finite estimates, nonzero market variance,
  full-rank regressions and adequate observations for residual correlation.
- Verify both slope identities in every period, residual means near zero and
  residual dot products with market excess returns near zero, within declared
  scale-aware numerical tolerances.
- Run relevant researcher tests without caches; record commands and actual
  outcomes in `tests/agent/03_checks.txt` and `tasks/README.md`.

## OUTPUT

- OLS estimation script, period-specific coefficients and keyed residuals,
  validation tests and check log, preserving unrounded numeric results.
- One descriptive commit per verified step; final status `In Review`.

## STOP

- Stop on branch mismatch, incomplete predecessors, undefined market variance,
  insufficient observations, singular designs or nonfinite estimates.
- Stop if covariance identities or residual checks fail after in-scope fixes.
- Ask before changing the sample, variables, periods, estimator or dependencies.
