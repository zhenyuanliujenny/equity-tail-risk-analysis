# Methods and source mapping

## Reviewed materials

The M12 `python code` folder contains nine notebooks: Week 2 through Week 10. The final report was also read. This review does not claim to cover every document in milestones M1–M12.

| Source | Material used |
|---|---|
| Weeks 2–5 | Context on market data preparation, returns, drawdowns and visualization |
| Week 6 | Historical 95% / 99% daily return quantiles |
| Week 7 | 10,000-path GBM construction, one-day historical/Monte Carlo comparison, historical CVaR |
| Week 8 | Assumed crash-return simulation; recognized as synthetic scenarios, not calibrated stock outcomes |
| Week 9 | Per-window historical risk comparisons and `arch` GARCH(1,1) code for GPRO, PLAY, HOFT |
| Week 10 | 12 requested tickers, 11 returned; saved aggregate risk table; illustrative PTON annotations |
| Final report | Research context and proposed integration; deployment/NLP/loss-avoidance claims are not treated as verified |

## Definitions

For daily simple returns r and confidence c, q = quantile(r, 1-c). The empirical expected shortfall is mean(r where r ≤ q). Values are stored as signed returns. Loss magnitudes can be expressed as -q and -ES when both are negative. The finite-sample inclusive threshold can include more than exactly 1-c of observations when returns are tied.

The tail multiplier ES/q is reported only when q is negative. It is a descriptive ratio, not proof of non-normality. Historical quantiles make no parametric normal assumption, unlike a normal-innovation GBM or the selected GARCH innovation distribution.

The GBM refactor uses daily arithmetic-return mean mu and sample standard deviation sigma, as the original code does. For each daily step, log gross return is approximated by mu - sigma²/2 + sigma Z. This is a modeling approximation; it is not a fitted heavy-tail model. Historical and simulated comparisons use the same one-day horizon, with 10,000 simulation draws and an explicit seed. No cross-asset dependence or portfolio weights are modeled.

## GARCH scope

The source fits returns multiplied by 100, with constant mean, GARCH(1,1), and normal innovations. Its `conditional_volatility` output is fitted sample volatility. Estimation windows are:

| Crisis example | Ticker | Fit start | Fit end (provider exclusive) | Display window |
|---|---|---|---|---|
| 2018 | GPRO | 2017-01-01 | 2019-12-31 | 2018-09-01 to 2018-12-31 |
| 2020 | PLAY | 2018-01-01 | 2020-12-31 | 2020-01-01 to 2020-05-31 |
| 2022 | HOFT | 2020-01-01 | 2022-12-31 | 2021-11-01 to 2022-06-30 |

Because full estimation samples include future observations relative to plotted dates, the fitted plots cannot establish prospective early warnings. A genuine forecasting study would need time-ordered train/test splits or rolling estimation, benchmark forecasts, and appropriate calibration and forecast-loss evaluation. Those are proposed extensions, not completed work.

## Snapshot provenance

`reported_risk_snapshot.csv` transcribes rounded text output from the Week 10 notebook. The requested ticker set was PLAY, AMC, SHAK, OSUR, GPRO, SONO, IRBT, CWST, PTON, BYND, WDFC, HOFT. IRBT returned an error and is absent from the results. No missing ticker value is imputed. The nominal 12-ticker research universe is not proof of 12 successful fits and should not be labeled a verified 12-stock aggregate portfolio model.

The snapshot is based on a long pooled history, not separate statistics for each of the three crises. Week 9 contains distinct crisis-period exercises. New provider downloads may differ; actual observation counts and coverage should always be reported.

## Portfolio refactor

New implementation files simplify the source's methods without reproducing every chart, notebook cell, simulated assumption, or speculative annotation. Synthetic demo data are generated locally with known parameters and clearly labeled. No source notebook output is executed as code. New unit tests check an analytical tail example, the zero-volatility GBM limit, seeded determinism, tail ordering, and invalid inputs.

## Further work

- Obtain and audit authorized historical inputs; compare refactor results with original outputs.
- Pin and validate dependency versions after an end-to-end run.
- Add rolling/held-out forecasting evaluation and coverage diagnostics.
- Evaluate sensitivity to return definitions, sample windows, normal-innovation assumptions and missing ticker histories.
- Treat any future NLP module as a separate measured implementation requiring a documented corpus, scoring method, time alignment and evaluation.
