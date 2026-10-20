# The Changing Defensive Role of U.S. Utilities During the AI Boom

## 1. Research Question

Has the defensive role of U.S. utility stocks changed during the AI boom? Specifically, how do utilities' market beta and their market-adjusted correlation with technology stocks during the AI boom compare with the period since 1990 before it?

- **H1 (Defensive Utilities, Cyclical Technology):** Over the full sample, the market beta of U.S. utility stocks is below one and the market beta of technology stocks is above one.

  $$H_{1a}: \beta_U^{FS} < 1 \;\; \text{vs.} \;\; H_{0}: \beta_U^{FS} \geq 1, \qquad H_{1b}: \beta_T^{FS} > 1 \;\; \text{vs.} \;\; H_{0}: \beta_T^{FS} \leq 1$$

- **H2 (Higher Market Sensitivity of Utilities in the AI Boom):** The market beta of U.S. utility stocks is higher during the AI boom than before the AI boom.

  $$H_{2}: \beta_U^{AI} > \beta_U^{BAI} \;\; \text{vs.} \;\; H_{0}: \beta_U^{AI} \leq \beta_U^{BAI}$$

- **H3 (Stronger Utility–Technology Co-Movement in the AI Boom):** The market-adjusted correlation between U.S. utility and technology stock returns is higher during the AI boom than before the AI boom.

  $$H_{3}: \rho_{U,T\mid M}^{AI} > \rho_{U,T\mid M}^{BAI} \;\; \text{vs.} \;\; H_{0}: \rho_{U,T\mid M}^{AI} \leq \rho_{U,T\mid M}^{BAI}$$

Superscripts $FS$, $BAI$, and $AI$ denote the full sample, before the AI boom, and the AI boom (Section 2); $\beta$ and $\rho_{U,T\mid M}$ are defined in Section 3. All hypotheses are tested one-sided at the 10%, 5%, and 1% levels. The three hypotheses are fixed in advance and tested without a multiple-testing correction.

## 2. Data and Sample

### Data

The analysis uses data from the **Kenneth French Data Library**:

- **Utilities:** Value-weighted utilities portfolio (Utils) from the 12-industry portfolios.
- **Technology:** Value-weighted business equipment portfolio (BusEq) from the 12-industry portfolios.
- **Market:** Fama–French market factor (Mkt-RF) and risk-free rate (RF).

*Source: Baele and Londono (2013) (also use U.S. industry portfolios, with 30 industries rather than the 12 used here).*

### Sample

- **Period:** Monday, 1 January 1990 to Friday, 28 August 2026 (the sample starts on a Monday and ends on a Friday, so it contains only full Monday–Friday weeks).

- **Comparison periods:** Periods are fixed in advance to avoid cherry-picking.

| Comparison period | Start | End |
| --- | --- | --- |
| Full Sample | 1 January 1990 | 28 August 2026 |
| | | |
| Before AI boom | 1 January 1990 | November 2022 |
| AI boom | December 2022 | 28 August 2026 |
| | | |
| Pre-Dot-Com | 1 January 1990 | February 2000 |
| Dot-com Crash | March 2000 | October 2002 |
| Pre Financial Crisis | November 2002 | May 2007 |
| Financial Crisis | June 2007 | February 2009 |
| Pre-COVID | March 2009 | February 2020 |
| COVID | March 2020 | February 2022 |

*Source: Ramesh et al. (2025) (provide the dates for the dot-com crash, global financial crisis, and COVID-19 crisis).*

*Manual Adjustments: Everything before crisis is pre-period. Begin of AI-Boom was release of ChatGPT by OpenAI. Before AI boom pools all weeks before the AI boom as the comparison period for H2 and H3. Weeks from March to November 2022 belong to no crisis subperiod and enter only the Full Sample and Before AI boom. Weeks are assigned to periods by the calendar month of their Friday week end.*

## 3. Constructed Variables

- **Excess Return:** Weekly (more observations than monthly data, less short-term fluctuation than daily data) excess returns are sector or market total returns minus the risk-free return for the same week:

  $$R^e_{U,t} = R_{U,t} - R_{f,t}, \quad R^e_{T,t} = R_{T,t} - R_{f,t}, \quad R^e_{M,t} = R_{M,t} - R_{f,t}$$

  **Week Rule:** A week runs from Monday to Friday and is labeled by its Friday date (`week_end`), also when that Friday is a trading holiday; weekly returns compound all trading days of the week.

  $R$ denotes total return; superscript $e$ denotes excess return; subscripts $U$, $T$, $M$, and $f$ identify utilities (Utils), technology (BusEq), market, and the risk-free asset; $t$ denotes the week.

  **Interpretation:** Positive (negative) excess returns indicate performance above (below) the risk-free return; zero indicates equal performance.

