# Equity Tail Risk Analysis

**Zhenyuan Liu · Python · NumPy · pandas · GARCH · Monte Carlo · VaR / CVaR**

A research portfolio based on work completed during my Innovation AI internship. I was responsible for data acquisition and cleaning, risk calculations, Monte Carlo simulation, GARCH analysis, visualizations, and reporting. The original exercises also reference supervisor guidance and a supplied base example; this portfolio does not claim invention of the methods or sole authorship of all instructional material.

## Start here

- [Visual project report](docs/index.html) — open locally in a browser, or via GitHub Pages after publishing.
- [Core risk methods](src/risk.py)
- [Offline synthetic example](examples/offline_demo.py)
- [Optional historical-data example](examples/market_scan.py)
- [Reported historical snapshot](docs/reported_risk_snapshot.csv)
- [Methods, source mapping, and limitations](docs/methods.md)

## Research question

How do historical loss quantiles, expected shortfall, and time-varying volatility describe equity downside risk across market stress periods? The project progressed from daily-return and drawdown analysis to historical VaR, GBM Monte Carlo comparison, and GARCH conditional-volatility analysis.

## Implemented in the supplied notebooks

| Component | Evidence | Scope |
|---|---|---|
| Market-data preparation | `yfinance`, pandas, NumPy; cleaning and CSV outputs | Public equity histories, with coverage and missing-data limitations |
| Historical VaR / CVaR | Lower return quantiles and tail means at 95% / 99% levels | Individual-asset daily risk; not a weighted portfolio-risk engine |
| Monte Carlo | 10,000 GBM scenarios; historical vs simulated 99% daily VaR comparison | The source also constructs annual paths; the reported comparison uses a one-day horizon |
| GARCH(1,1) | Python `arch`, normal innovations; GPRO / PLAY / HOFT crisis examples | Retrospective fitted conditional volatility, not validated advance prediction |
| 12-ticker scan | VaR/CVaR bars and a relative risk heatmap | 12 requested; 11 returned in the saved output because IRBT failed |

## Selected historical results

The supplied Week 10 output covers requested prices from 2018-01-01 to 2023-12-31 (provider end date exclusive); histories can differ by ticker. These figures are saved notebook outputs, not fresh downloads or trading performance.

| Ticker | Daily 95% VaR | Daily 95% CVaR | Reported tail multiplier |
|---|---:|---:|---:|
| AMC | -9.05% | -15.56% | 1.72× |
| PLAY | -5.58% | -10.32% | 1.85× |
| GPRO | -5.28% | -8.85% | 1.68× |

VaR is the lower-return threshold; CVaR is the mean return at or below that threshold. A negative CVaR is not a maximum possible loss. The multiplier describes the sample tail relative to its quantile; it is not evidence of a fat-tailed distribution by itself. A normal distribution also has a nonzero VaR–CVaR gap.

## Run the offline demonstration

Python 3.10+ with NumPy:

```sh
python -m pip install -r requirements.txt
python examples/offline_demo.py
python -m unittest discover -s tests -v
```

The demonstration uses explicitly synthetic normal returns and a fixed random seed. It validates code behavior and illustrates the method; its output must not be described as real equity results or a replication of the saved internship output.

## Optional historical-data / GARCH workflow

```sh
python -m pip install -r requirements-market.txt
python examples/market_scan.py --tickers GPRO PLAY HOFT --start 2018-01-01 --end 2023-12-31 --garch
```

This downloads adjusted historical prices and writes results locally. Provider access, licensing, ticker availability, corporate actions, and revisions can affect output. The optional market-data and `arch` paths have not been run in the portfolio preparation environment. GARCH fitting should also be reviewed for residual behavior, stability, and sample adequacy before substantive use.

## What changed for this portfolio

The Python files in `src/` and `examples/` are a new, compact refactor prepared from the notebook methods, not a verbatim copy of the internship deliverables. New changes include fixed random seeds, explicit confidence/horizon conventions, input checks, convergence checks, no inline package installation, and explicit failed-ticker reporting. Mathematical unit tests and an offline run verify the core implementation. No performance improvement is attributed to the internship from these later changes.

## Boundary between implementation and proposal

The final narrative discusses an NLP + GARCH dual-trigger trading system. The reviewed code does not substantiate a working NLP pipeline, connected broker, live automated trading, or verified loss avoidance. In the PTON illustration, sentiment text/score and event dates are hard-coded; the displayed bands use 10-day rolling volatility rather than GARCH. These illustrative claims are excluded from this portfolio's implemented results.

The GARCH crisis fits use estimation samples extending through and beyond the displayed crisis windows, so those plots must not be called out-of-sample forecasts. The stock universe and stress windows were selected retrospectively; this creates selection and hindsight bias.

## Data and sharing

No private company dataset, raw price history, access credentials, meeting links, recordings, or internal report is included. The displayed aggregate metrics come from the supplied notebooks. No open-source license is assigned pending confirmation of permission to publish internship-derived code and outputs. This is a statistical research project; no investment-return or production-system claim is made.

## Validation status

Core Python syntax, four mathematical/input tests, and the seeded offline demo were checked. Historical data retrieval, GARCH execution, and numerical equivalence to the source notebook outputs remain unverified in this environment. Dependency ranges describe intended compatibility, not a locked or fully tested environment.
