# The Changing Defensive Role of U.S. Utilities During the AI Boom

**Status: Draft (work in progress).** The turning-point algorithm settings, historical period-selection rules, and exact comparison dates are not yet finalized. They must be fixed and documented before estimating the risk measures.

## 1. Research Question

How do the U.S. utilities sector's market beta, downside beta, and market-adjusted correlation with technology stocks compare across historical periods, including the dot-com era and the AI boom?

## 2. Data, Sample and Exclusions

### Data

Data will be obtained from the **Kenneth French Data Library**, using value-weighted portfolios:

- **Utilities:** 12-industry portfolio (Utils).
- **Technology:** 12-industry portfolio (BusEq).
- **Market:** Fama–French market factor (Mkt-RF) and risk-free rate (RF).

### Sample

- **Period:** January 1980 to the latest available date.
- **Frequency:** Daily returns compounded into weekly returns. Weekly market excess returns will be calculated from separately compounded market and risk-free returns.
- **Comparison periods:** Dot-com boom, dot-com bust, pre-AI period, and AI era. Historical turning points will be identified using Pagan and Sossounov (2003) on a cumulative return index constructed from monthly BusEq returns. Algorithm settings, selection rules, and date boundaries remain open and must be fixed before estimation.

### Exclusions

- Non-U.S. markets and individual stocks.
- Observations with missing return data.

## 3. Constructed Variables

All measures will use weekly returns. Utilities and technology returns will be converted to excess returns by subtracting the risk-free rate; **Mkt-RF** already represents market excess returns.

- **Market Beta — Sharpe (1964):** Sensitivity of utilities returns to market movements:

  $$\beta_{U,M}=\frac{\operatorname{Cov}(R_U,R_M)}{\operatorname{Var}(R_M)}=\rho_{U,M}\frac{\sigma_U}{\sigma_M}$$

  Beta will also be decomposed into **market correlation** and **relative volatility** (utilities volatility divided by market volatility).

- **Downside Beta — Ang, Chen & Xing (2006):** Market sensitivity in weeks when market excess returns are below their mean within the comparison period:

  $$\beta^-_{U,M}=\frac{\operatorname{Cov}(R_U,R_M\mid R_M<\overline{R}_M)}{\operatorname{Var}(R_M\mid R_M<\overline{R}_M)}$$

- **Partial Correlation — Kenett et al. (2015):** Correlation between utilities and technology returns after controlling for the overall market:

  $$\rho_{U,T\mid M}=\frac{\rho_{U,T}-\rho_{U,M}\rho_{T,M}}{\sqrt{(1-\rho_{U,M}^2)(1-\rho_{T,M}^2)}}$$

  This will be calculated by separately regressing utilities and technology excess returns on market excess returns and correlating the residuals.

*In the formulas, returns are excess returns.*

## 4. Identification and Specification

### Identification

This study uses a descriptive and correlational approach to compare utilities' risk characteristics across historical periods. It does not establish causality.

### Specification

The following measures will be estimated separately for each period using weekly excess returns:

- **Market Beta:** OLS regression of utilities excess returns on market excess returns, including a decomposition into market correlation and relative volatility.
- **Downside Beta:** The same regression, restricted to market excess returns below their period mean.
- **Partial Correlation:** Correlation between the residuals from separate OLS regressions of utilities and technology excess returns on market excess returns.

The period-specific estimates will be presented in a comparison table. Differences will be interpreted descriptively, without claims of statistical significance.

### Technical Implementation

The analysis will use Python with **pandas** and **numpy** for data processing and calculations, **statsmodels** for OLS regressions, and **requests** for data retrieval. **Streamlit** and **Plotly** will be used to present the results interactively.

## 5. Checks and Bounds (Fixed Now)

### Checks

- **Data Quality:** Check for missing values and duplicate dates.
- **Return Calculation:** Verify daily-to-weekly compounding, correct market excess-return and risk-free-rate calculations, and aligned dates.
- **Beta Validation:** Verify that regression-based beta equals beta calculated from correlation and relative volatility.

### Bounds

- **Predefined Methodology:** Data sources, variables, and frequency are fixed. Period-selection rules and date boundaries must be documented before estimating the risk measures.
- **No Cherry-Picking:** No observations will be removed based on their impact on the results.
- **Documentation:** Any methodological changes will be documented in Git.

## 6. What Is Delegated and What Is Not

### Delegated to the AI Agent

- **Data Preparation:** Download and process utilities, technology, and market data using predefined sources and rules.
- **Analysis:** Calculate weekly returns, market beta, downside beta, and partial correlation; run the specified regressions and report all predefined comparisons.
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
- Ang, A., Chen, J., & Xing, Y. (2006). Downside risk. *The Review of Financial Studies, 19*(4), 1191–1239. https://doi.org/10.1093/rfs/hhj035
- Kenett, D. Y., Huang, X., Vodenska, I., Havlin, S., & Stanley, H. E. (2015). Partial correlation analysis: Applications for financial markets. *Quantitative Finance, 15*(4), 569–578. https://doi.org/10.1080/14697688.2014.946660
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *The Journal of Finance, 19*(3), 425–442. https://doi.org/10.1111/j.1540-6261.1964.tb02865.x
