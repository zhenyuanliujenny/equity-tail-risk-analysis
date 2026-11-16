"""Independent synthetic demonstration of standard risk methods.

No external data, credentials, company output, news text or trading execution.
GARCH paths use specified generating parameters, not fitted estimates.
"""
from pathlib import Path
import csv
import json
import numpy as np


def simulate_garch(n=1500, omega=0.000004, alpha=0.08, beta=0.90, seed=1):
    """Zero-mean GARCH(1,1), Gaussian innovations, decimal daily returns."""
    if n < 2 or omega <= 0 or alpha < 0 or beta < 0 or alpha+beta >= 1:
        raise ValueError("Require n >= 2, omega > 0 and stationary parameters")
    innovations = np.random.default_rng(seed).standard_normal(n)
    variance = np.empty(n)
    returns = np.empty(n)
    variance[0] = omega/(1-alpha-beta)
    returns[0] = np.sqrt(variance[0])*innovations[0]
    for t in range(1,n):
        variance[t] = omega+alpha*returns[t-1]**2+beta*variance[t-1]
        returns[t] = np.sqrt(variance[t])*innovations[t]
    return returns, variance


def empirical_tail(returns, confidence=0.99):
    """Signed lower-return quantile and inclusive-threshold tail mean."""
    values = np.asarray(returns,dtype=float)
    if values.ndim != 1 or values.size < 2 or not np.isfinite(values).all():
        raise ValueError("Expected at least two finite scalar observations")
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie strictly between 0 and 1")
    threshold = float(np.quantile(values,1-confidence))
    return threshold,float(values[values<=threshold].mean())


def gbm_next_day(returns, scenarios=10000, seed=100):
    """Moment-based one-day GBM approximation; mu/sigma are daily moments."""
    values=np.asarray(returns,dtype=float)
    empirical_tail(values)  # validate the input sample
    if scenarios < 2:
        raise ValueError("At least two scenarios are required")
    mu=values.mean();sigma=values.std(ddof=1)
    shocks=np.random.default_rng(seed).standard_normal(scenarios)
    return np.expm1(mu-0.5*sigma*sigma+sigma*shocks)


def run():
    # Anonymous parameter choices for method demonstration only.
    configs=[("Synthetic A",0.000002,0.05,0.90,1101),
             ("Synthetic B",0.000004,0.08,0.90,1102),
             ("Synthetic C",0.000008,0.12,0.85,1103)]
    rows=[];series={}
    for i,(label,omega,alpha,beta,seed) in enumerate(configs):
        returns,variance=simulate_garch(omega=omega,alpha=alpha,beta=beta,seed=seed)
        draws=gbm_next_day(returns,seed=2100+i)
        hq,he=empirical_tail(returns);mq,me=empirical_tail(draws)
        rows.append(dict(series=label,observations=len(returns),scenarios=len(draws),
                         horizon_days=1,confidence=0.99,
                         generating_omega=omega,generating_alpha=alpha,
                         generating_beta=beta,series_seed=seed,mc_seed=2100+i,
                         empirical_quantile=hq,empirical_tail_mean=he,
                         gbm_quantile=mq,gbm_tail_mean=me))
        series[label] = dict(last_250_returns=returns[-250:].tolist(),
                             last_250_generating_volatility=np.sqrt(variance[-250:]).tolist())
    root=Path(__file__).resolve().parents[1]
    docs=root/"docs";docs.mkdir(exist_ok=True)
    with (docs/"synthetic_results.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (docs/"synthetic_series.json").write_text(json.dumps(series,indent=2))
    print(json.dumps({"data":"synthetic; no market observations", "results":rows},indent=2))
    return rows,series


if __name__=="__main__":
    run()
