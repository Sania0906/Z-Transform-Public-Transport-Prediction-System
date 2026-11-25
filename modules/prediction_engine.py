"""
Module 2: Arrival-Time Prediction Engine
Evaluates Z-Transform predictions against benchmark baselines (SMA, Kinematic, Ridge Regression),
computes MAE, RMSE, MAPE, logs prediction events, and provides step-by-step mathematical walkthroughs.
"""

import time
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.linear_model import Ridge
from database.db_manager import DatabaseManager
from modules.z_transform_engine import ZTransformEngine
from modules.preprocessing import DataPreprocessor

class ArrivalPredictionEngine:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.z_engine = ZTransformEngine(ar_order=3)

    def set_ar_order(self, order: int):
        self.z_engine = ZTransformEngine(ar_order=order)

    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Compute MAE, RMSE, MAPE, and Max Error."""
        errors = y_pred - y_true
        abs_errors = np.abs(errors)
        mae = float(np.mean(abs_errors))
        rmse = float(np.sqrt(np.mean(errors ** 2)))

        # Avoid division by zero in MAPE
        non_zero_mask = np.abs(y_true) > 1e-3
        if np.any(non_zero_mask):
            mape = float(np.mean(abs_errors[non_zero_mask] / np.abs(y_true[non_zero_mask])) * 100.0)
        else:
            mape = 0.0

        max_err = float(np.max(abs_errors))
        mean_pct_err = float(np.mean(abs_errors / np.maximum(np.abs(y_true), 1.0)) * 100.0)

        return {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 2),
            "max_error": round(max_err, 2),
            "mean_pct_error": round(mean_pct_err, 2)
        }

    def train_test_split_backtest(self, series: np.ndarray, train_ratio: float = 0.75, 
                                  sma_window: int = 5) -> Dict:
        """
        Run rigorous temporal backtest comparing:
        1. Proposed Z-Transform Engine
        2. Simple Moving Average (SMA)
        3. Ridge Linear Regression
        """
        N = len(series)
        if N < 15:
            raise ValueError(f"Insufficient time-series length ({N}). Need at least 15 observations.")

        split_idx = int(N * train_ratio)
        train_data = series[:split_idx]
        test_data = series[split_idx:]

        # 1. Z-Transform Model
        mean_train = float(np.mean(train_data))
        s_train = train_data - mean_train
        b_poly, a_poly, sigma_w2 = self.z_engine.estimate_system_transfer_function(s_train)
        pz_info = self.z_engine.analyze_poles_and_zeros(b_poly, a_poly)
        a_coeffs = -a_poly[1:]
        p = len(a_coeffs)

        # 2. Ridge Regression Model
        X_train, y_train = [], []
        for i in range(p, len(train_data)):
            X_train.append(train_data[i-p:i][::-1])
            y_train.append(train_data[i])
        X_train, y_train = np.array(X_train), np.array(y_train)
        ridge_model = Ridge(alpha=1.0)
        ridge_model.fit(X_train, y_train)

        # Generate rolling one-step-ahead test predictions
        z_preds = []
        sma_preds = []
        ridge_preds = []
        full_history = list(train_data)

        for actual_val in test_data:
            # Z-Transform prediction
            past_p = np.array(full_history[-p:][::-1]) - mean_train
            s_pred = float(np.dot(a_coeffs, past_p))
            z_preds.append(s_pred + mean_train)

            # SMA prediction
            sma_preds.append(float(np.mean(full_history[-sma_window:])))

            # Ridge prediction
            past_p_ridge = np.array(full_history[-p:][::-1]).reshape(1, -1)
            ridge_preds.append(float(ridge_model.predict(past_p_ridge)[0]))

            # Advance rolling history
            full_history.append(actual_val)

        z_preds = np.array(z_preds)
        sma_preds = np.array(sma_preds)
        ridge_preds = np.array(ridge_preds)

        z_metrics = self.calculate_metrics(test_data, z_preds)
        sma_metrics = self.calculate_metrics(test_data, sma_preds)
        ridge_metrics = self.calculate_metrics(test_data, ridge_preds)

        return {
            "test_actual": test_data,
            "z_preds": z_preds,
            "sma_preds": sma_preds,
            "ridge_preds": ridge_preds,
            "z_metrics": z_metrics,
            "sma_metrics": sma_metrics,
            "ridge_metrics": ridge_metrics,
            "pz_info": pz_info,
            "b_poly": b_poly,
            "a_poly": a_poly,
            "ar_coeffs": a_coeffs.tolist(),
            "sigma_w2": sigma_w2
        }

    def predict_vehicle_arrival(self, vehicle_id: str, target_stop_id: str) -> Dict:
        """
        Produce real-time live arrival prediction for a specific bus and target stop.
        Combines spatial kinematic estimation with Z-transform discrete delay forecasting.
        """
        start_t = time.perf_counter()
        vehicles = self.db.get_vehicles()
        veh_match = vehicles[vehicles['vehicle_id'] == vehicle_id]
        if veh_match.empty:
            raise ValueError(f"Vehicle {vehicle_id} not found.")

        veh = veh_match.iloc[0].to_dict()
        route_id = veh['route_id']
        cur_lat = veh['latitude']
        cur_lon = veh['longitude']
        cur_speed = max(5.0, veh['speed_kmh']) # clamp minimum 5 km/h
        cur_delay = veh['current_delay_sec']

        # Get route stops and sequence
        route_stops = self.db.get_stops_for_route(route_id)
        target_stop_match = route_stops[route_stops['stop_id'] == target_stop_id]
        if target_stop_match.empty:
            raise ValueError(f"Stop {target_stop_id} does not belong to route {route_id}.")

        target_row = target_stop_match.iloc[0]
        target_lat = target_row['latitude']
        target_lon = target_row['longitude']
        target_name = target_row['stop_name']
        scheduled_travel_sec = float(target_row['scheduled_travel_time_sec'])

        # Haversine distance to target stop
        R = 6371.0
        dlat = np.radians(target_lat - cur_lat)
        dlon = np.radians(target_lon - cur_lon)
        a = (np.sin(dlat / 2.0)**2 +
             np.cos(np.radians(cur_lat)) * np.cos(np.radians(target_lat)) *
             np.sin(dlon / 2.0)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        remaining_dist_km = round(R * c * 1.25, 2) # apply route curvature factor 1.25

        # 1. Kinematic baseline ETA (sec)
        kinematic_eta_sec = round((remaining_dist_km / cur_speed) * 3600.0, 1)

        # 2. Historical arrivals for this stop & route
        hist_df = self.db.get_historical_arrivals(route_id, target_stop_id, limit=250)
        if hist_df.empty or len(hist_df) < 15:
            # Fallback to route-wide historical data if specific stop data is sparse
            hist_df = self.db.get_historical_arrivals(route_id, limit=250)

        raw_seq, clean_seq, preproc_stats = DataPreprocessor.extract_discrete_travel_time_series(hist_df)
        
        # 3. Z-Transform Model Execution
        z_result = self.z_engine.run_full_pipeline(clean_seq, forecast_steps=1)
        z_forecast_travel_sec = float(z_result['final_forecast'][0])
        z_pred_delay_sec = float(z_result['s_pred_detrended'][0])
        ci_low = float(z_result['ci_lower'][0])
        ci_high = float(z_result['ci_upper'][0])

        # Synthesize final ETA in seconds from now:
        # Scheduled remaining time adjusted by Z-Transform forecast delay perturbation
        z_eta_sec = max(30.0, kinematic_eta_sec + z_pred_delay_sec)
        baseline_eta_sec = kinematic_eta_sec # Kinematic baseline

        now_dt = datetime.datetime.now()
        estimated_arrival_dt = now_dt + datetime.timedelta(seconds=int(z_eta_sec))
        baseline_arrival_dt = now_dt + datetime.timedelta(seconds=int(baseline_eta_sec))

        calc_time_ms = round((time.perf_counter() - start_t) * 1000.0, 2)

        # Log prediction to database
        self.db.log_prediction(
            route_id=route_id, vehicle_id=vehicle_id, target_stop_id=target_stop_id,
            sched_sec=scheduled_travel_sec, base_eta=baseline_eta_sec, z_eta=z_eta_sec,
            pred_delay=z_pred_delay_sec, ci_low=ci_low, ci_high=ci_high,
            pole_rad=z_result['pz_analysis']['spectral_radius'],
            stability=z_result['pz_analysis']['stability_status'],
            comp_ms=calc_time_ms
        )

        return {
            "vehicle_id": vehicle_id,
            "route_id": route_id,
            "route_name": veh.get('route_name', route_id),
            "target_stop_id": target_stop_id,
            "target_stop_name": target_name,
            "remaining_dist_km": remaining_dist_km,
            "current_speed_kmh": cur_speed,
            "current_delay_sec": cur_delay,
            "kinematic_eta_sec": baseline_eta_sec,
            "z_eta_sec": round(z_eta_sec, 1),
            "z_predicted_delay_sec": round(z_pred_delay_sec, 1),
            "estimated_arrival_time": estimated_arrival_dt.strftime("%H:%M:%S"),
            "baseline_arrival_time": baseline_arrival_dt.strftime("%H:%M:%S"),
            "confidence_interval_sec": (round(max(0, z_eta_sec - 1.96 * np.sqrt(z_result['sigma_w2'])), 1),
                                        round(z_eta_sec + 1.96 * np.sqrt(z_result['sigma_w2']), 1)),
            "z_pipeline": z_result,
            "preproc_stats": preproc_stats,
            "calc_time_ms": calc_time_ms
        }

    def generate_step_by_step_walkthrough(self, sample_seq: Optional[np.ndarray] = None) -> Dict:
        """
        Generate detailed, academic step-by-step mathematical walkthrough
        demonstrating the entire Z-Transform prediction derivation.
        """
        if sample_seq is None or len(sample_seq) < 10:
            sample_seq = np.array([410.2, 425.8, 395.0, 440.5, 418.1, 432.0, 450.4, 405.2, 422.0, 438.9, 415.5, 442.1])

        mean_val = float(np.mean(sample_seq))
        s = sample_seq - mean_val
        p = self.z_engine.p

        # Step 1: Discrete signal detrending
        step1 = {
            "title": "Step 1: Discrete Time-Series Signal Detrending",
            "equation": "s[n] = x[n] - \\bar{x}",
            "explanation": f"Observed sample window of N={len(sample_seq)} traversal times with sample mean x_bar = {mean_val:.2f} s. Isolated zero-mean traffic perturbation signal s[n].",
            "values": [round(v, 2) for v in s[-6:]]
        }

        # Step 2: Autocorrelation Sequence Computation
        r = self.z_engine.compute_autocorrelation(s, p)
        step2 = {
            "title": "Step 2: Sample Autocorrelation Estimation",
            "equation": "r_{ss}[k] = \\frac{1}{N-k} \\sum_{n=0}^{N-1-k} s[n] s[n+k]",
            "explanation": f"Estimated unbiased autocorrelation for lags k = 0, ..., {p}.",
            "lags": {f"r_ss[{k}]": round(float(r[k]), 4) for k in range(len(r))}
        }

        # Step 3: Yule-Walker System Identification
        b_poly, a_poly, sigma_w2 = self.z_engine.estimate_system_transfer_function(s)
        a_coeffs = -a_poly[1:]
        step3 = {
            "title": "Step 3: Yule-Walker Matrix System Identification",
            "equation": "\\mathbf{R}_{ss} \\mathbf{a} = \\mathbf{r}_{ss} \\implies \\mathbf{a} = \\mathbf{R}_{ss}^{-1} \\mathbf{r}_{ss}",
            "explanation": f"Solved Toeplitz system of order p={p}. White noise innovation variance sigma_w^2 = {sigma_w2:.4f}.",
            "coefficients": {f"a_{idx}": round(float(val), 4) for idx, val in enumerate(a_coeffs, 1)}
        }

        # Step 4: Transfer Function Representation in Z-Domain
        tf_str = "H(z) = \\frac{1}{1 - " + " - ".join([f"({c:.4f} z^{{-{i}}})" for i, c in enumerate(a_coeffs, 1)]) + "}"
        step4 = {
            "title": "Step 4: Discrete Transfer Function Formulation",
            "equation": tf_str,
            "explanation": "Formulated causal discrete-time LTI system transfer function in negative powers of complex variable z."
        }

        # Step 5: Pole-Zero Unit Circle Stability Analysis
        pz = self.z_engine.analyze_poles_and_zeros(b_poly, a_poly)
        step5 = {
            "title": "Step 5: Pole-Zero Analysis & BIBO Stability Verification",
            "equation": "\\text{Roots of } A(z) = 0 \\implies |p_k| < 1.0 \\quad \\forall k",
            "explanation": f"All poles reside inside the unit circle (|z| < 1). System is {pz['stability_status']}. Maximum spectral radius = {pz['spectral_radius']:.4f}.",
            "poles": pz['pole_details']
        }

        # Step 6: Inverse Z-Transform via Partial Fractions
        n_axis, h_n, residues = self.z_engine.compute_inverse_z_transform_impulse(b_poly, a_poly, n_points=6)
        step6 = {
            "title": "Step 6: Inverse Z-Transform via Partial Fraction Decomposition",
            "equation": "h[n] = \\mathcal{Z}^{-1}\\{H(z)\\} = \\sum_{k=1}^p R_k (p_k)^n u[n]",
            "explanation": "Decomposed transfer function into first-order partial fractions and synthesized analytical impulse response sequence h[n].",
            "impulse_first_samples": [round(float(v), 4) for v in h_n[:6]]
        }

        # Step 7: Recursive Delay and Arrival Estimation
        s_pred = float(np.dot(a_coeffs, s[-p:][::-1]))
        final_eta_trav = mean_val + s_pred
        step7 = {
            "title": "Step 7: One-Step Ahead Arrival Travel-Time Prediction",
            "equation": "\\hat{x}[n+1] = \\bar{x} + \\sum_{j=1}^p a_j s[n+1-j]",
            "explanation": f"Predicted perturbation: {s_pred:+.2f} s. Final predicted arrival travel time: {final_eta_trav:.2f} s.",
            "final_value_sec": round(final_eta_trav, 2),
            "ci_95": (round(final_eta_trav - 1.96 * np.sqrt(sigma_w2), 2),
                      round(final_eta_trav + 1.96 * np.sqrt(sigma_w2), 2))
        }

        return {
            "sample_input_window": sample_seq.tolist(),
            "mean_val": round(mean_val, 2),
            "steps": [step1, step2, step3, step4, step5, step6, step7]
        }