*Sources: Black, Jensen and Scholes (1972), p. 2 (definition), p. 10 (monthly returns); Baele and Londono (2013), p. 35 (daily log returns).*

- **Market Beta:** Sensitivity of utilities and technology excess returns to market excess returns; technology beta serves as a benchmark for utilities beta (tested against one in H1b, otherwise descriptive):

  $$\beta_U = \frac{\operatorname{Cov}(R_U^e, R_M^e)}{\operatorname{Var}(R_M^e)}, \qquad \beta_T = \frac{\operatorname{Cov}(R_T^e, R_M^e)}{\operatorname{Var}(R_M^e)}$$

  $\beta$ denotes market beta; $\operatorname{Cov}$ denotes covariance and $\operatorname{Var}$ variance.

  **Interpretation:** For either sector, $0 \leq \beta < 1$ indicates lower market sensitivity, consistent with defensive characteristics; $\beta = 1$ indicates the same sensitivity as the market; $\beta > 1$ indicates greater sensitivity; $\beta < 0$ indicates an inverse linear association with the market. Comparing $\beta_U$ and $\beta_T$ shows their relative market sensitivities within the same period.

*Source: Black, Jensen and Scholes (1972), p. 2.*

- **Partial Correlation:** Correlation between utilities and technology excess returns after controlling for their common linear association with market excess returns:

  $$\rho_{U,T\mid M} = \operatorname{Corr}(\varepsilon_U,\varepsilon_T)$$

  $\rho$ denotes correlation; $\mid$ indicates conditioning on the variable to its right; $\operatorname{Corr}$ denotes Pearson correlation; $\varepsilon$ denotes the market-adjusted component of an excess return.

  **Interpretation:** Positive (negative) values indicate positive (negative) remaining linear co-movement; zero indicates no remaining linear correlation. This does not establish causality.

*Source: Gallup (2019), p. 602.*

## 4. Identification and Specification

### Identification

The study uses an empirical analysis to examine utilities’ market sensitivity and market-adjusted correlation with technology stocks. Market betas are tested against one (H1); the differences between the AI boom and before the AI boom are tested for utilities' market beta (H2) and the partial correlation (H3). All other period comparisons are descriptive. (Limitation: Descriptive differences across the remaining periods establish no statistical significance, and no comparison establishes causality. The comparison identifies changes during, not caused by, the AI boom; concurrent factors such as rising interest rates may contribute. Technology stocks are part of the market portfolio, and their market weight is high during the AI boom; a higher utilities beta and the market-adjusted correlation may therefore partly reflect the same co-movement with technology, and controlling for a technology-heavy market removes part of the technology return itself.)

### Specification

All estimates use the same aligned weekly observations within the full sample and each predefined comparison period.

- **Market Beta Estimation:** Estimate separate OLS regressions with intercepts for utilities and technology:

  $$R^e_{U,t} = \alpha_U + \beta_U R^e_{M,t} + \varepsilon_{U,t}, \qquad R^e_{T,t} = \alpha_T + \beta_T R^e_{M,t} + \varepsilon_{T,t}$$

  $\alpha$ denotes the intercept. OLS minimizes the sum of squared residuals separately for each sector; hats denote estimated quantities. The estimated slopes $\hat{\beta}_U$ and $\hat{\beta}_T$ are the period-specific market betas.

  **Interpretation:** Compare utilities’ market sensitivity across periods and with technology as a benchmark.

*Source: Black, Jensen and Scholes (1972), p. 7, Eq. (6), adapted to weekly sector excess returns.*

- **Robust Standard Errors:** All regression standard errors ($\operatorname{SE}$) are Newey–West standard errors with a lag length of four weeks; point estimates remain the OLS estimates.

  **Interpretation:** Unlike conventional OLS standard errors, they remain valid when return volatility changes over time or returns are serially correlated.

*Source: Newey and West (1987).*

