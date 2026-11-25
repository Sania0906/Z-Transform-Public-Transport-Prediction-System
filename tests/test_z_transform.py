"""
Unit Tests for Module 2 Z-Transform Mathematical Engine.
Tests transfer function estimation, pole-zero roots, BIBO stability criteria,
and Inverse Z-Transform impulse response synthesis.
"""

import unittest
import numpy as np
from modules.z_transform_engine import ZTransformEngine

class TestZTransformEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ZTransformEngine(ar_order=3)
        np.random.seed(42)
        # Generate known stable AR(2) process: s[n] = 0.6 s[n-1] - 0.2 s[n-2] + w[n]
        # Poles: roots of z^2 - 0.6z + 0.2 = 0 -> |z| = sqrt(0.2) ≈ 0.447 < 1 (Stable)
        N = 100
        w = np.random.normal(0, 5, N)
        s = np.zeros(N)
        for i in range(2, N):
            s[i] = 0.6 * s[i-1] - 0.2 * s[i-2] + w[i]
        self.synthetic_s = s

    def test_autocorrelation_symmetry(self):
        r = self.engine.compute_autocorrelation(self.synthetic_s, max_lag=4)
        self.assertEqual(len(r), 5)
        # r[0] is maximum (signal energy)
        self.assertTrue(all(r[0] >= abs(r[k]) for k in range(1, 5)))

    def test_yule_walker_transfer_function(self):
        b_poly, a_poly, sigma_w2 = self.engine.estimate_system_transfer_function(self.synthetic_s)
        self.assertEqual(len(b_poly), 1)
        self.assertEqual(b_poly[0], 1.0)
        self.assertEqual(len(a_poly), 4) # [1.0, -a1, -a2, -a3]
        self.assertEqual(a_poly[0], 1.0)
        self.assertGreater(sigma_w2, 0.0)

    def test_pole_zero_and_bibo_stability(self):
        b_poly, a_poly, _ = self.engine.estimate_system_transfer_function(self.synthetic_s)
        pz = self.engine.analyze_poles_and_zeros(b_poly, a_poly)
        
        self.assertEqual(len(pz['poles']), 3)
        self.assertIn("spectral_radius", pz)
        # All poles for this synthetic process should be strictly inside unit circle
        self.assertLess(pz['spectral_radius'], 1.0, "Stable process must have spectral radius < 1.0.")
        self.assertTrue(pz['is_bibo_stable'])

    def test_inverse_z_transform_impulse_response(self):
        b_poly = np.array([1.0])
        a_poly = np.array([1.0, -0.5]) # Pole at z = 0.5 -> h[n] = (0.5)^n
        n_axis, h_n, residues = self.engine.compute_inverse_z_transform_impulse(b_poly, a_poly, n_points=10)
        
        self.assertEqual(len(h_n), 10)
        # Theoretical h[0]=1.0, h[1]=0.5, h[2]=0.25, h[3]=0.125
        expected = 0.5 ** np.arange(10)
        np.testing.assert_allclose(h_n, expected, atol=1e-3)

    def test_frequency_response(self):
        b_poly = np.array([1.0])
        a_poly = np.array([1.0, -0.4])
        w, mag_db, phase_deg = self.engine.compute_frequency_response(b_poly, a_poly, worN=64)
        self.assertEqual(len(w), 64)
        self.assertEqual(len(mag_db), 64)
        self.assertEqual(len(phase_deg), 64)
        # DC gain: H(1) = 1 / (1 - 0.4) = 1.667 -> 20*log10(1.667) ≈ 4.43 dB
        self.assertAlmostEqual(mag_db[0], 20.0 * np.log10(1.6667), delta=0.5)

    def test_full_pipeline_execution(self):
        res = self.engine.run_full_pipeline(self.synthetic_s + 400.0, forecast_steps=3)
        self.assertIn("final_forecast", res)
        self.assertEqual(len(res["final_forecast"]), 3)
        self.assertIn("ci_lower", res)
        self.assertIn("ci_upper", res)
        self.assertTrue(all(res["ci_lower"] <= res["final_forecast"]))
        self.assertTrue(all(res["final_forecast"] <= res["ci_upper"]))

if __name__ == '__main__':
    unittest.main()
