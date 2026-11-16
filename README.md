# Volatility and Tail Risk Methods Demo

**Independent technical demonstration · Python · NumPy · Synthetic data**

This newly created personal project illustrates standard risk methods using
anonymous simulated return series. All inputs and outputs are synthetic. It does
not reproduce an employer's project, a real asset universe, or historical results.

## Explore

- [Visual report](docs/index.html) — open locally in a browser, or use GitHub Pages
  after deploying the `docs` directory.
- [Generator and risk methods](src/demo.py)
- [Report builder](src/build_report.py)
- [Mathematical tests](tests/test_demo.py)
- [Generated results and parameters](docs/synthetic_results.csv)

## Method

1. Generate 1,500 daily returns for each of three anonymous series using a
   stationary GARCH(1,1) variance recursion with Gaussian innovations.
2. Compute empirical 99% lower-return quantiles and conditional tail means.
3. Generate 10,000 one-day GBM scenarios for each series using its daily sample
   moments; compare tail estimates at the same horizon.
4. Inspect known generating conditional volatility and record all seeds and
   parameter choices.

The GARCH parameters are specified, not fitted. This project demonstrates
simulation and risk measurement; it does not claim GARCH estimation, forecast
validation, trading performance or language-processing implementation.

## Run

Python 3.10+ and NumPy are required. No network connection is needed after
dependencies have been installed.

```sh
python -m pip install -r requirements.txt
python src/build_report.py
python -m unittest discover -s tests -v
```

The report builder regenerates `docs/index.html`, `docs/synthetic_results.csv` and
`docs/synthetic_series.json`. The JSON contains only synthetic plotting data.

## Conventions

- Returns are decimal daily returns; report tables convert them to percentages.
- VaR is presented as a signed lower-return quantile. CVaR is the mean of returns
  at or below that quantile, using an inclusive threshold for finite samples.
- Negative values are losses. A tail mean is not a worst-case bound.
- GBM uses a daily arithmetic-moment approximation with normally distributed log
  increments; it is not a fitted model of the synthetic GARCH distribution.
- GARCH variance follows `h[t] = omega + alpha*r[t-1]^2 + beta*h[t-1]`, with
  `alpha + beta < 1`. Initial variance equals the stationary variance.

## Limitations

The three series and generating parameters are illustrative choices. Sampling
noise and model assumptions affect comparisons. There is no market-data fit,
out-of-sample test, portfolio aggregation or real-world performance result.
The empirical sample reflects changing variance, while the GBM comparison uses
constant moments. A VaR–CVaR gap alone does not establish a fat-tailed distribution.

## Validation

The report builder was run successfully and five tests passed: an analytical tail
example, the GARCH variance recurrence, seeded reproducibility, the zero-variance
GBM limit, and invalid-input rejection. Dependency ranges are not a version lock;
the checked NumPy version is recorded in `docs/validation.json`.

## Data boundary

This folder contains newly written demonstration code, standard statistical
formulas, and generated synthetic outputs. It contains no company documents,
original research output, real ticker list, raw market observations, credentials,
private links, or discussion of another project's internal implementation.
