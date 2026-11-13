"""Optional public-market-data workflow, requires network and extra packages.

Example: python examples/market_scan.py --tickers GPRO PLAY HOFT
This scans individual equities; it does not calculate portfolio aggregate risk.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from risk import tail_risk, compare_one_day, fit_garch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", default=["GPRO","PLAY","HOFT"])
    parser.add_argument("--start", default="2018-01-01")
    parser.add_argument("--end", default="2023-12-31")
    parser.add_argument("--garch", action="store_true")
    args = parser.parse_args()
    import yfinance as yf
    out = Path("results"); out.mkdir(exist_ok=True)
    results = []
    failed = []
    for ticker in args.tickers:
        try:
            data = yf.Ticker(ticker).history(start=args.start, end=args.end,
                                            auto_adjust=True)
            close = data["Close"].dropna()
            if len(close) < 101:
                raise ValueError("Insufficient history")
            # Do not forward-fill missing sessions into fabricated zero returns.
            returns = close.pct_change(fill_method=None).dropna().to_numpy()
            row = {"ticker": ticker, "observations": len(returns),
                   "first_price_date": str(close.index[0]),
                   "last_price_date": str(close.index[-1]),
                   "historical_95": tail_risk(returns),
                   "daily_99_comparison": compare_one_day(returns)}
            if args.garch:
                fit = fit_garch(returns)
                row["garch_parameters"] = {k: float(v) for k,v in fit.params.items()}
                np.savetxt(out/f"{ticker}_fitted_volatility_percent.csv",
                           fit.conditional_volatility, delimiter=",",
                           header="in_sample_fitted_conditional_volatility_percent")
            results.append(row)
        except Exception as error:
            failed.append({"ticker":ticker, "error":str(error)})
    output = {"requested_tickers":args.tickers, "start_inclusive":args.start,
              "end_exclusive":args.end, "auto_adjust":True,
              "results":results, "failures":failed}
    (out/"market_scan.json").write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))
    if failed:
        raise SystemExit("Incomplete scan: see explicit failures in market_scan.json")
