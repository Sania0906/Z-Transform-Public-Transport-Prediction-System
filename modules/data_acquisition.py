"""
Module 1: Real-Time Transit Data Acquisition
Handles vehicle telemetry, route & stop geometry, distance/speed calculations,
and simulated real-time streaming with live GPS progression.
"""

import math
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from database.db_manager import DatabaseManager

class TransitDataAcquisition:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()
        self.simulation_mode = True # Clearly labeled synthetic/simulation mode

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great-circle distance between two points in km."""
        R = 6371.0 # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2.0) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate compass bearing (in degrees) from point 1 to point 2."""
        dlon = math.radians(lon2 - lon1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        y = math.sin(dlon) * math.cos(lat2_rad)
        x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
             math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))
        bearing = math.degrees(math.atan2(y, x))
        return (bearing + 360.0) % 360.0

    def get_routes(self) -> pd.DataFrame:
        """Retrieve all registered transit routes."""
        return self.db.get_all_routes()

    def get_stops(self, route_id: Optional[str] = None) -> pd.DataFrame:
        """Retrieve bus stops (filtered by route or global)."""
        if route_id:
            return self.db.get_stops_for_route(route_id)
        return self.db.get_all_stops()

    def get_active_vehicles(self, route_id: Optional[str] = None) -> pd.DataFrame:
        """Acquire active vehicle telemetry."""
        return self.db.get_vehicles(route_id)

    def get_historical_data(self, route_id: str, stop_id: Optional[str] = None, limit: int = 500) -> pd.DataFrame:
        """Acquire historical arrival time-series data."""
        return self.db.get_historical_arrivals(route_id, stop_id, limit)

    def simulate_telemetry_tick(self, vehicle_id: str, step_seconds: float = 10.0) -> Dict:
        """
        Advance vehicle along its route segment by step_seconds.
        Simulates realistic engine speed, GPS coordinate advancement,
        bearing rotation, and stop arrival / departure.
        """
        vehicles_df = self.db.get_vehicles()
        v_match = vehicles_df[vehicles_df['vehicle_id'] == vehicle_id]
        if v_match.empty:
            raise ValueError(f"Vehicle {vehicle_id} not found.")

        veh = v_match.iloc[0].to_dict()
        route_id = veh['route_id']
        stops_df = self.db.get_stops_for_route(route_id)
        
        cur_lat = veh['latitude']
        cur_lon = veh['longitude']
        speed_kmh = veh['speed_kmh']
        next_sid = veh['next_stop_id']
        dist_to_next = veh['distance_to_next_km']
        delay_sec = veh['current_delay_sec']

        target_stop_row = stops_df[stops_df['stop_id'] == next_sid]
        if target_stop_row.empty:
            target_stop_row = stops_df.iloc[0:1]
        
        target_lat = target_stop_row.iloc[0]['latitude']
        target_lon = target_stop_row.iloc[0]['longitude']

        # Distance moved in step_seconds (km)
        dist_moved = (speed_kmh / 3600.0) * step_seconds
        remaining_dist = max(0.0, dist_to_next - dist_moved)

        # Check if arrived at stop
        if remaining_dist <= 0.05: # Within 50 meters
            # Vehicle reached or passed stop -> advance to next stop
            cur_seq = target_stop_row.iloc[0]['stop_sequence']
            next_seq_row = stops_df[stops_df['stop_sequence'] == cur_seq + 1]
            if not next_seq_row.empty:
                new_next_sid = next_seq_row.iloc[0]['stop_id']
                new_target_lat = next_seq_row.iloc[0]['latitude']
                new_target_lon = next_seq_row.iloc[0]['longitude']
                new_dist = self.haversine_distance_km(target_lat, target_lon, new_target_lat, new_target_lon)
                new_bearing = self.calculate_bearing(target_lat, target_lon, new_target_lat, new_target_lon)
                status = "At Stop"
                new_speed = 0.0
            else:
                # Route end reached -> loop back to first stop
                first_row = stops_df.iloc[0]
                new_next_sid = first_row['stop_id']
                new_target_lat = first_row['latitude']
                new_target_lon = first_row['longitude']
                new_dist = self.haversine_distance_km(target_lat, target_lon, new_target_lat, new_target_lon)
                new_bearing = self.calculate_bearing(target_lat, target_lon, new_target_lat, new_target_lon)
                status = "Terminal Loop"
                new_speed = 15.0
            
            new_lat, new_lon = target_lat, target_lon
            new_delay = delay_sec + np.random.normal(5.0, 4.0) # slight dwell deviation
            
            self.db.update_vehicle_position(
                vehicle_id=vehicle_id, lat=new_lat, lon=new_lon, speed=new_speed,
                bearing=new_bearing, next_stop_id=new_next_sid, dist_to_next=round(new_dist, 2),
                delay_sec=round(new_delay, 1), status=status
            )
            veh.update({
                'latitude': new_lat, 'longitude': new_lon, 'speed_kmh': new_speed,
                'bearing': new_bearing, 'next_stop_id': new_next_sid,
                'distance_to_next_km': round(new_dist, 2),
                'current_delay_sec': round(new_delay, 1), 'status': status
            })
            return veh

        # Still en route between stops: advance coordinates towards target
        total_seg_dist = self.haversine_distance_km(cur_lat, cur_lon, target_lat, target_lon)
        if total_seg_dist > 0:
            fraction = min(1.0, dist_moved / total_seg_dist)
            new_lat = cur_lat + fraction * (target_lat - cur_lat)
            new_lon = cur_lon + fraction * (target_lon - cur_lon)
        else:
            new_lat, new_lon = target_lat, target_lon

        new_bearing = self.calculate_bearing(new_lat, new_lon, target_lat, target_lon)
        # Random speed perturbation
        new_speed = float(np.clip(speed_kmh + np.random.normal(0.0, 1.5), 15.0, 45.0))
        new_delay = float(delay_sec + np.random.normal(0.2, 1.0))
        status = "En Route"

        self.db.update_vehicle_position(
            vehicle_id=vehicle_id, lat=round(new_lat, 6), lon=round(new_lon, 6),
            speed=round(new_speed, 1), bearing=round(new_bearing, 1),
            next_stop_id=next_sid, dist_to_next=round(remaining_dist, 2),
            delay_sec=round(new_delay, 1), status=status
        )
        veh.update({
            'latitude': round(new_lat, 6), 'longitude': round(new_lon, 6),
            'speed_kmh': round(new_speed, 1), 'bearing': round(new_bearing, 1),
            'distance_to_next_km': round(remaining_dist, 2),
            'current_delay_sec': round(new_delay, 1), 'status': status
        })
        return veh
