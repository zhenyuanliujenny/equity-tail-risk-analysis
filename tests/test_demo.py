import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from demo import simulate_garch,empirical_tail,gbm_next_day


class MethodTests(unittest.TestCase):
    def test_hand_computed_empirical_tail(self):
        quantile,tail=empirical_tail([-0.2,-0.1,0,0.1,0.2],0.8)
        self.assertAlmostEqual(quantile,-0.12)
        self.assertAlmostEqual(tail,-0.2)

    def test_garch_variance_recurrence(self):
        r,v=simulate_garch(n=20,seed=40)
        self.assertAlmostEqual(v[0],0.000004/(1-0.08-0.90))
        np.testing.assert_allclose(v[1:],0.000004+0.08*r[:-1]**2+0.90*v[:-1])
        self.assertTrue(np.all(v>0))

    def test_reproducibility(self):
        a,_=simulate_garch();b,_=simulate_garch()
        np.testing.assert_array_equal(a,b)
        np.testing.assert_array_equal(gbm_next_day(a),gbm_next_day(b))

    def test_gbm_zero_variance_limit(self):
        np.testing.assert_allclose(gbm_next_day([0.01]*10),np.expm1(0.01))

    def test_reject_invalid_samples_and_parameters(self):
        with self.assertRaises(ValueError):simulate_garch(alpha=0.1,beta=0.9)
        with self.assertRaises(ValueError):empirical_tail([float('nan'),0.1])
        with self.assertRaises(ValueError):empirical_tail([0.1,0.2],1)


if __name__=="__main__":unittest.main()
