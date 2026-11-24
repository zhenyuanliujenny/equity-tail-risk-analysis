# Volatility and Tail Risk Analysis

A Python demonstration comparing downside-risk estimates from synthetic GARCH return series and 10,000 one-day Monte Carlo scenarios.

## Project Overview

A loss threshold does not tell us how severe losses can be beyond it. This project compares Value at Risk (VaR) with Conditional Value at Risk (CVaR, also called Expected Shortfall), then examines how a constant-volatility simulation changes those estimates.

The analysis uses three synthetic series of 1,500 daily returns each. All results are simulated, not historical financial outcomes.

## Key Insights

- **Tail losses extend beyond the VaR threshold.** For Synthetic C, the empirical 99% VaR is **−5.47%**, while CVaR is **−7.30%**: the average return in the sample tail is more negative than its threshold.
- **Model assumptions affect the estimated tail.** For the same series, empirical CVaR is **−7.30%**, compared with **−4.85%** under the GBM simulation—a **2.45 percentage-point difference in loss magnitude**. This is a comparison within one synthetic example, not evidence that either method predicts market losses better.

Numbers are rounded from the [generated results](docs/synthetic_results.csv); both comparisons use a 99% confidence level and a one-day horizon.

## Methods & Tools

- **GARCH(1,1) simulation:** generates changing conditional volatility using specified parameters, rather than fitting a model to observations.
- **Monte Carlo:** generates 10,000 one-day Geometric Brownian Motion (GBM) scenarios per series using its daily sample mean and standard deviation.
- **VaR / CVaR:** compares a lower-return quantile with the mean return at or below that threshold.
- **Python and NumPy:** implement simulation, numerical calculations and reproducible random seeds.

[Methodology and validation notes](docs/METHODOLOGY.md) provide the equations, assumptions and test details.

## Visual Report

**[Open the report file](docs/index.html)** for the volatility chart, results table and interpretation. GitHub displays HTML source; download the file and open it in a browser to view the rendered report. Running the command below also creates a local copy.

## How to Run

Requires Python 3.10+ and NumPy. From the repository root:

```sh
python -m pip install -r requirements.txt
python src/build_report.py
python -m unittest discover -s tests -v
```

Open `docs/index.html` in a browser. The builder regenerates the report, `docs/synthetic_results.csv` and `docs/synthetic_series.json`. No network access is needed after installing dependencies.

## Limitations

All data are synthetic. GARCH parameters are specified, not estimated; the volatility chart shows the generating process, not a forecast. Results reflect modeling assumptions and sampling variability. This demo includes no market backtesting, out-of-sample validation, portfolio aggregation, production deployment or trading-performance evaluation. CVaR is not a worst-case loss bound.