- **Partial Correlation Estimation:** Calculate residuals from the two regressions above and then their Pearson correlation:

  $$\hat{\varepsilon}_{U,t} = R^e_{U,t} - \hat{\alpha}_U - \hat{\beta}_U R^e_{M,t}, \qquad \hat{\varepsilon}_{T,t} = R^e_{T,t} - \hat{\alpha}_T - \hat{\beta}_T R^e_{M,t}$$

  $$\hat{\rho}_{U,T\mid M} = \operatorname{Corr}(\hat{\varepsilon}_U,\hat{\varepsilon}_T)$$

  **Interpretation:** The estimate measures period-specific utilities–technology co-movement after removing their linear market association.

*Source: Gallup (2019), p. 602 (residual correlation), p. 606 (separate residual regressions), applied to sector excess returns with market excess returns and an intercept as controls.*

- **H1 Test (Beta Against One):** One-sided t-tests of the full-sample OLS betas against one:

  $$t_U = \frac{\hat{\beta}_U^{FS} - 1}{\operatorname{SE}(\hat{\beta}_U^{FS})}, \qquad t_T = \frac{\hat{\beta}_T^{FS} - 1}{\operatorname{SE}(\hat{\beta}_T^{FS})}$$

  $\operatorname{SE}$ denotes the Newey–West standard error; both statistics are asymptotically standard normal under $H_0$. $H_{1a}$ is supported for significantly negative $t_U$, $H_{1b}$ for significantly positive $t_T$.

  **Interpretation:** The regression table stars report the corresponding two-sided test (H0: β = 1) for every period; for an estimate in the hypothesized direction, the one-sided p-value equals half the two-sided p-value.

- **H2 Test (Beta Difference):** Estimate one pooled regression over the full sample with an AI-boom dummy $D_t$ ($D_t = 1$ from December 2022, otherwise $0$) interacted with the market excess return:

  $$R^e_{U,t} = \alpha_U + \delta_U D_t + \beta_U^{BAI} R^e_{M,t} + \gamma_U \left(D_t \cdot R^e_{M,t}\right) + \varepsilon_{U,t}, \qquad t_{\gamma} = \frac{\hat{\gamma}_U}{\operatorname{SE}(\hat{\gamma}_U)}$$

  $\delta_U$ allows a separate intercept and $\gamma_U = \beta_U^{AI} - \beta_U^{BAI}$ is the beta difference. $H_2$ is supported for a significantly positive $t_{\gamma}$ (one-sided, asymptotically standard normal).

  **Interpretation:** $\hat{\gamma}_U > 0$ indicates higher market sensitivity of utilities during the AI boom than before it.

- **H3 Test (Correlation Difference):** Compare the two partial correlations of the non-overlapping periods with a Fisher z-test:

  $$z_k = \tfrac{1}{2}\ln\frac{1 + \hat{\rho}^{k}_{U,T\mid M}}{1 - \hat{\rho}^{k}_{U,T\mid M}}, \qquad Z = \frac{z_{AI} - z_{BAI}}{\sqrt{\dfrac{1}{N_{AI} - 4} + \dfrac{1}{N_{BAI} - 4}}}, \qquad k \in \{AI, BAI\}$$

  $\ln$ denotes the natural logarithm; $N_k$ is the number of weekly observations in period $k$. The subtracted 4 accounts for the controlled market variable. $H_3$ is supported for a significantly positive $Z$ (one-sided, standard normal).

  **Interpretation:** $Z > 0$ indicates stronger market-adjusted utility–technology co-movement during the AI boom than before it. (Limitation: The test assumes independent, approximately normal observations; fat-tailed weekly returns may make it less accurate.)

*Sources: Fisher (1921), p. 7 (z-transformation), p. 14 (weight n − 3 for a simple correlation); Fisher (1924) (weight n − 3 − k for a partial correlation with k controls, here k = 1, giving n − 4).*

**Regression Table: Market Betas**

| Comparison period | Utilities Beta (SE) | Technology Beta (SE) | R² Utilities | R² Technology | N |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Sample | — | — | — | — | — |
| | | | | | |
| Before AI boom | — | — | — | — | — |
| AI boom | — | — | — | — | — |
| | | | | | |
| Pre-Dot-Com | — | — | — | — | — |
| Dot-com Crash | — | — | — | — | — |
| Pre Financial Crisis | — | — | — | — | — |
| Financial Crisis | — | — | — | — | — |
| Pre-COVID | — | — | — | — | — |
| COVID | — | — | — | — | — |

