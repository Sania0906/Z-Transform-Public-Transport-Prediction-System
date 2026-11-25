"""
Unit & Integration Tests for Module 1 Data Pipeline.
Tests GPS coordinate math, Kalman trajectory denoising, Hampel outlier detection, and signal conditioning.
"""

import unittest
import numpy as np
import pandas as pd
from modules.data_acquisition import TransitDataAcquisition
from modules.preprocessing import DataPreprocessor, KalmanGPSFilter

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        self.acq = TransitDataAcquisition()

    def test_haversine_distance(self):
        # Known coordinates: San Francisco to Oakland (~13 km)
        lat1, lon1 = 37.7749, -122.4194
        lat2, lon2 = 37.8044, -122.2712
        dist = self.acq.haversine_distance_km(lat1, lon1, lat2, lon2)
        self.assertGreater(dist, 10.0)
        self.assertLess(dist, 16.0)

    def test_calculate_bearing(self):
        # Due north
        bearing_north = self.acq.calculate_bearing(37.77, -122.41, 37.87, -122.41)
        self.assertAlmostEqual(bearing_north, 0.0, delta=1.0)
        # Due east
        bearing_east = self.acq.calculate_bearing(37.77, -122.41, 37.77, -122.31)
        self.assertAlmostEqual(bearing_east, 90.0, delta=1.0)

    def test_simulate_telemetry_tick(self):
        vehicles = self.acq.get_active_vehicles()
        vid = vehicles.iloc[0]['vehicle_id']
        before_dist = vehicles.iloc[0]['distance_to_next_km']
        
        updated = self.acq.simulate_telemetry_tick(vid, step_seconds=10.0)
        self.assertIn("latitude", updated)
        self.assertIn("longitude", updated)
        self.assertIn("speed_kmh", updated)

    def test_kalman_filter_denoising(self):
        kf = KalmanGPSFilter(dt=1.0, process_noise_std=0.01, measurement_noise_std=0.5)
        true_lats = np.linspace(37.770, 37.780, 25)
        true_lons = np.linspace(-122.420, -122.410, 25)
        
        # Inject Gaussian sensor noise
        np.random.seed(42)
        noisy_lats = true_lats + np.random.normal(0, 0.0005, 25)
        noisy_lons = true_lons + np.random.normal(0, 0.0005, 25)

        flats, flons = kf.filter_trajectory(noisy_lats, noisy_lons)
        
        noisy_error = np.mean((noisy_lats - true_lats)**2 + (noisy_lons - true_lons)**2)
        filtered_error = np.mean((flats - true_lats)**2 + (flons - true_lons)**2)
        
        self.assertLess(filtered_error, noisy_error, "Kalman filter must reduce mean squared tracking error.")

    def test_hampel_filter_outlier_rejection(self):
        clean = np.array([400.0, 405.0, 398.0, 402.0, 404.0, 401.0, 399.0, 403.0])
        # Inject artificial outlier spike
        noisy = clean.copy()
        noisy[3] = 950.0 # Extreme spike
        
        filtered, outliers = DataPreprocessor.hampel_filter(noisy, window_size=3, n_sigmas=3.0)
        self.assertIn(3, outliers, "Outlier at index 3 must be detected.")
        self.assertLess(filtered[3], 450.0, "Spike must be replaced by local median.")

    def test_signal_normalization_and_inversion(self):
        seq = np.array([100.0, 200.0, 300.0, 400.0, 500.0])
        norm_seq, params = DataPreprocessor.normalize_signal(seq, method='standard')
        self.assertAlmostEqual(float(np.mean(norm_seq)), 0.0, places=5)
        self.assertAlmostEqual(float(np.std(norm_seq)), 1.0, places=5)

        # Invert normalization
        recovered = DataPreprocessor.denormalize_signal(norm_seq, params, method='standard')
        np.testing.assert_allclose(recovered, seq, rtol=1e-5)

if __name__ == '__main__':
    unittest.main()
