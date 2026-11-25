"""
Database Manager for Z-Transform Public Transport Arrival Time Prediction System.
Handles SQLite operations, table initialization, and fast analytical queries.
"""

import sqlite3
import os
import pandas as pd
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "transport.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables from schema.sql"""
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            with self.get_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()

    def get_all_routes(self) -> pd.DataFrame:
        query = "SELECT * FROM routes ORDER BY route_id"
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def get_route_by_id(self, route_id: str) -> Optional[Dict]:
        query = "SELECT * FROM routes WHERE route_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (route_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_stops_for_route(self, route_id: str) -> pd.DataFrame:
        query = """
            SELECT rs.stop_sequence, s.stop_id, s.stop_name, s.latitude, s.longitude,
                   s.shelter_type, s.transfer_routes, rs.distance_from_start_km,
                   rs.scheduled_travel_time_sec
            FROM route_stops rs
            JOIN stops s ON rs.stop_id = s.stop_id
            WHERE rs.route_id = ?
            ORDER BY rs.stop_sequence ASC
        """
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=(route_id,))

    def get_all_stops(self) -> pd.DataFrame:
        query = "SELECT * FROM stops ORDER BY stop_name"
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def get_vehicles(self, route_id: Optional[str] = None) -> pd.DataFrame:
        if route_id:
            query = """
                SELECT v.*, r.route_name, r.route_color, r.route_short_name
                FROM vehicles v
                JOIN routes r ON v.route_id = r.route_id
                WHERE v.route_id = ?
                ORDER BY v.vehicle_id
            """
            params = (route_id,)
        else:
            query = """
                SELECT v.*, r.route_name, r.route_color, r.route_short_name
                FROM vehicles v
                JOIN routes r ON v.route_id = r.route_id
                ORDER BY v.vehicle_id
            """
            params = ()
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)

    def update_vehicle_position(self, vehicle_id: str, lat: float, lon: float, 
                                speed: float, bearing: float, next_stop_id: str,
                                dist_to_next: float, delay_sec: float, status: str):
        query = """
            UPDATE vehicles
            SET latitude = ?, longitude = ?, speed_kmh = ?, bearing = ?,
                next_stop_id = ?, distance_to_next_km = ?, current_delay_sec = ?,
                status = ?, last_updated = CURRENT_TIMESTAMP
            WHERE vehicle_id = ?
        """
        with self.get_connection() as conn:
            conn.execute(query, (lat, lon, speed, bearing, next_stop_id, dist_to_next, delay_sec, status, vehicle_id))
            conn.commit()

    def get_historical_arrivals(self, route_id: str, stop_id: Optional[str] = None, limit: int = 500) -> pd.DataFrame:
        if stop_id:
            query = """
                SELECT * FROM historical_arrivals
                WHERE route_id = ? AND stop_id = ?
                ORDER BY record_id DESC
                LIMIT ?
            """
            params = (route_id, stop_id, limit)
        else:
            query = """
                SELECT * FROM historical_arrivals
                WHERE route_id = ?
                ORDER BY record_id DESC
                LIMIT ?
            """
            params = (route_id, limit)
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=params)
            if not df.empty:
                df = df.sort_values('record_id').reset_index(drop=True)
            return df

    def log_prediction(self, route_id: str, vehicle_id: str, target_stop_id: str,
                       sched_sec: float, base_eta: float, z_eta: float,
                       pred_delay: float, ci_low: float, ci_high: float,
                       pole_rad: float, stability: str, comp_ms: float):
        query = """
            INSERT INTO prediction_logs 
            (route_id, vehicle_id, target_stop_id, scheduled_travel_time_sec,
             baseline_eta_sec, z_transform_eta_sec, predicted_delay_sec,
             confidence_interval_low, confidence_interval_high, system_pole_radius,
             stability_status, computation_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(query, (route_id, vehicle_id, target_stop_id, sched_sec,
                                 base_eta, z_eta, pred_delay, ci_low, ci_high,
                                 pole_rad, stability, comp_ms))
            conn.commit()

    def get_recent_prediction_logs(self, limit: int = 20) -> pd.DataFrame:
        query = "SELECT * FROM prediction_logs ORDER BY log_id DESC LIMIT ?"
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=(limit,))