*Newey–West standard errors in parentheses; stars test H0: β = 1 (two-sided): \* p < 0.10, \*\* p < 0.05, \*\*\* p < 0.01.*

**Hypothesis Tests**

| Hypothesis | Estimate | Test Statistic | One-Sided p-Value | N |
| --- | ---: | ---: | ---: | ---: |
| H1a: $\beta_U^{FS} < 1$ | — | — | — | — |
| H1b: $\beta_T^{FS} > 1$ | — | — | — | — |
| H2: $\beta_U^{AI} > \beta_U^{BAI}$ | — | — | — | — |
| H3: $\rho_{U,T\mid M}^{AI} > \rho_{U,T\mid M}^{BAI}$ | — | — | — | — |

*Estimates: $\hat{\beta}$ for H1, $\hat{\gamma}_U$ for H2, $\hat{\rho}^{AI} - \hat{\rho}^{BAI}$ for H3. Test statistics: $t$ for H1 and H2, $Z$ for H3. N: Full Sample weeks for H1 and H2; $N_{BAI} + N_{AI}$ for H3.*

**Descriptive Statistics**

*Panel A: Correlations*

| Comparison period | Partial Correlation | Corr(U, T) | Corr(U, M) | Corr(T, M) | N |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Sample | — | — | — | — | — |
| | | | | | |
| Before AI boom | — | — | — | — | — |
| AI boom | — | — | — | — | — |
| | | | | | |
| Pre-Dot-Com | — | — | — | — | — |
| Dot-com Crash | — | — | — | — | — |
| Pre Financial Crisis | — | — | — | — | — |
| Financial Crisis | — | — | — | — | — |
| Pre-COVID | — | — | — | — | — |
| COVID | — | — | — | — | — |

*Panel B: Volatilities (standard deviation of weekly excess returns, %)*

| Comparison period | σ Utilities | σ Technology | σ Market |
| --- | ---: | ---: | ---: |
| Full Sample | — | — | — |
| | | | |
| Before AI boom | — | — | — |
| AI boom | — | — | — |
| | | | |
| Pre-Dot-Com | — | — | — |
| Dot-com Crash | — | — | — |
| Pre Financial Crisis | — | — | — |
| Financial Crisis | — | — | — |
| Pre-COVID | — | — | — |
| COVID | — | — | — |

## 5. Checks and Bounds (Fixed Now)

### Checks & Validation

- **Data Quality:** Verify valid returns, consistent units, no unexpected missing or duplicate observations, weekly alignment, and correct week-ending assignments to predefined, sourced periods.
- **Weekly Return Verification:** Verify correct daily-to-weekly compounding and excess returns using consistent weeks across all series.
- **Market Beta Validation:** Verify that both OLS betas match their covariance–variance formulas within numerical tolerance.
- **Partial Correlation Validation:** Verify residual orthogonality to market excess returns, agreement with the analytic partial-correlation formula, and correlations within [−1, 1], allowing for numerical tolerance.

### Bounds

- **Predefined Methodology:** Data sources, variables, weekly return construction, estimation methods, and comparison-period boundaries are fixed before estimating the results.
- **Fixed Sample Cutoff:** The sample ends on Friday, 28 August 2026. The data retrieval date and the final sample week must be recorded.
- **No Cherry-Picking:** Observations and period boundaries must not be selected, shifted, or excluded based on their effects on the estimated results. Data exclusions are permitted only for documented data-quality reasons.
- **Documentation:** All methodological changes and deviations from the original proposal must be documented and tracked in Git, including their justification.

## 6. AI Delegation and Research Responsibilities

| Research Step | AI Agent (Delegation) | Researcher (You) |
| --- | --- | --- |
| Research Design | Brainstorming & Suggestions | Final Decisions |
| Literature & Writing | Literature Search, Summaries & Drafting | Source Verification & Content Approval |
| Data Analysis & Results | Coding, Estimation & Tables | Task Specification, Code & Results Review |
| Validation | Automated Testing & Debugging | Independent Human Review |
| Documentation | Branch Commits, Code Documentation | Main Commits, Merge Approval |
| Interpretation | Interpretation Support | Scientific Judgment & Conclusions |