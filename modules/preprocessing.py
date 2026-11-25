"""
Module 1: Preprocessing & GPS Signal Filtering
Implements discrete signal extraction, missing-value imputation, 2D Kalman filter,
Hampel outlier rejection, and statistical normalization for Z-Transform analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import signal

class KalmanGPSFilter:
    """
    Constant-Velocity 2D State-Space Kalman Filter for GPS Trajectory Denoising.
    State vector: [x, y, vx, vy]^T
    Measurement: [z_x, z_y]^T
    """
    def __init__(self, dt: float = 1.0, process_noise_std: float = 0.05, measurement_noise_std: float = 0.8):
        self.dt = dt
        # State Transition Matrix F
        self.F = np.array([
            [1.0, 0.0, dt,  0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        # Measurement Matrix H
        self.H = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ])
        # Process Noise Covariance Q
        q = process_noise_std ** 2
        self.Q = np.array([
            [0.25*dt**4, 0.0,        0.5*dt**3,  0.0],
            [0.0,        0.25*dt**4, 0.0,        0.5*dt**3],
            [0.5*dt**3,  0.0,        dt**2,      0.0],
            [0.0,        0.5*dt**3,  0.0,        dt**2]
        ]) * q
        # Measurement Noise Covariance R
        r = measurement_noise_std ** 2
        self.R = np.eye(2) * r
        # State Estimate x and Error Covariance P
        self.x = np.zeros(4)
        self.P = np.eye(4) * 10.0
        self.initialized = False

    def reset(self, init_lat: float, init_lon: float):
        self.x = np.array([init_lat, init_lon, 0.0, 0.0])
        self.P = np.eye(4) * 1.0
        self.initialized = True

    def update(self, z_lat: float, z_lon: float) -> Tuple[float, float, float, float]:
        """Predict and update with incoming GPS measurement."""
        if not self.initialized:
            self.reset(z_lat, z_lon)
            return z_lat, z_lon, 0.0, 0.0

        # Prediction step
        x_pred = self.F @ self.x
        P_pred = self.F @ self.P @ self.F.T + self.Q

        # Measurement residual (innovation)
        z = np.array([z_lat, z_lon])
        y = z - self.H @ x_pred

        # Innovation covariance S
        S = self.H @ P_pred @ self.H.T + self.R
        # Kalman Gain K
        K = P_pred @ self.H.T @ np.linalg.inv(S)

        # Updated state estimate
        self.x = x_pred + K @ y
        # Updated covariance estimate
        I = np.eye(4)
        self.P = (I - K @ self.H) @ P_pred

        lat_est = float(self.x[0])
        lon_est = float(self.x[1])
        vx_est = float(self.x[2])
        vy_est = float(self.x[3])
        return lat_est, lon_est, vx_est, vy_est

    def filter_trajectory(self, lats: np.ndarray, lons: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Batch filter an entire coordinate sequence."""
        if len(lats) == 0:
            return np.array([]), np.array([])
        filtered_lats = np.zeros(len(lats))
        filtered_lons = np.zeros(len(lons))
        self.reset(lats[0], lons[0])

        for i in range(len(lats)):
            flat, flon, _, _ = self.update(lats[i], lons[i])
            filtered_lats[i] = flat
            filtered_lons[i] = flon
        return filtered_lats, filtered_lons


