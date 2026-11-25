"""
Unit & Integration Tests for Prediction Engine and Passenger Dashboards.
Tests model comparisons, MAE/RMSE calculations, vehicle prediction, and walkthrough generation.
"""

import unittest
import numpy as np
from modules.prediction_engine import ArrivalPredictionEngine
from modules.passenger_dashboard import PassengerDashboardService

class TestPredictionEngine(unittest.TestCase):
    def setUp(self):
        self.pred_engine = ArrivalPredictionEngine()
        self.dash_service = PassengerDashboardService()
        np.random.seed(42)
        # 40 historical samples
        self.sample_series = np.random.normal(420.0, 30.0, 40)

    def test_metrics_calculation(self):
        y_true = np.array([100.0, 200.0, 300.0])
        y_pred = np.array([110.0, 190.0, 300.0])
        metrics = self.pred_engine.calculate_metrics(y_true, y_pred)
        self.assertAlmostEqual(metrics['mae'], (10 + 10 + 0) / 3.0, places=2)
        self.assertAlmostEqual(metrics['rmse'], np.sqrt((100 + 100 + 0) / 3.0), places=2)
        self.assertGreater(metrics['mape'], 0.0)

    def test_backtest_execution(self):
        backtest = self.pred_engine.train_test_split_backtest(self.sample_series, train_ratio=0.75, sma_window=3)
        self.assertIn("z_metrics", backtest)
        self.assertIn("sma_metrics", backtest)
        self.assertIn("ridge_metrics", backtest)
        self.assertGreater(len(backtest["z_preds"]), 0)
        self.assertEqual(len(backtest["z_preds"]), len(backtest["test_actual"]))

    def test_predict_vehicle_arrival(self):
        # Predict arrival for BUS-1011 to S-104
        pred_res = self.pred_engine.predict_vehicle_arrival('BUS-1011', 'S-104')
        self.assertIn("z_eta_sec", pred_res)
        self.assertGreater(pred_res["z_eta_sec"], 0)
        self.assertIn("estimated_arrival_time", pred_res)
        self.assertIn("confidence_interval_sec", pred_res)
        self.assertLessEqual(pred_res["confidence_interval_sec"][0], pred_res["z_eta_sec"])
        self.assertGreaterEqual(pred_res["confidence_interval_sec"][1], pred_res["z_eta_sec"])

    def test_walkthrough_generation(self):
        walk = self.pred_engine.generate_step_by_step_walkthrough()
        self.assertIn("steps", walk)
        self.assertEqual(len(walk["steps"]), 7, "Must contain exactly 7 sequential calculation steps.")
        for step in walk["steps"]:
            self.assertIn("title", step)
            self.assertIn("equation", step)
            self.assertIn("explanation", step)

    def test_passenger_countdown_service(self):
        eta_info = self.dash_service.compute_passenger_eta('BUS-1011', 'S-105')
        self.assertIn("countdown_minutes", eta_info)
        self.assertIn("countdown_seconds", eta_info)
        self.assertGreaterEqual(eta_info["countdown_minutes"], 0)
        self.assertGreaterEqual(eta_info["countdown_seconds"], 0)
        self.assertLess(eta_info["countdown_seconds"], 60)

if __name__ == '__main__':
    unittest.main()
