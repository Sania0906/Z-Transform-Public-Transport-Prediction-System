"""
Module 3: Intelligent Passenger Dashboard Logic
Handles passenger route/stop searching, vehicle selection, live ETA countdown computation,
historical pattern analysis, delay notifications, and interactive Plotly visualizations.
"""

import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple
from database.db_manager import DatabaseManager
from modules.data_acquisition import TransitDataAcquisition
from modules.prediction_engine import ArrivalPredictionEngine

class PassengerDashboardService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.acq = TransitDataAcquisition(self.db)
        self.pred_engine = ArrivalPredictionEngine(self.db)

    def get_search_routes(self) -> pd.DataFrame:
        """Fetch all available transit routes."""
        return self.acq.get_routes()

    def get_search_stops(self, route_id: Optional[str] = None) -> pd.DataFrame:
        """Fetch stops for specific route or system-wide."""
        return self.acq.get_stops(route_id)

    def get_route_vehicles(self, route_id: str) -> pd.DataFrame:
        """Fetch vehicles currently operating on the selected route."""
        return self.acq.get_active_vehicles(route_id)

    def compute_passenger_eta(self, vehicle_id: str, target_stop_id: str) -> Dict:
        """Generate high-precision arrival estimate and countdown metrics."""
        pred_data = self.pred_engine.predict_vehicle_arrival(vehicle_id, target_stop_id)
        z_eta_sec = pred_data['z_eta_sec']

        minutes = int(z_eta_sec // 60)
        seconds = int(z_eta_sec % 60)

        pred_data['countdown_minutes'] = minutes
        pred_data['countdown_seconds'] = seconds
        return pred_data

    def generate_passenger_advisories(self, pred_data: Dict, weather: str = "Clear", congestion_lvl: int = 3) -> List[Dict]:
        """Generate passenger-friendly notifications and service alerts."""
        advisories = []
        delay = pred_data['z_predicted_delay_sec']

        # Service On-time / Delay alert
        if delay > 240.0:
            advisories.append({
                "title": "Severe Delay Advisory",
                "message": f"Bus {pred_data['vehicle_id']} is delayed by approximately {delay/60:.1f} minutes due to heavy corridor traffic. Please plan accordingly.",
                "level": "danger"
            })
        elif delay > 60.0:
            advisories.append({
                "title": "Minor Service Delay",
                "message": f"Expected arrival delayed by {delay/60:.1f} minutes due to traffic signals and boarding dwell times.",
                "level": "warning"
            })
        else:
            advisories.append({
                "title": "On-Schedule Operation",
                "message": f"Service on {pred_data['route_name']} is operating on schedule within normal ±45-second variance.",
                "level": "success"
            })

        # Weather / Congestion advisory
        if weather in ["Rain", "Light Rain"]:
            advisories.append({
                "title": "Inclement Weather Notice",
                "message": "Wet road conditions observed. Slower vehicle deceleration enforced for passenger safety.",
                "level": "info"
            })
        elif congestion_lvl >= 4:
            advisories.append({
                "title": "Peak Congestion Zone",
                "message": "High passenger volume and dense arterial traffic along target segment.",
                "level": "warning"
            })

        return advisories

    def create_historical_delay_chart(self, route_id: str, stop_id: str) -> go.Figure:
        """Plot historical delay patterns across different times of day."""
        hist_df = self.db.get_historical_arrivals(route_id, stop_id, limit=200)
        if hist_df.empty:
            hist_df = self.db.get_historical_arrivals(route_id, limit=200)

        fig = go.Figure()

        if not hist_df.empty and 'time_of_day' in hist_df.columns:
            # Group by time_of_day
            time_order = ['morning_peak', 'midday', 'evening_peak', 'night']
            colors = {
                'morning_peak': '#EF476F',
                'midday': '#00F5D4',
                'evening_peak': '#FFB703',
                'night': '#118AB2'
            }

            for t_cat in time_order:
                sub = hist_df[hist_df['time_of_day'] == t_cat]
                if not sub.empty:
                    fig.add_trace(go.Box(
                        y=sub['delay_seconds'],
                        name=t_cat.replace('_', ' ').title(),
                        marker_color=colors.get(t_cat, '#00B4D8'),
                        boxpoints='outliers',
                        jitter=0.3
                    ))

        fig.update_layout(
            title="Historical Arrival Delay Distribution by Time-of-Day (seconds)",
            template="plotly_dark",
            paper_bgcolor="rgba(10, 15, 29, 0.0)",
            plot_bgcolor="rgba(19, 27, 46, 0.6)",
            yaxis_title="Delay (seconds)",
            xaxis_title="Operating Period",
            font=dict(color="#CBD5E1", size=12),
            margin=dict(l=40, r=40, t=50, b=40),
            showlegend=False
        )
        return fig

    def create_actual_vs_predicted_chart(self, backtest_results: Dict) -> go.Figure:
        """Plot actual observations versus Z-Transform predictions and baselines."""
        actual = backtest_results['test_actual']
        z_pred = backtest_results['z_preds']
        sma_pred = backtest_results['sma_preds']
        time_index = np.arange(len(actual))

        fig = go.Figure()

        # Actual trace
        fig.add_trace(go.Scatter(
            x=time_index, y=actual,
            mode='lines+markers',
            name='Actual Arrival Travel Time',
            line=dict(color='#FFFFFF', width=2.5),
            marker=dict(size=6, color='#FFFFFF')
        ))

        # Z-Transform prediction trace
        fig.add_trace(go.Scatter(
            x=time_index, y=z_pred,
            mode='lines+markers',
            name=f"Z-Transform Model (MAE: {backtest_results['z_metrics']['mae']}s)",
            line=dict(color='#00F5D4', width=3),
            marker=dict(size=6, symbol='diamond', color='#00F5D4')
        ))

        # Baseline SMA trace
        fig.add_trace(go.Scatter(
            x=time_index, y=sma_pred,
            mode='lines',
            name=f"Baseline SMA (MAE: {backtest_results['sma_metrics']['mae']}s)",
            line=dict(color='#FFB703', width=2, dash='dash')
        ))

        fig.update_layout(
            title="Comparative Model Performance: Actual vs. Predicted Travel Times (Test Horizon)",
            template="plotly_dark",
            paper_bgcolor="rgba(10, 15, 29, 0.0)",
            plot_bgcolor="rgba(19, 27, 46, 0.6)",
            xaxis_title="Observation Index (Discrete Epoch n)",
            yaxis_title="Travel Time (seconds)",
            font=dict(color="#CBD5E1", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig

    def create_z_plane_pole_zero_chart(self, pz_analysis: Dict) -> go.Figure:
        """Visualize poles and zeros on the complex Z-plane unit circle."""
        fig = go.Figure()

        # Draw Unit Circle (|z| = 1)
        theta = np.linspace(0, 2 * np.pi, 200)
        unit_circle_x = np.cos(theta)
        unit_circle_y = np.sin(theta)

        fig.add_trace(go.Scatter(
            x=unit_circle_x, y=unit_circle_y,
            mode='lines',
            name='Unit Circle (|z| = 1.0)',
            line=dict(color='#00E5FF', width=2, dash='dot')
        ))

        # Unit disk interior shading
        fig.add_trace(go.Scatter(
            x=unit_circle_x, y=unit_circle_y,
            fill='toself',
            fillcolor='rgba(0, 180, 216, 0.08)',
            mode='none',
            name='ROC Stable Region',
            hoverinfo='skip'
        ))

        # Plot Poles ('x')
        poles = pz_analysis['poles']
        if len(poles) > 0:
            fig.add_trace(go.Scatter(
                x=[p.real for p in poles],
                y=[p.imag for p in poles],
                mode='markers+text',
                name='System Poles (Roots of A(z))',
                marker=dict(symbol='x', size=13, color='#EF476F', line=dict(width=3, color='#EF476F')),
                text=[f"p{idx+1}: |z|={np.abs(p):.3f}" for idx, p in enumerate(poles)],
                textposition="top right",
                textfont=dict(color="#FFA69E", size=11)
            ))

        # Plot Zeros ('o')
        zeros = pz_analysis['zeros']
        if len(zeros) > 0:
            fig.add_trace(go.Scatter(
                x=[z.real for z in zeros],
                y=[z.imag for z in zeros],
                mode='markers',
                name='System Zeros (Roots of B(z))',
                marker=dict(symbol='circle-open', size=11, color='#00F5D4', line=dict(width=2))
            ))

        # Axis crosshairs
        fig.add_hline(y=0, line_dash="dash", line_color="rgba(148, 163, 184, 0.3)", line_width=1)
        fig.add_vline(x=0, line_dash="dash", line_color="rgba(148, 163, 184, 0.3)", line_width=1)

        fig.update_layout(
            title=f"Complex Z-Plane Pole-Zero Constellation (Max |p| = {pz_analysis['spectral_radius']:.4f})",
            template="plotly_dark",
            paper_bgcolor="rgba(10, 15, 29, 0.0)",
            plot_bgcolor="rgba(19, 27, 46, 0.6)",
            xaxis_title="Real Axis Re{z}",
            yaxis_title="Imaginary Axis Im{z}",
            xaxis=dict(range=[-1.5, 1.5], constrain="domain"),
            yaxis=dict(range=[-1.5, 1.5], scaleanchor="x", scaleratio=1),
            font=dict(color="#CBD5E1", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40),
            width=500,
            height=480
        )
        return fig