class DataPreprocessor:
    """Comprehensive preprocessing, cleaning, imputation, and normalization."""
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, target_columns: List[str]) -> pd.DataFrame:
        """
        Impute missing values using forward-fill followed by backward-fill,
        and fallback to column median for unbroken time series continuity.
        """
        df_clean = df.copy()
        for col in target_columns:
            if col in df_clean.columns:
                # Forward-fill then backward-fill
                df_clean[col] = df_clean[col].ffill().bfill()
                # If entire column was null, fallback to 0.0
                if df_clean[col].isnull().any():
                    df_clean[col] = df_clean[col].fillna(0.0)
        return df_clean

    @staticmethod
    def hampel_filter(data: np.ndarray, window_size: int = 5, n_sigmas: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Hampel identifier for robust outlier replacement in discrete travel time signals.
        Replaces outliers with the local rolling median.
        """
        n = len(data)
        filtered_data = np.copy(data)
        outlier_indices = []
        k = 1.4826 # scale factor for Gaussian distribution

        for i in range(n):
            start = max(0, i - window_size)
            end = min(n, i + window_size + 1)
            window = data[start:end]
            median = np.median(window)
            mad = k * np.median(np.abs(window - median))

            if mad > 1e-6 and np.abs(data[i] - median) > n_sigmas * mad:
                filtered_data[i] = median
                outlier_indices.append(i)

        return filtered_data, np.array(outlier_indices)

    @staticmethod
    def calculate_snr(clean_signal: np.ndarray, noisy_signal: np.ndarray) -> float:
        """Calculate Signal-to-Noise Ratio (SNR) in decibels (dB)."""
        signal_power = np.mean(clean_signal ** 2)
        noise = noisy_signal - clean_signal
        noise_power = np.mean(noise ** 2)
        if noise_power < 1e-12:
            return 60.0 # High quality threshold
        return float(10.0 * np.log10(signal_power / noise_power))

    @staticmethod
    def normalize_signal(signal_seq: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Normalize discrete signal sequence.
        Methods:
        - 'standard': Zero-mean, unit-variance (Z-score)
        - 'minmax': Scaled to [0, 1] range
        - 'detrend': Mean-centered detrending (s[n] = x[n] - mean)
        """
        params = {}
        if len(signal_seq) == 0:
            return signal_seq, params

        if method == 'standard':
            mean = float(np.mean(signal_seq))
            std = float(np.std(signal_seq))
            if std < 1e-6:
                std = 1.0
            norm_seq = (signal_seq - mean) / std
            params = {'mean': mean, 'std': std}

        elif method == 'minmax':
            min_val = float(np.min(signal_seq))
            max_val = float(np.max(signal_seq))
            denom = (max_val - min_val) if (max_val - min_val) > 1e-6 else 1.0
            norm_seq = (signal_seq - min_val) / denom
            params = {'min': min_val, 'max': max_val}

        elif method == 'detrend':
            mean = float(np.mean(signal_seq))
            norm_seq = signal_seq - mean
            params = {'mean': mean}
        else:
            norm_seq = signal_seq

        return norm_seq, params

    @staticmethod
    def denormalize_signal(norm_seq: np.ndarray, params: Dict[str, float], method: str = 'standard') -> np.ndarray:
        """Invert normalization back to original physical units (seconds)."""
        if method == 'standard':
            return norm_seq * params.get('std', 1.0) + params.get('mean', 0.0)
        elif method == 'minmax':
            return norm_seq * (params.get('max', 1.0) - params.get('min', 0.0)) + params.get('min', 0.0)
        elif method == 'detrend':
            return norm_seq + params.get('mean', 0.0)
        return norm_seq

    @classmethod
    def extract_discrete_travel_time_series(cls, df_hist: pd.DataFrame, 
                                            target_col: str = 'actual_travel_time_sec') -> Tuple[np.ndarray, np.ndarray, Dict]:
        """
        Extract clean discrete-time sequence x[n] from historical arrival records,
        applying missing-value imputation, outlier rejection, and detrending.
        Returns:
            raw_seq: original observed sequence
            clean_seq: outlier-filtered, imputed sequence
            stats: summary dictionary with SNR, outlier count, mean, std
        """
        if df_hist.empty or target_col not in df_hist.columns:
            return np.array([]), np.array([]), {}

        # Impute missing values
        clean_df = cls.handle_missing_values(df_hist, [target_col, 'delay_seconds', 'segment_speed_kmh'])
        raw_seq = clean_df[target_col].to_numpy(dtype=float)

        # Hampel outlier filtering
        clean_seq, outliers = cls.hampel_filter(raw_seq, window_size=5, n_sigmas=2.8)

        # SNR calculation
        snr_val = cls.calculate_snr(clean_seq, raw_seq)

        stats = {
            'n_samples': len(raw_seq),
            'n_outliers_rejected': len(outliers),
            'raw_mean': float(np.mean(raw_seq)),
            'raw_std': float(np.std(raw_seq)),
            'clean_mean': float(np.mean(clean_seq)),
            'clean_std': float(np.std(clean_seq)),
            'snr_db': round(snr_val, 2)
        }
        return raw_seq, clean_seq, stats
