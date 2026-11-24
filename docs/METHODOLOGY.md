# Methodology and Validation

This document records the implementation conventions behind the [project overview](../README.md) and [visual report](index.html). All observations and results are synthetic.

## Synthetic Return Generation

[`simulate_garch`](../src/demo.py) creates three zero-mean Gaussian GARCH(1,1) series, each containing 1,500 daily steps:

```text
h[t] = omega + alpha * r[t-1]^2 + beta * h[t-1]
r[t] = sqrt(h[t]) * z[t], where z[t] ~ Normal(0, 1)
h[0] = omega / (1 - alpha - beta)
```

Parameters satisfy `omega > 0`, `alpha >= 0`, `beta >= 0` and `alpha + beta < 1`. They are specified to generate data, not estimated from observations.

| Series | omega | alpha | beta | Series seed | Monte Carlo seed |
|---|---:|---:|---:|---:|---:|
| Synthetic A | 0.000002 | 0.05 | 0.90 | 1101 | 2100 |
| Synthetic B | 0.000004 | 0.08 | 0.90 | 1102 | 2101 |
| Synthetic C | 0.000008 | 0.12 | 0.85 | 1103 | 2102 |

The report plots the last 250 generating volatility values for Synthetic B. These values are known from the simulation, not fitted estimates or out-of-sample forecasts. The series are illustrative choices, not real equities or portfolio holdings.

## Tail-Risk Conventions

Returns are stored as decimal daily returns; the report converts them to percentages. For confidence level `c = 0.99`:

```text
VaR return threshold = quantile(returns, 1 - c)
CVaR return tail mean = mean(returns at or below that threshold)
```

Both statistics retain their signs. Negative returns represent losses; a more negative number indicates a larger loss magnitude. The inclusive finite-sample threshold can include more than exactly 1% of observations when values are tied. CVaR is a tail average, not the worst possible loss. A VaR–CVaR gap alone does not establish a fat-tailed distribution.

## Monte Carlo Comparison

[`gbm_next_day`](../src/demo.py) generates 10,000 one-day return scenarios per series:

```text
simulated return = exp(mu - 0.5 * sigma^2 + sigma * Z) - 1
```

Here `mu` is the daily arithmetic sample mean, `sigma` is the daily sample standard deviation (`ddof=1`), and `Z` is standard normal. This daily moment approximation uses constant moments; it is not a fit of the synthetic GARCH distribution. All empirical and simulated tail comparisons use a one-day horizon.

The GARCH sample has changing generating variance, while the GBM comparator uses constant unconditional sample moments. Differences reflect model assumptions and finite-sample/simulation variation. They do not establish forecast superiority, causal effects, trading returns or real-market risk.

## Evidence for README Insights

The committed [results CSV](synthetic_results.csv) contains the following Synthetic C values:

| Statistic | Decimal return | Rounded daily return |
|---|---:|---:|
| Empirical 99% VaR | -0.054714501388995224 | -5.47% |
| Empirical 99% CVaR | -0.0729799672316025 | -7.30% |
| GBM 99% CVaR | -0.04849867963174018 | -4.85% |

The CVaR loss-magnitude difference is `(0.0729799672316025 - 0.04849867963174018) * 100 = 2.4481` percentage points, rounded to 2.45. These describe this generated sample only.

## Reproduction and Validation

Run the [report builder](../src/build_report.py) from the repository root using the README commands. It regenerates:

- `docs/index.html`: the self-contained visual report.
- `docs/synthetic_results.csv`: results, parameter settings and random seeds.
- `docs/synthetic_series.json`: synthetic chart data only.

The existing [test suite](../tests/test_demo.py) has five tests covering an analytical empirical-tail example, the GARCH variance recurrence, seeded reproducibility, the zero-variance GBM limit, and invalid-input rejection. Passing these tests checks selected implementation behavior, not model validity or financial performance.

The existing [validation record](validation.json) reports NumPy 2.3.5, five passing tests and report generation. It is a recorded environment, not a dependency lockfile; it is not rewritten by the report builder. Current review checks are documented separately in the change summary.

## Scope and Data Boundary

Only the existing self-contained demonstration and synthetic outputs are used. No employer data, internal workflows, original research outputs, real portfolio holdings, credentials or private links are needed. The project has no GARCH estimation, residual diagnostics, held-out forecast evaluation, cross-asset dependence model or trading execution.
