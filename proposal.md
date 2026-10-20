# The Changing Defensive Role of U.S. Utilities During the AI Boom

## 1. Research Question

How has the defensive behavior of U.S. utility stocks, measured by market beta, evolved since 1990, and how has their partial correlation with technology stocks changed, particularly during the AI boom?

- **H1 – Market Beta:** U.S. utility stocks have become more sensitive to overall market movements during the AI boom.
- **H2 – Partial Correlation:** The market-adjusted correlation between U.S. utility and technology stock returns has increased during the AI boom.

Both hypotheses are assessed by descriptively comparing the AI boom estimates with those of all preceding periods; changes across periods are not tested statistically.

## 2. Data and Sample

### Data

The analysis uses data from the **Kenneth French Data Library**:

- **Utilities:** Value-weighted utilities portfolio (Utils) from the 12-industry portfolios.
- **Technology:** Value-weighted business equipment portfolio (BusEq) from the 12-industry portfolios.
- **Market:** Fama–French market factor (Mkt-RF) and risk-free rate (RF).

*Source: Baele and Londono (2013) (also use U.S. industry portfolios, with 30 industries rather than the 12 used here).*

### Sample

- **Period:** January 1990 to the latest available date.

*Source: Baele and Londono (2013) (also use U.S. industry portfolios, with 30 industries rather than the 12 used here).*

- **Comparison periods:** Periods are fixed in advance to avoid cherry-picking.

| Comparison period | Start | End |
| --- | --- | --- |
| Full Sample | January 1990 | Latest available date |
| Pre-Dot-Com | January 1990 | February 2000 |
| Dot-com Crash | March 2000 | October 2002 |
| Pre Financial Crisis | November 2002 | May 2007 |
| Financial Crisis | June 2007 | February 2009 |
| Pre-COVID | March 2009 | February 2020 |
| Covid | March 2020 | February 2022 |
| Pre-AI boom | March 2022 | November 2022 |
| AI boom | December 2022 | Latest available date |

*Source: Ramesh et al. (2025) (provide the dates for the dot-com crash, global financial crisis, and COVID-19 crisis).*

*Manual Adjustments: Everything before crisis is pre-period. Begin of AI-Boom was release of ChatGPT by OpenAI.*

## 3. Constructed Variables

- **Excess Return:** Weekly (more observations than monthly data, less short-term fluctuation than daily data) excess returns are sector or market total returns minus the risk-free return for the same week:

  $$R^e_{U,t} = R_{U,t} - R_{f,t}, \quad R^e_{T,t} = R_{T,t} - R_{f,t}, \quad R^e_{M,t} = R_{M,t} - R_{f,t}$$

  $R$ denotes total return; superscript $e$ denotes excess return; subscripts $U$, $T$, $M$, and $f$ identify utilities (Utils), technology (BusEq), market, and the risk-free asset; $t$ denotes the week.

  **Interpretation:** Positive (negative) excess returns indicate performance above (below) the risk-free return; zero indicates equal performance.

*Sources: Black, Jensen and Scholes (1972), p. 2 (definition), p. 10 (monthly returns); Baele and Londono (2013), p. 35 (daily log returns).*

- **Market Beta:** Sensitivity of utilities and technology excess returns to market excess returns; technology beta serves as a descriptive benchmark for utilities beta:

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

The study uses an empirical analysis to examine utilities’ market sensitivity and market-adjusted correlation with technology stocks. Market betas are tested for a statistically significant difference from one (H0: β = 1); partial correlations are reported descriptively. Differences across periods are compared descriptively. (Limitation: Descriptive differences across periods establish neither statistical significance nor causality.)

### Specification

All estimates use the same aligned weekly observations within the full sample and each predefined comparison period.

- **Market Beta Estimation:** Estimate separate OLS regressions with intercepts for utilities and technology:

  $$R^e_{U,t} = \alpha_U + \beta_U R^e_{M,t} + \varepsilon_{U,t}, \qquad R^e_{T,t} = \alpha_T + \beta_T R^e_{M,t} + \varepsilon_{T,t}$$

  $\alpha$ denotes the intercept. OLS minimizes the sum of squared residuals separately for each sector; hats denote estimated quantities. The estimated slopes $\hat{\beta}_U$ and $\hat{\beta}_T$ are the period-specific market betas.

  **Interpretation:** Compare utilities’ market sensitivity across periods and with technology as a descriptive benchmark.

