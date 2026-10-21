# Literature

| Source | Data and sample | Method | Key findings | Relevance for this research | Relevant pages / sections | DOI | Local PDF |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fischer Black, Michael C. Jensen & Myron Scholes (1972). **The Capital Asset Pricing Model: Some Empirical Tests.** In Michael C. Jensen (ed.), *Studies in the Theory of Capital Markets*. Praeger. | Monthly NYSE stock and market returns; portfolio tests for January 1931–December 1965, with earlier observations used to form portfolios. | Beta-ranked portfolios; time-series regressions of portfolio excess returns on market excess returns with an intercept; cross-sectional CAPM tests. | High-beta portfolios have negative intercepts and low-beta portfolios positive intercepts, contrary to the traditional CAPM. | Source for excess-return definitions and market beta as covariance with market excess returns divided by market excess-return variance. This project uses weekly rather than monthly returns; it does not replicate their portfolio-sorting tests. | Section I: excess-return and beta definitions; Section II.D: data and monthly portfolio construction; Section II.E.1 and Table 2: time-series results. | Not specified; [paper](https://www.efalken.com/LowVolClassics/blackjensenscholes.pdf). | [Black_Jensen_Scholes_1972_CAPM_Some_Empirical_Tests.pdf](<pdf/Black_Jensen_Scholes_1972_CAPM_Some_Empirical_Tests.pdf>) |
| Lieven Baele & Juan M. Londono (2013). **Understanding Industry Betas.** *Journal of Empirical Finance*, 22, 30–51. | Daily industry excess returns for 30 U.S. industry portfolios; 1970–2009. This project uses the 12-industry classification and weekly returns. | DCC–MIDAS and kernel beta estimation; structural-break analysis. | Industry betas change over time. A common structural break is identified around March 1998. | Supports analyzing time-varying market betas and comparing historical periods over a long sample. This project uses weekly rather than daily returns to balance observations within short crisis periods and short-term fluctuations. Does not supply this project's crisis dates. | p. 30, abstract: time-varying betas and March 1998 break. Exact data-section and time-horizon page references require full-text verification. | [10.1016/j.jempfin.2013.02.003](https://doi.org/10.1016/j.jempfin.2013.02.003) | [Baele_Londono_2013_Understanding_Industry_Betas.pdf](<pdf/Baele_Londono_2013_Understanding_Industry_Betas.pdf>) |
| John Luke Gallup (2019). **Added-variable plots with confidence intervals.** *The Stata Journal*, 19(3), 598–614. | Methodological article illustrated using Stata’s automobile dataset (auto.dta); the main regression example uses 74 observations. No financial-return sample. | Partial regression (Frisch–Waugh–Lovell theorem); separate OLS regressions remove the other covariates from both variables. Added-variable plots display the residual relationship; avciplot adds confidence intervals around the fitted line. | Correlation between the two residual series equals partial correlation. The residual-regression slope equals the corresponding coefficient in the full regression and is distinct from the correlation coefficient. Plots can reveal influential observations. | Supports estimating utilities–technology partial correlation as the Pearson correlation of residuals from separate regressions of weekly sector excess returns on the same market excess returns, each with an intercept and the same observations. Confidence intervals and added-variable plots are not part of the current project specification. | pp. 601–602, Section 2.1: partial regression and residual correlation; p. 606, Section 4: separate residual regressions and degrees of freedom; p. 607: confidence-interval formula and 74-observation example. | [10.1177/1536867X19874236](https://doi.org/10.1177/1536867X19874236) | [Gallup_2019_Added_Variable_Plots_with_Confidence_Intervals.pdf](<pdf/Gallup_2019_Added_Variable_Plots_with_Confidence_Intervals.pdf>) |
| Shietal Ramesh, Rand Kwong Yew Low & Robert Faff (2025). **Modelling time-varying volatility spillovers across crises: Evidence from major commodity futures and the US stock market.** *Energy Economics*, 143, 108225. | Nine commodity futures and the S&P 500; January 1990–February 2022. | Time-varying parameter vector autoregression with stochastic volatility (TVP-VAR-SV) and spillover indices. | Volatility spillovers intensify during crises. The S&P 500 is the largest net transmitter of volatility in the studied system. | Table 2 supplies the dot-com crash (March 2000–October 2002), global financial crisis (June 2007–February 2009), and COVID-19 crisis (March 2020–February 2022) dates. Intervening pre-periods and the December 2022 AI-boom start are researcher choices. The paper provides crisis dates, not direct evidence for utility–technology partial correlations. | Abstract; Section 4 (Data), p. 5; Table 2 (Crises timeline), p. 7; Appendix A.1 (crisis date justifications), p. 17. | [10.1016/j.eneco.2025.108225](https://doi.org/10.1016/j.eneco.2025.108225) | [Ramesh_Low_Faff_2025_Time_Varying_Volatility_Spillovers_Across_Crises.pdf](<pdf/Ramesh_Low_Faff_2025_Time_Varying_Volatility_Spillovers_Across_Crises.pdf>) |

## Categorized literature index

### How to use this index for later questions

- **Retrieval scope:** For questions about **Empirical Evidence**, consult only the papers under Defensiveness and Interconnection below. If a question specifies one of these topics, use only that subsection. For **Methodological** questions, use only Beta or Partial Correlation as requested; if Methodological is requested without a subsection, use both methodological subsections; for **Further Evidence**, use only that section. Expand the source set only when the researcher asks for it. Secondary relevance notes do not automatically expand the source set.
- **Reading procedure:** Use this index to select the local PDFs, then read the relevant passages, tables, or formulas in those PDFs before answering. Cite the actual local version and printed page and/or table number (also give the PDF page when cover sheets or scans make navigation ambiguous); the index is a navigation aid, not a substitute for full-text evidence.
- **Verification level:** Identification and initial classification are based on the first two PDF pages, including visual inspection of scanned pages. Existing matrix details above are retained. Details not established on those pages are marked **Unverified detail** or explicitly require later verification. The pre-existing table above is preserved and has not been revalidated beyond the opening pages; its later-page, table, and numerical claims require a fresh PDF check before reuse. No full-text review has been completed for this classification.
- **File naming:** `Author_Author_Year_Short_Title.pdf`; use `et_al` for more than three authors, ASCII spellings in filenames, and a version suffix where needed. The filename year identifies the local version, which may differ from the researcher's journal citation. All 18 PDFs are retained, representing 16 indexed works with two additional copies/versions. For journal-formatted articles, use the issue/publication year printed on the local article, not an earlier online-availability, acceptance, or copyright year. For dated working papers and preprints, use their own version date.

## Empirical Evidence

### Defensiveness

| Paper | PDF | LLM Findings | Human Review |
| --- | --- | --- | --- |
| **González, Jareño & Skinner (2016). Interest and Inflation Risk: Investor Behavior.** | [Gonzalez_Jareno_Skinner_2016_Interest_and_Inflation_Risk.pdf](<pdf/Gonzalez_Jareno_Skinner_2016_Interest_and_Inflation_Risk.pdf>) | • Market beta of Tech / Utilities is 1.385 / 0.467 overall, 1.239 / 0.571 in contractions, and 1.473 / 0.379 in expansions (González et al., 2016, p. 7, Table 4, Model 1). | ✅ Verified |
|  |  | • Monthly return volatility of Tech / Utilities is 7.5% / 4.4% (González et al., 2016, p. 6, Table 3). |  |
|  |  | • Minimum monthly return of Tech / Utilities is −32.8% / −15.1% (González et al., 2016, p. 6, Table 3). |  |
|  |  | **Extra:** |  |
|  |  | ▪ All p < 0.01 versus zero (González et al., 2016, p. 7, Table 4, Model 1). | ✅ Verified |
|  |  | ▪ Market: 4.3% (González et al., 2016, p. 6, Table 3). |  |
|  |  | ▪ US GICS sectors (González et al., 2016, pp. 6–7). |  |
|  |  | ▪ 292 monthly log returns, Nov. 1989–Feb. 2014 (González et al., 2016, pp. 6–7). |  |
|  |  | ▪ SUR controls for market and nominal-rate changes (González et al., 2016, pp. 6–7). |  |
|  |  | ▪ Model 2 gives similar betas (González et al., 2016, pp. 6–7). |  |
|  |  | ▪ Pooled contractions: Jul. 1990–Feb. 1991, Apr.–Nov. 2001, Jan. 2008–Mar. 2011 (González et al., 2016, p. 5, Table 2). |  |
|  |  | ▪ 55 contraction / 237 expansion months (González et al., 2016, p. 5, Table 2). |  |
|  |  | ▪ Last contraction includes recovery (González et al., 2016, p. 5, Table 2). |  |
|  |  | ▪ No direct tests of phase-beta/volatility differences or isolated financial-crisis estimate in Tables 3–4 (González et al., 2016, pp. 6–7). |  |
| **Bernanke & Kuttner — What Explains the Stock Market’s Reaction to Federal Reserve Policy?** Researcher citation: **2005**; local version: **2003**. | [Bernanke_Kuttner_2003_Stock_Market_Reaction_to_Federal_Reserve_Policy_Working_Paper.pdf](<pdf/Bernanke_Kuttner_2003_Stock_Market_Reaction_to_Federal_Reserve_Policy_Working_Paper.pdf>) | • Market beta of Tech / Utilities is 1.61 / 0.32 (Bernanke & Kuttner, 2003, p. 30, Table 8; PDF p. 32). | ✅ Verified |
|  |  | • Return response to a 1-pp unexpected Fed rate increase of Tech / Utilities is −14.73 / −5.42 pp (Bernanke & Kuttner, 2003, p. 30, Table 8; PDF p. 32). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Beta significance not reported (Bernanke & Kuttner, 2003, p. 30, Table 8; PDF p. 32). |  |
|  |  | ▪ Absolute t = 2.72 / 1.55 (Bernanke & Kuttner, 2003, p. 30, Table 8; PDF p. 32). |  |
|  |  | ▪ Ten Fama–French US industries (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ 164 monthly observations, May 1989–Dec. 2002 (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Regressions on expected/unexpected Fed changes (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Betas from market excess-return regressions (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Tech rate response significant at conventional 1% level (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Utilities not significant at 10% (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Rate sensitivity is distinct from market beta (Bernanke & Kuttner, 2003, pp. 30–31; PDF pp. 32–33). |  |
|  |  | ▪ Local version is 2003, not 2005 (Bernanke & Kuttner, 2003, p. 30; PDF p. 32). |  |
|  |  | ▪ Table 8 has no phase-specific estimates or unconditional volatility (Bernanke & Kuttner, 2003, p. 30; PDF p. 32). |  |
| **Baele & Londono (2013). Understanding Industry Betas.** | [Baele_Londono_2013_Understanding_Industry_Betas.pdf](<pdf/Baele_Londono_2013_Understanding_Industry_Betas.pdf>) | • Unconditional market beta of Tech / Utilities is 1.31 / 0.59, highest / lowest among 30 industries (Baele & Londono, 2013, p. 33, Table 1; PDF p. 4). | ✅ Verified |
|  |  | • Annualized daily excess-return volatility of Tech / Utilities is 29.19% / 15.66% (Baele & Londono, 2013, p. 33, Table 1; PDF p. 4). |  |
|  |  | • NBER recession effect on kernel market beta of Tech / Utilities is −0.07 / +0.02 (Baele & Londono, 2013, p. 43, Table 9A; PDF p. 14). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Significance not reported (Baele & Londono, 2013, p. 33, Table 1; PDF p. 4). |  |
|  |  | ▪ Market: 18.58% (Baele & Londono, 2013, p. 33, Table 1; PDF p. 4). |  |
|  |  | ▪ Neither significant (Baele & Londono, 2013, p. 43, Table 9A; PDF p. 14). |  |
|  |  | ▪ Tech proxy = Business equipment, not exact GICS/XLK equivalent (Baele & Londono, 2013, p. 33, Table 1; PDF p. 4). |  |
|  |  | ▪ Thirty value-weighted US industries (Baele & Londono, 2013, pp. 35, 41; PDF pp. 6, 12). |  |
|  |  | ▪ Daily log excess returns, Jan. 1969–Dec. 2009 (Baele & Londono, 2013, pp. 35, 41; PDF pp. 6, 12). |  |
|  |  | ▪ DCC–MIDAS/kernel betas (Baele & Londono, 2013, pp. 35, 41; PDF pp. 6, 12). |  |
|  |  | ▪ Kernel sample ends Dec. 2008 (Baele & Londono, 2013, pp. 35, 41; PDF pp. 6, 12). |  |
|  |  | ▪ Recession regressions: quarterly betas, Newey–West HAC with four lags (Baele & Londono, 2013, pp. 33, 43; PDF pp. 4, 14). |  |
|  |  | ▪ No isolated financial-crisis estimate (Baele & Londono, 2013, pp. 33, 43; PDF pp. 4, 14). |  |
|  |  | ▪ Table 1 gives no volatility-difference tests (Baele & Londono, 2013, pp. 33, 43; PDF pp. 4, 14). |  |
| **Amankwah, Moradi-Motlagh & Valadkhani (2026). Asymmetric responses of the sectoral ETFs to market extremes: evidence from the left and right tails.** | [Amankwah_Moradi-Motlagh_Valadkhani_2026_Asymmetric_Responses_of_Sectoral_ETFs.pdf](<pdf/Amankwah_Moradi-Motlagh_Valadkhani_2026_Asymmetric_Responses_of_Sectoral_ETFs.pdf>) | • Downside beta of Tech / Utilities is 1.114 / 0.669 (optimal), 0.899 / 0.806 (10%), and 0.844 / 0.852 (5%) overall (Amankwah et al., 2026, p. 345, Table 3; PDF p. 12). |  |
|  |  | • Upside beta of Tech / Utilities is 1.154 / 0.649 (optimal), 1.092 / 0.790 (10%), and 1.020 / 0.878 (5%) overall (Amankwah et al., 2026, p. 345, Table 3; PDF p. 12). |  |
|  |  | • Downside beta of Tech / Utilities is 1.063 / 0.608 in 1999–2007 and 0.916 / 0.848 in 2008–2023, at 10% tails (Amankwah et al., 2026, pp. 347, 349, Tables 5, 7; PDF pp. 14, 16). |  |
|  |  | • Upside beta of Tech / Utilities is 1.538 / 0.272 in 1999–2007 and 1.004 / 0.704 in 2008–2023, at 10% tails (Amankwah et al., 2026, pp. 347, 349, Tables 5, 7; PDF pp. 14, 16). |  |
|  |  | • Daily return volatility of Tech / Utilities is 1.621% / 1.216% (Amankwah et al., 2026, p. 344, Table 2; PDF p. 11). |  |
|  |  | • Minimum daily return of Tech / Utilities is −14.866% / −12.056% (Amankwah et al., 2026, p. 344, Table 2; PDF p. 11). |  |
|  |  | **Extra:** |  |
|  |  | ▪ SPY: 1.223% (Amankwah et al., 2026, p. 344, Table 2; PDF p. 11). |  |
|  |  | ▪ Difference tests not reported (Amankwah et al., 2026, p. 344, Table 2; PDF p. 11). |  |
|  |  | ▪ Nine sector ETFs plus SPY (Amankwah et al., 2026, pp. 339–341; PDF pp. 6–8). |  |
|  |  | ▪ Daily data, 1 Jan. 1999–17 Oct. 2023 (Amankwah et al., 2026, pp. 339–341; PDF pp. 6–8). |  |
|  |  | ▪ Threshold regressions (Amankwah et al., 2026, pp. 339–341; PDF pp. 6–8). |  |
|  |  | ▪ Tech = XLK, Utilities = XLU (Amankwah et al., 2026, pp. 339–341; PDF pp. 6–8). |  |
|  |  | ▪ Post-GFC starts 1 Jan. 2008 and includes the crisis (Amankwah et al., 2026, pp. 341, 348–349; PDF pp. 8, 15–16). |  |
|  |  | ▪ Pre/post windows are not pure expansion/recession phases (Amankwah et al., 2026, pp. 341, 348–349; PDF pp. 8, 15–16). |  |
|  |  | ▪ Tech upside exceeds downside beta at every threshold/period (Amankwah et al., 2026, pp. 347–350, Tables 4, 6, 8; PDF pp. 14–17). |  |
|  |  | ▪ 10% Wald F = 27.68 / 12.76 / 9.53 overall/pre/post, all p < 0.01 (Amankwah et al., 2026, pp. 347–350, Tables 4, 6, 8; PDF pp. 14–17). |  |
|  |  | ▪ Utilities downside beta stays below one at all thresholds/periods (Amankwah et al., 2026, pp. 345–350, Tables 3–8; PDF pp. 12–17). |  |
|  |  | ▪ 10% asymmetry insignificant overall (F = 0.13), significant pre-GFC (F = 5.38, p < 0.05) (Amankwah et al., 2026, pp. 345–350, Tables 3–8; PDF pp. 12–17). |  |
|  |  | ▪ Wald tests compare betas, not beta versus one (Amankwah et al., 2026, pp. 345–350, Tables 3–8; PDF pp. 12–17). |  |
|  |  | ▪ Errors: wrong periods in Table 5 footnote / Table 6 heading (Amankwah et al., 2026, pp. 347–350; PDF pp. 14–17). |  |
|  |  | ▪ Post-GFC XLU 10% beta difference is +0.144 in Table 7, not −0.06 in Table 8 (Amankwah et al., 2026, pp. 347–350; PDF pp. 14–17). |  |
|  |  | ▪ Corresponding asymmetry test unreliable (Amankwah et al., 2026, pp. 347–350; PDF pp. 14–17). |  |
|  |  | ▪ Downside beta is tail market sensitivity, not VaR/Expected Shortfall/drawdown (Amankwah et al., 2026, pp. 339, 344–345; PDF pp. 6, 11–12). |  |
|  |  | ▪ Daily minima are observations, not loss quantiles (Amankwah et al., 2026, pp. 339, 344–345; PDF pp. 6, 11–12). |  |
|  |  | ▪ Both minimum daily returns occur on 16 Mar. 2020 (Amankwah et al., 2026, p. 344, Table 2; PDF p. 11). |  |

### Interconnection

| Paper | PDF | LLM Findings | Human Review |
| --- | --- | --- | --- |
| **Ferreira & Gama (2010). Correlation dynamics of global industry portfolios.** | [Ferreira_Gama_2010_Correlation_Dynamics_of_Global_Industry_Portfolios.pdf](<pdf/Ferreira_Gama_2010_Correlation_Dynamics_of_Global_Industry_Portfolios.pdf>) | • Pairwise Tech–Utilities correlation (raw or market-adjusted) is not reported; only each industry's correlation with the world market (Ferreira & Gama, 2010, p. 37, Eq. 1; PDF p. 3). |  |
|  |  | • Mean monthly realized correlation with the world market of Tech / Utilities is 0.681 / 0.692 [1979–2008] (Ferreira & Gama, 2010, p. 40, Table 1; PDF p. 6). |  |
|  |  | • Linear trend coefficient (×10,000) of this correlation of Tech / Utilities is 4.412 / −0.328; t-PST 0.57 / −0.36 (Ferreira & Gama, 2010, p. 40, Table 1; PDF p. 6). |  |
|  |  | • Mean correlation with the world market of Tech / Utilities is 0.697 / 0.680 (1979–83), 0.596 / 0.684 (1984–88), 0.617 / 0.800 (1989–93), 0.613 / 0.707 (1994–98), 0.811 / 0.517 (1999–2003), and 0.751 / 0.764 (2004–08) (Ferreira & Gama, 2010, p. 40, Table 2; PDF p. 6). |  |
|  |  | • Contemporaneous (lag 0) correlation between this market-correlation series and an NBER expansion dummy of Tech / Utilities is −0.17 / −0.05 (Ferreira & Gama, 2010, p. 41, Table 3; PDF p. 7). |  |
|  |  | • Mean correlation with the world market of Tech / Utilities is 0.704 / 0.719 in down months and 0.668 / 0.677 in up months (Ferreira & Gama, 2010, p. 42, Table 4; PDF p. 8). |  |
|  |  | • Slope of this correlation on the world market return of Tech / Utilities is 0.797 / 0.324 in down months and 0.268 / −0.584 in up months (Ferreira & Gama, 2010, p. 43, Table 5; PDF p. 9). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Trends insignificant: t-PST below the 5% critical value of 1.72 (Ferreira & Gama, 2010, p. 40, Table 1; PDF p. 6). |  |
|  |  | ▪ Time effects p = 0.000 for both; H0: equal means across the six 60-month subperiods (Ferreira & Gama, 2010, p. 40, Table 2; PDF p. 6). |  |
|  |  | ▪ Down = Up p-value of Tech / Utilities is 0.072 / 0.016 for mean correlations and 0.072 / 0.013 for slopes (Ferreira & Gama, 2010, pp. 42–43, Tables 4–5; PDF pp. 8–9). |  |
|  |  | ▪ Slope t-statistics: Tech 3.56 (down) / 0.94 (up); Utilities 0.92 (down) / −1.83 (up) (Ferreira & Gama, 2010, p. 43, Table 5; PDF p. 9). |  |
|  |  | ▪ Recession increase in correlation ranges from 9.2% (Basic Materials) to 2.8% (Utilities); Tech value not reported (Ferreira & Gama, 2010, p. 42, fn. 5; PDF p. 8). |  |
|  |  | ▪ Technology is the only industry without a late-1990s correlation decline; its market correlation rose from the mid-1990s until stabilizing in 2004 (Ferreira & Gama, 2010, p. 38, Fig. 1; PDF p. 4). |  |
|  |  | ▪ Correlation with the market proxies an industry's average pairwise correlation with the other industries (Ferreira & Gama, 2010, p. 37, fn. 2; PDF p. 3). |  |
|  |  | ▪ Global ICB industries from Datastream; USD total-return indexes incl. dividends; 53 countries in 2008; industry value = cross-sectional average of Level-4 sector correlations; not U.S.-only (Ferreira & Gama, 2010, p. 37; PDF p. 3). |  |
|  |  | ▪ Daily returns, monthly realized correlations, Jan. 1979–Dec. 2008; market = Datastream value-weighted world portfolio (Ferreira & Gama, 2010, p. 37; PDF p. 3). |  |
|  |  | ▪ SUR across ten industries, Newey–West with 5 lags; Vogelsang (1998) t-PST trend test (Ferreira & Gama, 2010, pp. 40–43; PDF pp. 6–9). |  |
|  |  | ▪ Recessions = NBER-dated U.S. cycles as world proxy; down/up = sign of monthly world return (Ferreira & Gama, 2010, pp. 39, 41–42; PDF pp. 5, 7–8). |  |
|  |  | ▪ Error: text announces five 60-month subperiods, Table 2 shows six (Ferreira & Gama, 2010, pp. 40–41; PDF pp. 6–7). |  |
|  |  | ▪ Error: text says Down = Up is rejected for all ten groups, but Tech p = 0.072 (Ferreira & Gama, 2010, pp. 43–44, Table 5; PDF pp. 9–10). |  |
|  |  | ▪ Contradiction: conclusion says the correlation–volatility link is stronger in rising markets, contrary to Section 4 (Ferreira & Gama, 2010, pp. 44, 46; PDF pp. 10, 12). |  |
| **Mensi, Nekhili, Vo, Suleman & Kang (2021). Asymmetric volatility connectedness among U.S. stock sectors.** | [Mensi_et_al_2021_Asymmetric_Volatility_Connectedness.pdf](<pdf/Mensi_et_al_2021_Asymmetric_Volatility_Connectedness.pdf>) | • Pairwise return correlation of Tech–Utilities is 0.5591 [unconditional, 2012–2018] (Mensi et al., 2021, p. 8, Table 2). |  |
|  |  | • Pairwise volatility spillover received by Tech from Utilities / by Utilities from Tech is 0.34 / 0.56 [% of 10-day forecast error variance; realized volatility] (Mensi et al., 2021, p. 9, Table 3). |  |
|  |  | • Same pairwise spillover is 0.61 / 0.54 for good volatility (positive semivariance) (Mensi et al., 2021, p. 10, Table 4). |  |
|  |  | • Same pairwise spillover is 0.39 / 0.70 for bad volatility (negative semivariance) (Mensi et al., 2021, p. 11, Table 5). |  |
|  |  | • Net total directional spillover of Tech / Utilities is −29.9 / −9.5 (realized volatility), −29.3 / −7.5 (good), and −25.6 / −9.0 (bad); both are net receivers (Mensi et al., 2021, pp. 9–11, Tables 3–5). |  |
|  |  | • Market-adjusted correlation is not reported (Mensi et al., 2021, pp. 5–11). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Ten U.S. sector indices plus Total Market; index provider not named (Mensi et al., 2021, p. 5). |  |
|  |  | ▪ Five-minute intraday data, 21 Sept. 2012–31 Dec. 2018; 1578 daily realized-volatility observations (Mensi et al., 2021, p. 5). |  |
|  |  | ▪ Diebold–Yilmaz (2012) generalized VAR(2), 10-day horizon; realized semivariances (Baruník et al., 2017) (Mensi et al., 2021, pp. 3–4, 9). |  |
|  |  | ▪ No significance tests for spillovers or correlations (Mensi et al., 2021, pp. 8–11, Tables 2–5). |  |
|  |  | ▪ No market phases; time variation via rolling windows; Markov regime-switching as robustness (Mensi et al., 2021, pp. 2, 4, 16). |  |
|  |  | ▪ Text: Technology receives more risk under bad than good volatility; Utilities shows asymmetry between good and bad volatility transmission (Mensi et al., 2021, p. 20). |  |
|  |  | ▪ Contradiction: rolling window is 180 days in text but 200 observations in footnote 2 (Mensi et al., 2021, p. 4). |  |
|  |  | ▪ Data error: Utilities statistics are identical to Financials (Mensi et al., 2021, p. 7, Table 1). |  |
|  |  | ▪ Data error: Utilities rows in Tables 3–5 equal the Financials rows, with 41–42% spillover between the two (Mensi et al., 2021, pp. 9–11, Tables 3–5). |  |
|  |  | ▪ Data error: Utilities row in Table 2 duplicates the Con. Services column (Utilities–Con. Services = 1.0000); Tech–Utilities = Tech–Con. Services = 0.5591 (Mensi et al., 2021, p. 8, Table 2). |  |
|  |  | ▪ Utilities results are therefore unreliable; Con. Goods correlations of ≈0 with all sectors are also implausible (Mensi et al., 2021, p. 8, Table 2). |  |
|  |  | ▪ Volatility connectedness differs from return correlation (Mensi et al., 2021, pp. 3–5). |  |
| **Ngene (2021). What drives dynamic connectedness of the U.S equity sectors during different business cycles?** | [Ngene_2021_Dynamic_Connectedness_of_US_Equity_Sectors.pdf](<pdf/Ngene_2021_Dynamic_Connectedness_of_US_Equity_Sectors.pdf>) | • Pairwise volatility spillover received by Tech from Utilities / by Utilities from Tech is 5.7 / 5.8 [% of 24-week forecast error variance; full sample] (Ngene, 2021, p. 9, Table 2). |  |
|  |  | • Net directional spillover of Tech / Utilities is −9.3 / −10.6 [%]; both are net receivers (Ngene, 2021, p. 9, Table 2). |  |
|  |  | • Spillover to others of Tech / Utilities is 60.5 / 58.0 and from others 69.8 / 68.6 [%] (Ngene, 2021, p. 9, Table 2). |  |
|  |  | • Own-variance share of Tech / Utilities is 30.2 / 31.4 [%] (Ngene, 2021, p. 9, Table 2). |  |
|  |  | • Net pairwise index (NPDI) Tech–Utilities and phase-specific pairwise values are not reported; NPDI is only defined (Ngene, 2021, p. 7, Eq. 8). |  |
|  |  | • Market-adjusted correlation is not reported (Ngene, 2021, pp. 3–14). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Nine MSCI U.S. sector indices in USD; TEC = Technology, UTL = Utilities (Ngene, 2021, p. 3). |  |
|  |  | ▪ Weekly Friday-to-Friday log returns, 1 June 1994–15 Jan. 2021; 1392 observations (Ngene, 2021, p. 3). |  |
|  |  | ▪ GJR-GARCH(1,1) conditional variances in a TVP-VAR(1) (BIC); generalized FEVD, 24-week horizon (Ngene, 2021, pp. 6–7, 9). |  |
|  |  | ▪ No significance tests for connectedness measures (Ngene, 2021, p. 9, Table 2). |  |
|  |  | ▪ NBER recession dummy only in total-connectedness regressions, not in pairwise results (Ngene, 2021, pp. 7–8). |  |
|  |  | ▪ TEC is a net receiver until ≈2013 and shows intensifying transmission after ≈2014–15 (Ngene, 2021, pp. 10–11, Fig. 3; Fig. 3 on p. 12). |  |
|  |  | ▪ UTL is a net receiver over the whole sample; its receiving role intensifies after ≈2014–15 (Ngene, 2021, pp. 10–11, Fig. 3; Fig. 3 on p. 12). |  |
|  |  | ▪ Error: text refers to Table 3 for connectedness results shown in Table 2 (Ngene, 2021, p. 9). |  |
|  |  | ▪ Error: text lists −10.6 / −9.3 / −5.8 for UTL / CSI / HCI, but Table 2 gives CSI −7.57 and TEC −9.3 (Ngene, 2021, p. 9, Table 2). |  |
|  |  | ▪ Volatility connectedness differs from return correlation (Ngene, 2021, pp. 6–7). |  |
| **Kallberg & Pasquariello (2008). Time-series and cross-sectional excess comovement in stock indexes.** | [Kallberg_Pasquariello_2008_Excess_Comovement_in_Stock_Indexes.pdf](<pdf/Kallberg_Pasquariello_2008_Excess_Comovement_in_Stock_Indexes.pdf>) | • Pairwise Tech–Utilities excess correlation is not reported; sector values average each industry's significant squared residual correlations with all other industries (Kallberg & Pasquariello, 2008, p. 484, Eq. 5; p. 490, Table 2; PDF pp. 4, 10). |  |
|  |  | • Mean excess square correlation (FGLS residuals) of Tech / Utilities is 0.081 / 0.099 [weekly, Oct. 1979–Dec. 2001] (Kallberg & Pasquariello, 2008, p. 490, Table 2; PDF p. 10). |  |
|  |  | • Benchmark raw square correlation of Tech / Utilities is 0.278 / 0.153 (Kallberg & Pasquariello, 2008, p. 490, Table 2; PDF p. 10). |  |
|  |  | • Mean ratio of excess to raw square correlation of Tech / Utilities is 29% / 64% (Kallberg & Pasquariello, 2008, p. 490, Table 2; PDF p. 10). |  |
|  |  | • NBER recession dummy effect on excess comovement of Tech / Utilities is −0.0020 / −0.0042 (model 1) and −0.0023 / −0.0032 (model 2) (Kallberg & Pasquariello, 2008, p. 497, Table 4; PDF p. 17). |  |
|  |  | • Restrictive-Fed dummy effect of Tech / Utilities is 0.0091 / −0.0046 (model 1) and 0.0096 / −0.0031 (model 2) (Kallberg & Pasquariello, 2008, p. 498, Table 4; PDF p. 18). |  |
|  |  | • Three-month T-bill coefficient of Tech / Utilities is 0.0952 / −0.2104 (model 1) and 0.0700 / −0.1760 (model 2) (Kallberg & Pasquariello, 2008, p. 497, Table 4; PDF p. 17). |  |
|  |  | **Extra:** |  |
|  |  | ▪ Excess square correlations significant at 1% for both; H0: ρ* = 0 vs. ρ* > 0 (Kallberg & Pasquariello, 2008, p. 490, Table 2; PDF p. 10). |  |
|  |  | ▪ Recession: Tech not significant (t = −1.01 / −1.32); Utilities significant at 10% in model 1 (t = −1.83), not in model 2 (t = −1.52) (Kallberg & Pasquariello, 2008, p. 497, Table 4; PDF p. 17). |  |
|  |  | ▪ Restrictive Fed: Tech significant at 1%; Utilities at 5% / 10% (Kallberg & Pasquariello, 2008, p. 498, Table 4; PDF p. 18). |  |
|  |  | ▪ T-bill coefficients all significant at 1% (Kallberg & Pasquariello, 2008, p. 497, Table 4; PDF p. 17). |  |
|  |  | ▪ Adjusted R² of Tech / Utilities is 70.71–72.76% / 19.63–19.64% (Kallberg & Pasquariello, 2008, p. 498, Table 4; PDF p. 18). |  |
|  |  | ▪ 82 Datastream U.S. industry indexes (FTSE classification), value-weighted, dividend-adjusted weekly log returns, 5 Jan. 1976–31 Dec. 2001 (Kallberg & Pasquariello, 2008, pp. 486–487; PDF pp. 6–7). |  |
|  |  | ▪ Tech = Information Technology (Computer Hardware & Service, Semiconductors, Telecom Equipment); Utilities = Electricity, Gas Distribution, Water (Kallberg & Pasquariello, 2008, p. 491; PDF p. 11). |  |
|  |  | ▪ Joint FGLS rolling regressions (N = 100 weeks) on sector, macro-sector, market, HML, and SMB factors (Kallberg & Pasquariello, 2008, p. 488, Eq. 19; PDF p. 8). |  |
|  |  | ▪ Residual correlations volatility-adjusted (4-year window); only correlations significant at 10% kept, then squared (Kallberg & Pasquariello, 2008, pp. 484, 488; PDF pp. 4, 8). |  |
|  |  | ▪ Table 4: OLS with Newey–West standard errors (Kallberg & Pasquariello, 2008, p. 498; PDF p. 18). |  |
|  |  | ▪ Phases: NBER recession weeks (165 of 1158); restrictive Fed per Jensen et al. (1996) (Kallberg & Pasquariello, 2008, p. 498; PDF p. 18). |  |
|  |  | ▪ Excess comovement peaks in 1990 and 1996–97 for many sectors, except Utilities and IT, which show the widest fluctuations (Kallberg & Pasquariello, 2008, p. 491; PDF p. 11). |  |
|  |  | ▪ Controls include sector factors, unlike a market-only partial correlation; squaring removes the sign (Kallberg & Pasquariello, 2008, pp. 484, 488; PDF pp. 4, 8). |  |
| **Buccheri, Marmi & Mantegna (2013). Evolution of correlation structure of industrial indices of U.S. equity markets.** | [Buccheri_Marmi_Mantegna_2013_Evolution_of_Correlation_Structure.pdf](<pdf/Buccheri_Marmi_Mantegna_2013_Evolution_of_Correlation_Structure.pdf>) | • Pairwise Tech–Utilities correlation values are not reported; only network and eigenvalue analyses (Buccheri et al., 2013, pp. 012806-2–012806-6). |  |
|  |  | • Cluster membership of Tech / Utilities is C4 (Hardw, Softw, Chips, LabEq, Other) / C1 (financial, business services, construction, wholesale, utilities) [PMFG, full-sample daily correlations] (Buccheri et al., 2013, pp. 012806-2–012806-3, Figs. 2–4). | ✅ Verified |
|  |  | • Dot-com period (Mar. 1999–Apr. 2001): second eigenvector loads strongly positive on the C4 tech industries, while most others are near zero or negative; tech correlations decouple from the rest (Buccheri et al., 2013, p. 012806-6, Fig. 10). |  |
|  |  | • Variance explained by the first eigenvalue is ≈31% in the dot-com period and ≈70% in 2008–09; the second explains up to ≈16% (Buccheri et al., 2013, p. 012806-6). |  |
|  |  | **Extra:** |  |
|  |  | ▪ 49 Fama–French value-weighted U.S. industry portfolios; daily returns, July 1969–Dec. 2011; 10,621 trading days (Buccheri et al., 2013, pp. 012806-1–012806-2). | ✅ Verified |
|  |  | ▪ Monthly Pearson correlation matrices from 3-month windows; PMFG, Infomap clusters, link mutual information, Spearman rank correlation, eigenvalues (Buccheri et al., 2013, pp. 012806-1–012806-5). |  |
|  |  | ▪ No significance tests; raw correlations without market adjustment (Buccheri et al., 2013, pp. 012806-1–012806-6). |  |
|  |  | ▪ Periods: dot-com Mar. 1999–Apr. 2001; subprime Aug. 2008–Aug. 2009 (Buccheri et al., 2013, p. 012806-1). |  |
|  |  | ▪ Error: Fig. 1 caption dates the 9/11 attack to September 2011 (Buccheri et al., 2013, p. 012806-2). |  |
|  |  | ▪ Error: second-eigenvalue change dated “June–March 2001” (Buccheri et al., 2013, p. 012806-5). |  |
|  |  | ▪ Inconsistency: dot-com window ends April 2001 in text but May 2001 in Fig. 10 (Buccheri et al., 2013, p. 012806-6). |  |
|  |  | ▪ Inconsistency: start date June 1969 in appendix vs. July 1969 elsewhere (Buccheri et al., 2013, pp. 012806-1, 012806-7). |  |

## Methodological

### Beta

| Paper | Methodological role | Local PDF / verification notes |
| --- | --- | --- |
| **Black, Jensen & Scholes (1972). The Capital Asset Pricing Model: Some Empirical Tests.** | Core source for market beta and empirical CAPM testing (PDF pp. 1–2: title, chapter year, abstract). See the existing matrix row above for the project's excess-return definitions and regression interpretation. | [Primary local copy](pdf/Black_Jensen_Scholes_1972_CAPM_Some_Empirical_Tests.pdf); [additional SSRN copy](pdf/Black_Jensen_Scholes_1972_CAPM_Some_Empirical_Tests_SSRN_Copy.pdf). Both identify the same 1972 chapter on PDF pp. 1–2; their file hashes differ, so both are retained. Both opening pages point to SSRN; “SSRN_Copy” distinguishes the incoming ssrn-908569.pdf file, not a demonstrated textual revision. No separate revision date appears on those pages; 1972 is the stated chapter year. |
| **Newey & West — A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix.** Existing filename citation: **1987**; local version: **1986**. | Supplementary source for inference using a positive semi-definite HAC covariance estimator. Supports regression uncertainty estimates; it does not define or replace the market-beta point estimator. | [April 1986 NBER Technical Working Paper no. 55](pdf/Newey_West_1986_HAC_Covariance_Matrix_Working_Paper.pdf), PDF pp. 1–2: cover and abstract visually checked. Detailed inference conditions remain unverified. Classification does not authorize a change to the project's estimation or standard-error methods. |

### Partial Correlation

| Paper | Methodological role | Local PDF / verification notes |
| --- | --- | --- |
| **Kenett, Huang, Vodenska, Havlin & Stanley — Partial correlation analysis: Applications for financial markets.** Researcher citation: **2015**; local version: **2014**. | Financial-market motivation: observed correlation may reflect another variable's influence; partial correlation examines the remaining association after controlling for that variable. Includes stock and sector applications. | [Preprint dated 7 February 2014, arXiv v1](pdf/Kenett_et_al_2014_Partial_Correlation_Analysis_Preprint.pdf), pp. 1–2. Treat the market as this project's control; partial correlation alone does not establish causality. The cited 2015 journal version is not present. |
| **Gallup (2019). Added-variable plots with confidence intervals.** | Complementary regression-based explanation of conditioning on covariates and visualizing the residual relationship. See the existing matrix row above for residual correlation and its distinction from the residual-regression slope. | [PDF](pdf/Gallup_2019_Added_Variable_Plots_with_Confidence_Intervals.pdf). PDF pp. 1–2 (printed pp. 598–599): abstract and introduction. Use alongside Kenett when asked to compare the financial motivation with regression implementation; neither source is an empirical utilities–technology result. |
| **Fisher (1921). On the “Probable Error” of a Coefficient of Correlation deduced from a Small Sample.** | Supplementary source for correlation inference and small-sample uncertainty, rather than a direct source for this project's residualization procedure. | [Journal scan](pdf/Fisher_1921_Probable_Error_of_a_Correlation_Coefficient_Journal_Scan.pdf). The opening pages are the September 1921 *Metron*, Vol. 1, No. 4 cover/contents and announcements; the contents identify Fisher's article starting on printed p. 3. This file is a journal-issue scan, including material beyond Fisher's article. Read the article itself before citing transformations, assumptions, or formulas. |

## Further Evidence

| Paper | Supporting role | Local PDF / verification notes |
| --- | --- | --- |
| **Valadkhani (2025). Inflation-driven instability in US sectoral betas.** | Monthly sector-ETF betas modeled as functions of annualized inflation, January 1999–February 2024; beta reliability deteriorates outside moderate inflation ranges. Additional context for beta instability. | [PDF](pdf/Valadkhani_2025_Inflation_Driven_Instability_in_US_Sectoral_Betas.pdf), abstract and introduction, p. 506. The abstract discusses 1–5% and particularly 4–5% on the upside; the introduction uses 1–4%. Verify the results before stating an exact threshold. Interest rates are discussed as context; do not infer a separately estimated interest-rate effect from the opening pages. |
| **Ramesh, Low & Faff (2025). Modelling time-varying volatility spillovers across crises: Evidence from major commodity futures and the US stock market.** | Crisis-period and cross-asset spillover context using nine commodity futures and the S&P 500, 1990–2022; TVP-VAR-SV with Diebold–Yilmaz spillover indices. See the existing matrix row for crisis-date references. | [PDF](pdf/Ramesh_Low_Faff_2025_Time_Varying_Volatility_Spillovers_Across_Crises.pdf). The first PDF page is a repository cover sheet; the second contains the article abstract. Provides supporting crisis context, not direct utilities–technology defensiveness or partial-correlation evidence. |
