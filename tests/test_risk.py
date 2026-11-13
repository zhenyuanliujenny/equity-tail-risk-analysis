import unittest, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from risk import tail_risk, simulate_gbm

class RiskTests(unittest.TestCase):
    def test_empirical_tail_definition(self):
        r=tail_risk([-0.20,-0.10,0,0.10,0.20],0.8)
        self.assertAlmostEqual(r["return_quantile"],-0.12)
        self.assertAlmostEqual(r["tail_mean_return"],-0.20)

    def test_gbm_constant_return_limit(self):
        simulated=simulate_gbm([0.01]*5,10,2)
        np.testing.assert_allclose(simulated,np.expm1(0.02))

    def test_seeded_draws_and_tail_ordering(self):
        r=np.random.default_rng(5).normal(0,0.02,1000)
        np.testing.assert_array_equal(simulate_gbm(r),simulate_gbm(r))
        metrics=tail_risk(simulate_gbm(r))
        self.assertLessEqual(metrics["tail_mean_return"],metrics["return_quantile"])

    def test_invalid_inputs(self):
        for values in [[np.nan,0.1],[0.1],[np.inf,0.2]]:
            with self.assertRaises(ValueError):tail_risk(values)

if __name__=="__main__":unittest.main()
