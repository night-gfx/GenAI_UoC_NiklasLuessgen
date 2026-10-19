# The Changing Defensive Role of U.S. Utilities During the AI Boom

**Status: Draft (work in progress).** The turning-point algorithm settings, assignment rules, and exact comparison dates are not yet finalized. They must be fixed and documented before estimating the risk measures.

## 1. Research Question

How has the defensive behavior of U.S. utility stocks, measured by market beta, evolved since 1990, and how has their partial correlation with technology stocks changed, particularly during the AI boom?

## 2. Data and Sample

### Data

Data will be obtained from the **Kenneth French Data Library**, using value-weighted portfolios:

- **Utilities:** 12-industry portfolio (Utils).
- **Technology:** 12-industry portfolio (BusEq), used as a technology-oriented proxy.
- **Market:** Fama–French market factor (Mkt-RF) and risk-free rate (RF).

### Sample

- **Period:** January 1990 to the latest available date.
- **Frequency:** Daily returns compounded into weekly returns. Weekly market excess returns will be calculated from separately compounded total market returns and risk-free returns.
- **Comparison periods:** The following historical phases are defined **in advance as comparison categories**, not fixed return-dependent date boundaries:

| Comparison phase | Illustrative reference years (not final boundaries) |
| --- | --- |
| Dot-com boom | 1995–1999 |
| Dot-com bust | 2000–2002 |
| Global financial crisis | 2007–2009 |
| Pre-AI benchmark | 2017–2019 |
| AI boom | 2023–latest available date |

**Period selection to avoid cherry-picking:** Actual start/end dates will be determined systematically using the **Pagan and Sossounov (2003)** turning-point procedure applied to a cumulative index of **monthly BusEq total returns**. The procedure's settings and explicit rules for assigning detected market phases to the comparison categories (including how to handle the financial crisis, pre-AI benchmark, incomplete AI-era phase, and phases for which a matching turning point cannot be identified) must be specified, fixed, and documented **before** estimating beta or partial correlations. Illustrative reference years will not override the precommitted algorithm and assignment rules. Any phases not identified consistently will be reported as such, rather than selected manually to fit the results.

## 3. Constructed Variables

All measures will use aligned **weekly excess returns**. Utilities and technology weekly total returns will be converted into excess returns by subtracting the compounded weekly risk-free return. **Mkt-RF** is an excess-return factor at its original frequency; weekly market excess returns will be computed consistently from separately compounded daily total market returns and RF, rather than summing or compounding daily excess returns as if they were total returns.

- **Market Beta — Sharpe (1964):** The primary measure of defensiveness, defined here as low systematic market risk: sensitivity of utilities excess returns to broad U.S. market excess returns. A lower beta indicates less market sensitivity, but does not necessarily imply protection during downturns:

  $$\beta_{U,M}=\frac{\operatorname{Cov}(R_U^e,R_M^e)}{\operatorname{Var}(R_M^e)}$$

  Estimated as the slope of a simple OLS regression of utilities excess returns on market excess returns, including an intercept.

- **Partial Correlation — Kenett et al. (2015):** Market-adjusted co-movement between utilities and the technology proxy:

  $$\rho_{U,T\mid M}=\operatorname{Corr}(\varepsilon_U,\varepsilon_T)$$

  Here, $\varepsilon_U$ and $\varepsilon_T$ are residuals from **separate OLS regressions** of utilities and BusEq weekly excess returns on the same market excess-return series, each including an intercept. Their correlation measures association after removing the common linear market component. It is **not** a technology beta or evidence that AI caused utilities' returns.

*In the formulas, superscript $e$ denotes excess returns.*

## 4. Identification and Specification

### Identification

The study adopts a **descriptive and correlational** design to compare utilities' market sensitivity and their market-adjusted co-movement with the technology proxy. The design cannot identify causal effects of the AI boom or attribute positive utilities performance to AI-driven electricity demand.

### Specification

The following measures will be estimated separately for each algorithm-defined historical comparison period using aligned weekly excess returns:

1. **Market Beta:** Simple OLS regression of utilities excess returns on market excess returns (with intercept).
2. **Partial Correlation:** Correlation of residuals from separate OLS regressions of utilities and BusEq excess returns on market excess returns (each with intercept).

The two period-specific estimates will be reported in a comparison table. Changes will be interpreted **descriptively**; no claims of statistical significance or causal attribution will be made solely from differences across periods.

### Technical Implementation

The analysis will use Python with **pandas** and **numpy** for data processing and calculations, **statsmodels** for OLS regressions, and **requests** for data retrieval. **Streamlit** and **Plotly** will be used to present the results interactively.

## 5. Checks and Bounds (Fixed Now)

### Checks

- **Data Quality:** Check for missing values, duplicate dates, and alignment of the three portfolios/factors.
- **Return Calculation:** Verify daily-to-weekly compounding, correct weekly excess-return calculations, and aligned dates.
- **Beta Validation:** Verify the simple-OLS market beta against the covariance/variance formula.
- **Partial-Correlation Validation:** Verify that residual-based partial correlation agrees with the analytic partial-correlation formula (within numerical tolerance).
- **Period Selection:** Record the predetermined turning-point and phase-assignment settings, candidate phases, detected dates, and any unmatched or incomplete phases before calculating risk metrics.

### Bounds

- **Predefined Methodology:** Data sources, variables, and frequency are fixed. Turning-point parameters, assignment rules, and final date boundaries must be documented before estimating risk measures.
- **No Cherry-Picking:** The example periods do not dictate final dates. No observations or periods will be selected or removed based on their effect on estimated results.
- **Documentation:** Any methodological changes will be documented in Git.

## 6. What Is Delegated and What Is Not

### Delegated to the AI Agent

- **Data Preparation:** Download and process utilities, technology, and market data using predefined sources and rules.
- **Analysis:** Calculate weekly returns, market beta, and partial correlation; run the specified regressions and report all predefined comparisons.
- **Checks and Documentation:** Run predefined checks and record code changes, results, failures, and package versions.
- **Reporting:** Produce comparison tables, develop a Streamlit dashboard, and draft verifiable data and methods descriptions.
- **Task Boundaries:** Work on a separate Git branch in a restricted workspace with enforced file permissions and approval gates. Stop and ask if a protected file must change, a methodological decision is required, or validation failures cannot be resolved within the approved task.

### Researcher Responsibilities

- **Research Design:** Define the research question, sample, comparison periods, variables, methods, and checks before analysis.
- **Task Definition:** Write a tracked task specification with permitted files and actions, checks, approval requirements, and a step limit. Configure access restrictions in the agent's execution environment.
- **Independent Review:** Inspect code changes, independently rerun checks, validate results, and decide whether to merge the agent's branch.
- **Interpretation and Writing:** Explain the findings and write the motivation, interpretation, conclusions, and limitations.
- **Control:** Approve and document methodological changes.

## References

- Pagan, A. R., & Sossounov, K. A. (2003). A simple framework for analysing bull and bear markets. *Journal of Applied Econometrics, 18*(1), 23–46. https://doi.org/10.1002/jae.664
- Kenett, D. Y., Huang, X., Vodenska, I., Havlin, S., & Stanley, H. E. (2015). Partial correlation analysis: Applications for financial markets. *Quantitative Finance, 15*(4), 569–578. https://doi.org/10.1080/14697688.2014.946660
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *The Journal of Finance, 19*(3), 425–442. https://doi.org/10.1111/j.1540-6261.1964.tb02865.x