*Source: Black, Jensen and Scholes (1972), p. 7, Eq. (6), adapted to weekly sector excess returns.*

- **Partial Correlation Estimation:** Calculate residuals from the two regressions above and then their Pearson correlation:

  $$\hat{\varepsilon}_{U,t} = R^e_{U,t} - \hat{\alpha}_U - \hat{\beta}_U R^e_{M,t}, \qquad \hat{\varepsilon}_{T,t} = R^e_{T,t} - \hat{\alpha}_T - \hat{\beta}_T R^e_{M,t}$$

  $$\hat{\rho}_{U,T\mid M} = \operatorname{Corr}(\hat{\varepsilon}_U,\hat{\varepsilon}_T)$$

  **Interpretation:** The estimate measures period-specific utilities–technology co-movement after removing their linear market association.

*Source: Gallup (2019), p. 602 (residual correlation), p. 606 (separate residual regressions), applied to sector excess returns with market excess returns and an intercept as controls.*

**Regression Table: Market Betas**

| Comparison period | Utilities Beta (SE) | Technology Beta (SE) | R² Utilities | R² Technology | N |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Sample | — | — | — | — | — |
| Pre-Dot-Com | — | — | — | — | — |
| Dot-com Crash | — | — | — | — | — |
| Pre Financial Crisis | — | — | — | — | — |
| Financial Crisis | — | — | — | — | — |
| Pre-COVID | — | — | — | — | — |
| COVID | — | — | — | — | — |
| Pre-AI boom | — | — | — | — | — |
| AI boom | — | — | — | — | — |

*Standard errors in parentheses; stars test H0: β = 1 (two-sided): \* p < 0.10, \*\* p < 0.05, \*\*\* p < 0.01.*

**Descriptive Statistics**

*Panel A: Correlations*

| Comparison period | Partial Correlation | Corr(U, T) | Corr(U, M) | Corr(T, M) | N |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Sample | — | — | — | — | — |
| Pre-Dot-Com | — | — | — | — | — |
| Dot-com Crash | — | — | — | — | — |
| Pre Financial Crisis | — | — | — | — | — |
| Financial Crisis | — | — | — | — | — |
| Pre-COVID | — | — | — | — | — |
| COVID | — | — | — | — | — |
| Pre-AI boom | — | — | — | — | — |
| AI boom | — | — | — | — | — |

*Panel B: Volatilities (standard deviation of weekly excess returns, %)*

| Comparison period | σ Utilities | σ Technology | σ Market |
| --- | ---: | ---: | ---: |
| Full Sample | — | — | — |
| Pre-Dot-Com | — | — | — |
| Dot-com Crash | — | — | — |
| Pre Financial Crisis | — | — | — |
| Financial Crisis | — | — | — |
| Pre-COVID | — | — | — |
| COVID | — | — | — |
| Pre-AI boom | — | — | — |
| AI boom | — | — | — |

## 5. Checks and Bounds (Fixed Now)

### Checks & Validation

- **Data Quality:** Verify valid returns, consistent units, no unexpected missing or duplicate observations, weekly alignment, and correct week-ending assignments to predefined, sourced periods.
- **Weekly Return Verification:** Verify correct daily-to-weekly compounding and excess returns using consistent weeks across all series.
- **Market Beta Validation:** Verify that both OLS betas match their covariance–variance formulas within numerical tolerance.
- **Partial Correlation Validation:** Verify residual orthogonality to market excess returns, agreement with the analytic partial-correlation formula, and correlations within [−1, 1], allowing for numerical tolerance.

### Bounds

- **Predefined Methodology:** Data sources, variables, weekly return construction, estimation methods, and comparison-period boundaries are fixed before estimating the results.
- **Fixed Sample Cutoff:** The analysis uses the latest common available week across all datasets at the time of data collection. The exact data retrieval date and final sample date must be recorded.
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