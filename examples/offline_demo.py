"""Synthetic method demonstration; never presented as historical performance."""
from pathlib import Path
import sys, json
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from risk import compare_one_day

if __name__ == "__main__":
    # New reproducible demo, not the original internship dataset/results.
    returns = np.random.default_rng(2026).normal(0.0003, 0.025, 1000)
    result = {"data_type": "synthetic normal returns; not market observations",
              "observations": 1000, "horizon_days": 1,
              "scenarios": 10000, "simulation_seed": 42,
              "results": compare_one_day(returns)}
    print(json.dumps(result, indent=2))
