"""Core research methods refactored from the supplied internship notebooks.

This portfolio implementation was prepared after the internship. It is not the
original delivered source, a trading system, or a validation of trading results.
Returns use decimal units; quantiles and expected shortfalls retain their signs.
"""
import numpy as np


def _sample(values):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size < 2 or not np.isfinite(values).all():
        raise ValueError("Provide at least two finite returns in one dimension.")
    return values


def tail_risk(returns, confidence=0.95):
    """Empirical lower-return quantile and mean of observations at/below it.

    These are signed return statistics. With negative tails, their negatives
    express loss magnitudes. Non-negative tails must not be labeled losses.
    The finite-sample ES uses the source's inclusive threshold convention.
    """
    returns = _sample(returns)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    quantile = float(np.quantile(returns, 1-confidence))
    shortfall = float(returns[returns <= quantile].mean())
    return {"confidence": confidence, "return_quantile": quantile,
            "tail_mean_return": shortfall,
            "tail_multiplier": shortfall/quantile if quantile < 0 else None}


def simulate_gbm(returns, scenarios=10000, days=1, seed=42):
    """GBM research approximation using daily arithmetic-return moments.

    Matches the source's daily mu/sigma convention; no annualized dt is used.
    This is not a calibrated stochastic-volatility or fat-tail model.
    An explicit seed and horizon are portfolio reproducibility improvements.
    """
    returns = _sample(returns)
    if not isinstance(scenarios, int) or scenarios < 2:
        raise ValueError("scenarios must be an integer of at least two")
    if not isinstance(days, int) or days < 1:
        raise ValueError("days must be a positive integer")
    mu, sigma = returns.mean(), returns.std(ddof=1)
    z = np.random.default_rng(seed).standard_normal((days, scenarios))
    log_increments = mu - 0.5*sigma**2 + sigma*z
    return np.expm1(log_increments.sum(axis=0))


def compare_one_day(returns, confidence=0.99, scenarios=10000, seed=42):
    """Use identical daily horizons for the empirical and GBM comparisons."""
    return {"historical": tail_risk(returns, confidence),
            "gbm": tail_risk(simulate_gbm(returns, scenarios, 1, seed), confidence)}


def fit_garch(returns):
    """Fit normal-innovation, constant-mean GARCH(1,1) in percent units.

    Returns fitted model results. conditional_volatility is in-sample fitted
    volatility, not an out-of-sample forecast or verified advance warning.
    """
    from arch import arch_model
    returns = _sample(returns)
    if returns.size < 100:
        raise ValueError("Use at least 100 daily returns for this research fit.")
    result = arch_model(100*returns, mean="Constant", vol="GARCH",
                        p=1, q=1, dist="normal").fit(disp="off")
    if result.convergence_flag != 0:
        raise RuntimeError("GARCH optimizer did not converge")
    return result
