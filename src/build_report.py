"""Build a static report using freshly generated synthetic results only."""
from pathlib import Path
from html import escape
from demo import run


def build():
    rows,series=run()
    table="".join(
        f'<tr><td>{escape(r["series"])}</td>'
        f'<td>{100*r["empirical_quantile"]:.2f}%</td>'
        f'<td>{100*r["empirical_tail_mean"]:.2f}%</td>'
        f'<td>{100*r["gbm_quantile"]:.2f}%</td>'
        f'<td>{100*r["gbm_tail_mean"]:.2f}%</td></tr>' for r in rows)
    vol=series['Synthetic B']['last_250_generating_volatility']
    points=" ".join(f'{40+720*i/(len(vol)-1):.2f},{205-160*v/max(vol):.2f}'
                    for i,v in enumerate(vol))
    css='''*{box-sizing:border-box}body{margin:0;background:#f5f7f8;color:#1f303e;
    font:16px/1.65 system-ui,-apple-system,sans-serif}main{max-width:960px;
    margin:auto;padding:45px 28px}h1{font-size:43px;line-height:1.13;letter-spacing:-1px}
    h2{font-size:25px;line-height:1.3}.eyebrow{color:#146e72;font-size:12px;
    letter-spacing:1.5px;font-weight:700}.lead{font-size:20px;color:#536674}
    section{margin:24px 0;background:white;border:1px solid #dde5e8;
    border-radius:10px;padding:25px 30px}.notice{border-left:4px solid #168086;
    background:#eaf4f3;padding:15px 20px}a{color:#126d73;text-underline-offset:3px}
    table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:11px 9px;
    text-align:left;border-bottom:1px solid #dbe3e7}th{background:#edf3f5}
    svg{width:100%;height:auto}.tablewrap{overflow-x:auto}code{font-size:13px}
    footer{font-size:13px;color:#596e7a}@media(max-width:600px){main{padding:25px 15px}
    section{padding:20px 16px}h1{font-size:33px}}'''
    body=f'''<p class="eyebrow">INDEPENDENT TECHNICAL DEMO · PYTHON · NUMPY</p>
    <h1>Exploring volatility and tail risk</h1>
    <p class="lead">A reproducible, synthetic demonstration of GARCH dynamics,
    empirical tail measures and one-day GBM Monte Carlo simulation.</p>
    <div class="notice"><strong>All observations and results are synthetic.</strong>
    No real equities, company data, research deliverables or news text are used.
    This is a newly created personal methods demonstration.</div>
    <section><h2>What the demonstration implements</h2>
    <ul><li>Generate three anonymous return series, each with 1,500 daily steps,
    using a stationary Gaussian GARCH(1,1) recursion.</li>
    <li>Compute empirical 99% lower-return quantiles (VaR convention) and
    inclusive-threshold tail means (CVaR / Expected Shortfall convention).</li>
    <li>Generate 10,000 one-day GBM draws per series using daily sample moments,
    then compare quantiles and tail means on the same horizon.</li></ul>
    <p>GARCH parameters are specified to generate data; they are not estimated.
    The volatility curve below is known generating volatility, not a fitted
    estimate or a forecast.</p></section>
    <section><h2>Known conditional volatility changes over time</h2>
    <p>Synthetic B · last 250 generated steps · decimal daily volatility.</p>
    <svg viewBox="0 0 800 250" role="img" aria-label="Generating daily conditional volatility for Synthetic B over 250 simulated steps">
    <line x1="40" y1="205" x2="760" y2="205" stroke="#9aadb6"/>
    <polyline points="{points}" fill="none" stroke="#168086" stroke-width="2"/>
    <text x="40" y="230" font-size="13">Simulated step 1</text>
    <text x="640" y="230" font-size="13">Simulated step 250</text>
    <text x="40" y="25" font-size="13">Curve maximum: {max(vol):.4f} · baseline: 0</text>
    </svg><p>The path illustrates the variance recursion, where recent squared
    returns and prior variance affect the next conditional variance. It is not
    a reconstruction of an observed market event.</p></section>
    <section><h2>Empirical and simulated tails need not agree</h2>
    <div class="tablewrap"><table><thead><tr><th>Synthetic series</th>
    <th>Empirical VaR</th><th>Empirical CVaR</th><th>GBM VaR</th><th>GBM CVaR</th>
    </tr></thead><tbody>{table}</tbody></table></div>
    <p>All values are signed daily returns at the 99% confidence convention.
    Negative values represent losses. CVaR averages returns at or below the
    sample quantile; it is not a bound on the worst possible loss.</p>
    <p>The empirical sample has time-varying generating variance; the GBM
    comparator uses constant unconditional daily moments. Differences reflect
    both modeling assumptions and finite simulation/sample variability, not a
    verified performance advantage.</p>
    <p><a href="synthetic_results.csv">Download generated results and parameters</a></p>
    </section><section><h2>Reproducibility and limitations</h2>
    <p>Fixed random seeds are recorded alongside the results. The data generator,
    report builder and five unit tests are included. No network access or account
    credentials are needed to run the demo.</p>
    <ul><li>No GARCH parameter estimation, residual testing or held-out forecast
    evaluation is implemented.</li><li>No real-company outcomes, portfolio
    diversification model, language processing or trading execution is shown.</li>
    <li>Normal-shock assumptions and the GBM moment approximation are deliberate
    simplifications. More scenarios do not eliminate model risk.</li>
    <li>The results demonstrate method behavior, not real asset risk or
    investment performance.</li></ul></section>
    <section><h2>Read or reproduce</h2><p><a href="../README.md">Project overview</a>
    · <a href="../src/demo.py">Data generation and risk methods</a>
    · <a href="../tests/test_demo.py">Tests</a></p>
    <p><code>python src/build_report.py</code> regenerates this report and its
    CSV/JSON assets from the synthetic process.</p></section>
    <footer>Independent statistical methods demonstration · All data synthetic</footer>'''
    target=Path(__file__).resolve().parents[1]/'docs/index.html'
    target.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Volatility and Tail Risk Demo</title><style>'+css+
        '</style></head><body><main>'+body+'</main></body></html>')


if __name__=='__main__':
    build()
