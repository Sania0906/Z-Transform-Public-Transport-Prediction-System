"""
Module 2: Z-Transform Mathematical Engine
Performs Discrete-Time Signal Processing, Z-Transform transfer function modeling H(z),
Yule-Walker parameter estimation, Pole-Zero unit-circle stability analysis,
and analytical Inverse Z-Transform via Partial Fraction Expansion.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import signal

class ZTransformEngine:
    def __init__(self, ar_order: int = 3):
        """
        Initialize the Z-Transform Engine.
        ar_order (p): Order of the discrete transfer function denominator polynomial A(z).
        """
        self.p = max(1, min(6, ar_order)) # AR order between 1 and 6

    def compute_autocorrelation(self, s: np.ndarray, max_lag: int) -> np.ndarray:
        """
        Compute sample unbiased autocorrelation sequence r_ss[k] for lags 0 to max_lag.
        r_ss[k] = (1 / (N - k)) * sum_{n=0}^{N-1-k} s[n] * s[n+k]
        """
        N = len(s)
        r = np.zeros(max_lag + 1)
        for k in range(max_lag + 1):
            if N - k > 0:
                r[k] = np.sum(s[:N - k] * s[k:]) / (N - k)
            else:
                r[k] = 0.0
        return r

    def estimate_system_transfer_function(self, s: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Estimate AR system coefficients a_k via Yule-Walker Equations:
        R_ss * a = r_vector
        Returns:
            b_coeffs: Numerator coefficients B(z) = [1.0]
            a_coeffs: Denominator coefficients A(z) = [1.0, -a_1, -a_2, ..., -a_p]
            sigma_w2: White noise innovation variance
        """
        N = len(s)
        if N <= self.p:
            # Fallback for very short sequences
            return np.array([1.0]), np.array([1.0, -0.5]), float(np.var(s) if N > 1 else 1.0)

        # Autocorrelation vector up to lag p
        r = self.compute_autocorrelation(s, self.p)
        r0 = r[0]
        if r0 < 1e-9:
            return np.array([1.0]), np.array([1.0] + [0.0]*self.p), 1.0

        # Construct Toeplitz Autocorrelation Matrix
        R_matrix = np.zeros((self.p, self.p))
        for i in range(self.p):
            for j in range(self.p):
                R_matrix[i, j] = r[abs(i - j)]

        # Regularization for numerical conditioning
        R_matrix += np.eye(self.p) * 1e-6
        r_vec = r[1:self.p + 1]

        try:
            a_hat = np.linalg.solve(R_matrix, r_vec)
        except np.linalg.LinAlgError:
            a_hat = np.linalg.pinv(R_matrix) @ r_vec

        # A(z) = 1 - a1*z^-1 - ... - ap*z^-p
        # Polynomial representation in powers of z^-1: [1.0, -a_1, -a_2, ..., -a_p]
        a_poly = np.concatenate(([1.0], -a_hat))
        b_poly = np.array([1.0])

        # Residual innovation variance: sigma_w^2 = r[0] - a_hat^T * r_vec
        sigma_w2 = max(1e-4, float(r0 - np.dot(a_hat, r_vec)))

        return b_poly, a_poly, sigma_w2

    def analyze_poles_and_zeros(self, b_poly: np.ndarray, a_poly: np.ndarray) -> Dict:
        """
        Compute system poles and zeros, radii, damping ratios, and verify BIBO stability.
        Poles are roots of A(z^-1) = 0 -> roots of z^p - a_1*z^{p-1} - ... - a_p = 0.
        """
        # Roots of denominator polynomial in powers of z (highest degree first)
        # a_poly is [1.0, -a_1, -a_2, ..., -a_p]
        poles = np.roots(a_poly)
        zeros = np.roots(b_poly) if len(b_poly) > 1 else np.array([])

        pole_radii = np.abs(poles)
        max_radius = float(np.max(pole_radii)) if len(pole_radii) > 0 else 0.0
        is_stable = bool(max_radius < 1.0) # Strictly inside unit circle

        # Formulate pole details
        pole_details = []
        for idx, p in enumerate(poles):
            r = float(np.abs(p))
            theta = float(np.angle(p)) # radians
            omega_deg = float(np.degrees(theta))
            pole_details.append({
                "index": idx + 1,
                "real": round(float(p.real), 4),
                "imag": round(float(p.imag), 4),
                "magnitude": round(r, 4),
                "angle_deg": round(omega_deg, 2),
                "is_stable": r < 1.0
            })

        return {
            "poles": poles,
            "zeros": zeros,
            "pole_details": pole_details,
            "spectral_radius": round(max_radius, 4),
            "is_bibo_stable": is_stable,
            "stability_status": "BIBO Stable (Poles inside unit circle)" if is_stable else "Unstable / Marginal (Outside unit circle)"
        }

    def compute_inverse_z_transform_impulse(self, b_poly: np.ndarray, a_poly: np.ndarray, 
                                            n_points: int = 25) -> Tuple[np.ndarray, np.ndarray, List[Dict]]:
        """
        Compute the Inverse Z-Transform h[n] = Z^-1 { H(z) } via Partial Fraction Expansion:
        H(z) = sum_{k=1}^p [ R_k / (1 - p_k * z^-1) ]
        -> h[n] = sum_{k=1}^p R_k * (p_k)^n * u[n]
        """
        # scipy.signal.residuez decomposes B(z)/A(z) into partial fractions:
        # H(z) = sum_k ( r[k] / (1 - p[k]*z^-1) ) + direct terms k
        try:
            r, p, k = signal.residuez(b_poly, a_poly)
        except Exception:
            # Fallback to direct IIR impulse response
            impulse = np.zeros(n_points)
            impulse[0] = 1.0
            h_n = signal.lfilter(b_poly, a_poly, impulse)
            return np.arange(n_points), h_n, []

        n_axis = np.arange(n_points)
        h_n = np.zeros(n_points, dtype=float)

        # Synthesize h[n] = sum_k r_k * (p_k)^n
        for idx in range(len(r)):
            term = r[idx] * (p[idx] ** n_axis)
            h_n += term.real

        residue_details = []
        for idx in range(len(r)):
            residue_details.append({
                "pole": f"{p[idx].real:.3f} + {p[idx].imag:.3f}j",
                "residue_mag": round(float(np.abs(r[idx])), 4),
                "residue_phase_deg": round(float(np.degrees(np.angle(r[idx]))), 2)
            })

        return n_axis, h_n, residue_details

    def compute_frequency_response(self, b_poly: np.ndarray, a_poly: np.ndarray, 
                                   worN: int = 256) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Evaluate Z-Transform on the unit circle z = e^{j*omega}:
        H(e^{j*omega}) = B(e^{j*omega}) / A(e^{j*omega})
        Returns:
            w: normalized digital frequency [0, pi] rad/sample
            mag_db: magnitude response 20*log10(|H|)
            phase_deg: phase response in degrees
        """
        w, h = signal.freqz(b_poly, a_poly, worN=worN)
        mag_db = 20.0 * np.log10(np.maximum(np.abs(h), 1e-6))
        phase_deg = np.degrees(np.angle(h))
        return w, mag_db, phase_deg

    def predict_sequence(self, s: np.ndarray, a_poly: np.ndarray, 
                         forecast_steps: int = 1) -> np.ndarray:
        """
        Perform recursive multi-step forecasting using discrete difference equation:
        hat{s}[n+m] = sum_{j=1}^p a_j * s[n+m-j]
        """
        # a_poly is [1.0, -a1, -a2, ..., -ap] -> AR coefficients are -a_poly[1:]
        a_coeffs = -a_poly[1:]
        p = len(a_coeffs)
        history = list(s.copy())

        forecasts = []
        for _ in range(forecast_steps):
            if len(history) < p:
                pred = float(np.mean(history)) if len(history) > 0 else 0.0
            else:
                past_window = np.array(history[-p:][::-1])
                pred = float(np.dot(a_coeffs, past_window))
            forecasts.append(pred)
            history.append(pred)

        return np.array(forecasts)

    def run_full_pipeline(self, signal_seq: np.ndarray, forecast_steps: int = 1) -> Dict:
        """
        Execute complete mathematical Z-Transform pipeline on input discrete sequence.
        Returns all polynomials, poles, zeros, impulse response, forecast, and equations.
        """
        if len(signal_seq) == 0:
            raise ValueError("Input signal sequence is empty.")

        # Detrend: s[n] = x[n] - mean
        mean_val = float(np.mean(signal_seq))
        s_detrended = signal_seq - mean_val

        # Step 1: System Identification
        b_poly, a_poly, sigma_w2 = self.estimate_system_transfer_function(s_detrended)

        # Step 2: Pole-Zero Stability Analysis
        pz_analysis = self.analyze_poles_and_zeros(b_poly, a_poly)

        # Step 3: Inverse Z-Transform via Partial Fractions
        n_axis, h_n, residue_details = self.compute_inverse_z_transform_impulse(b_poly, a_poly, n_points=25)

        # Step 4: Frequency Response on Unit Circle
        w_freq, mag_db, phase_deg = self.compute_frequency_response(b_poly, a_poly)

        # Step 5: Multi-Step Prediction
        s_pred_detrended = self.predict_sequence(s_detrended, a_poly, forecast_steps=forecast_steps)
        final_forecast = s_pred_detrended + mean_val

        # Step 6: Analytical Forecast Error Variance
        # Var[e(m)] = sigma_w^2 * sum_{j=0}^{m-1} h[j]^2
        ci_lower = []
        ci_upper = []
        cum_h_sq = 0.0
        for m in range(forecast_steps):
            if m < len(h_n):
                cum_h_sq += h_n[m] ** 2
            else:
                cum_h_sq += 0.0
            var_m = sigma_w2 * max(1.0, cum_h_sq)
            std_m = np.sqrt(var_m)
            ci_lower.append(final_forecast[m] - 1.96 * std_m)
            ci_upper.append(final_forecast[m] + 1.96 * std_m)

        # Formulate formatted mathematical equation strings
        ar_terms = []
        for idx, a_val in enumerate(-a_poly[1:], start=1):
            sign = "+" if a_val >= 0 and idx > 1 else ""
            ar_terms.append(f"{sign}{a_val:.4f} z^{{-{idx}}}")
        denom_str = "1.0 - " + " - ".join([f"{a_val:.4f}z^{{-{idx}}}" if a_val >= 0 else f"({a_val:.4f})z^{{-{idx}}}" for idx, a_val in enumerate(-a_poly[1:], start=1)])

        tf_equation = f"H(z) = \\frac{{1}}{{1 - ({' + '.join(ar_terms)})}}"

        return {
            "mean_val": mean_val,
            "b_poly": b_poly,
            "a_poly": a_poly,
            "ar_coeffs": (-a_poly[1:]).tolist(),
            "sigma_w2": sigma_w2,
            "pz_analysis": pz_analysis,
            "n_axis": n_axis,
            "impulse_response": h_n,
            "residue_details": residue_details,
            "w_freq": w_freq,
            "mag_db": mag_db,
            "phase_deg": phase_deg,
            "forecast_steps": forecast_steps,
            "s_pred_detrended": s_pred_detrended,
            "final_forecast": final_forecast,
            "ci_lower": np.array(ci_lower),
            "ci_upper": np.array(ci_upper),
            "tf_equation": tf_equation
        }
