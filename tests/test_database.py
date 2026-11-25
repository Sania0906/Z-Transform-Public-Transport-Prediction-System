"""
Unit & Integration Tests for Database Operations.
Tests table queries, route/stop retrieval, vehicle updates, and prediction telemetry logging.
"""

import unittest
import numpy as np
import pandas as pd
from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager()

    def test_routes_exist(self):
        routes = self.db.get_all_routes()
        self.assertIsInstance(routes, pd.DataFrame)
        self.assertGreaterEqual(len(routes), 5, "Database must contain at least 5 routes.")
        self.assertIn("route_id", routes.columns)
        self.assertIn("route_name", routes.columns)

    def test_stops_exist(self):
        stops = self.db.get_all_stops()
        self.assertIsInstance(stops, pd.DataFrame)
        self.assertGreaterEqual(len(stops), 30, "Database must contain at least 30 transit stops.")
        self.assertIn("latitude", stops.columns)
        self.assertIn("longitude", stops.columns)

    def test_route_stops_mapping(self):
        r_stops = self.db.get_stops_for_route("R-101")
        self.assertIsInstance(r_stops, pd.DataFrame)
        self.assertEqual(len(r_stops), 10, "Route R-101 must contain exactly 10 stops.")
        # Verify sequence order
        sequences = list(r_stops['stop_sequence'])
        self.assertEqual(sequences, sorted(sequences), "Stops must be in ascending sequence order.")

    def test_vehicle_telemetry_and_update(self):
        vehicles = self.db.get_vehicles()
        self.assertGreaterEqual(len(vehicles), 15, "Must have at least 15 active vehicles.")
        
        # Test vehicle position update
        vid = vehicles.iloc[0]['vehicle_id']
        test_lat = 37.7801
        test_lon = -122.4101
        self.db.update_vehicle_position(
            vehicle_id=vid, lat=test_lat, lon=test_lon, speed=32.5,
            bearing=90.0, next_stop_id="S-102", dist_to_next=1.2,
            delay_sec=45.0, status="En Route"
        )
        updated = self.db.get_vehicles()
        v_row = updated[updated['vehicle_id'] == vid].iloc[0]
        self.assertAlmostEqual(v_row['latitude'], test_lat, places=3)
        self.assertAlmostEqual(v_row['longitude'], test_lon, places=3)

    def test_prediction_logging(self):
        self.db.log_prediction(
            route_id="R-101", vehicle_id="BUS-TEST", target_stop_id="S-105",
            sched_sec=420.0, base_eta=450.0, z_eta=435.0, pred_delay=15.0,
            ci_low=410.0, ci_high=460.0, pole_rad=0.68, stability="BIBO Stable",
            comp_ms=12.4
        )
        logs = self.db.get_recent_prediction_logs(limit=5)
        self.assertFalse(logs.empty)
        latest = logs.iloc[0]
        self.assertEqual(latest['vehicle_id'], "BUS-TEST")
        self.assertEqual(latest['route_id'], "R-101")

if __name__ == '__main__':
    unittest.main()
