"""
Synthetic Dataset Generator for Z-Transform Public Transport Arrival Time System.
Creates realistic spatial routes, bus stops, vehicle positions, and 4500+ historical arrivals.
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import random
import datetime
import numpy as np
import pandas as pd
from database.db_manager import DatabaseManager

np.random.seed(42)
random.seed(42)

DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets")
os.makedirs(DATASETS_DIR, exist_ok=True)

# Define 5 major Transit Routes in Metropolitan Corridor
ROUTES_DATA = [
    {
        "route_id": "R-101",
        "route_name": "Downtown Metro Express",
        "route_short_name": "EX-101",
        "route_color": "#1E88E5", # Electric Blue
        "origin": "Central Terminal Station",
        "destination": "Tech Innovation Hub",
        "total_distance_km": 14.8,
        "typical_duration_min": 42.0,
        "frequency_min": 8,
        "is_active": 1
    },
    {
        "route_id": "R-202",
        "route_name": "Emerald University & Med Corridor",
        "route_short_name": "UM-202",
        "route_color": "#00B0FF", # Cyan / Teal
        "origin": "West Bay Interchange",
        "destination": "Medical Science Park",
        "total_distance_km": 12.4,
        "typical_duration_min": 36.0,
        "frequency_min": 10,
        "is_active": 1
    },
    {
        "route_id": "R-303",
        "route_name": "Crimson Airport SkyLink",
        "route_short_name": "SL-303",
        "route_color": "#7C4DFF", # Purple Accent
        "origin": "International Terminal Plaza",
        "destination": "Civic Center Grand Plaza",
        "total_distance_km": 18.5,
        "typical_duration_min": 48.0,
        "frequency_min": 12,
        "is_active": 1
    },
    {
        "route_id": "R-404",
        "route_name": "Amber Suburban Circular Loop",
        "route_short_name": "SC-404",
        "route_color": "#00E5FF", # Neon Cyan
        "origin": "Northgate Transit Station",
        "destination": "East Gateway Hub",
        "total_distance_km": 15.6,
        "typical_duration_min": 44.0,
        "frequency_min": 15,
        "is_active": 1
    },
    {
        "route_id": "R-505",
        "route_name": "Harbor Waterfront Promenade",
        "route_short_name": "WP-505",
        "route_color": "#29B6F6", # Sky Blue
        "origin": "Maritime Pier 39",
        "destination": "Financial District Boulevard",
        "total_distance_km": 9.2,
        "typical_duration_min": 26.0,
        "frequency_min": 10,
        "is_active": 1
    }
]

# Base anchor points for realistic metropolitan geometry (lat ~ 37.76 to 37.81, lon ~ -122.45 to -122.39)
# Stop dictionary
STOPS_MASTER = {
    # R-101 Stops (10 stops)
    "S-101": ("Central Terminal Station", 37.7749, -122.4194, "Enclosed Glass Terminal", "R-202, R-303"),
    "S-102": ("Market & 5th Avenue", 37.7833, -122.4089, "Canopy Shelter", "R-303"),
    "S-103": ("Financial Center Plaza", 37.7915, -122.4005, "Enclosed Glass Terminal", "R-505"),
    "S-104": ("Embarcadero Gateway", 37.7955, -122.3937, "Canopy Shelter", "R-505"),
    "S-105": ("Mission Bay Boulevard", 37.7765, -122.3912, "Digital Modern Pod", "R-202"),
    "S-106": ("Bio-Research Center", 37.7682, -122.3895, "Canopy Shelter", "None"),
    "S-107": ("Potrero Hill Transit Node", 37.7588, -122.3982, "Standard Shelter", "None"),
    "S-108": ("Design District Walkway", 37.7670, -122.4050, "Standard Shelter", "R-404"),
    "S-109": ("Civic Auditorium", 37.7780, -122.4170, "Digital Modern Pod", "R-303"),
    "S-110": ("Tech Innovation Hub", 37.7885, -122.4072, "Enclosed Glass Terminal", "R-202, R-404"),

    # R-202 Stops (9 stops)
    "S-201": ("West Bay Interchange", 37.7645, -122.4468, "Enclosed Glass Terminal", "R-404"),
    "S-202": ("Castro Street Gateway", 37.7609, -122.4350, "Canopy Shelter", "None"),
    "S-203": ("Valencia Cultural District", 37.7600, -122.4215, "Standard Shelter", "None"),
    "S-204": ("Mission Central Hub", 37.7628, -122.4181, "Digital Modern Pod", "R-101"),
    "S-205": ("General Hospital East Wing", 37.7552, -122.4048, "Enclosed Glass Terminal", "None"),
    "S-206": ("Dogpatch Arts Walk", 37.7602, -122.3888, "Canopy Shelter", "R-505"),
    "S-207": ("UCSF Medical Plaza", 37.7668, -122.3905, "Digital Modern Pod", "R-101"),
    "S-208": ("South Beach Marina", 37.7810, -122.3900, "Standard Shelter", "R-505"),
    "S-209": ("Medical Science Park", 37.7685, -122.3920, "Enclosed Glass Terminal", "R-101, R-303"),

    # R-303 Stops (8 stops)
    "S-301": ("International Terminal Plaza", 37.7200, -122.4000, "Enclosed Glass Terminal", "None"),
    "S-302": ("Bayshore Expressway Junction", 37.7350, -122.4050, "Canopy Shelter", "None"),
    "S-303": ("Silver Terrace Node", 37.7450, -122.4030, "Standard Shelter", "None"),
    "S-304": ("Cesar Chavez Boulevard", 37.7525, -122.4060, "Digital Modern Pod", "R-202"),
    "S-305": ("16th Street Urban Transfer", 37.7650, -122.4190, "Enclosed Glass Terminal", "R-101, R-202"),
    "S-306": ("Van Ness Civic Corridor", 37.7750, -122.4200, "Canopy Shelter", "R-101"),
    "S-307": ("City Hall South Portico", 37.7790, -122.4180, "Digital Modern Pod", "None"),
    "S-308": ("Civic Center Grand Plaza", 37.7810, -122.4150, "Enclosed Glass Terminal", "R-101, R-404"),

    # R-404 Stops (10 stops)
    "S-401": ("Northgate Transit Station", 37.8020, -122.4200, "Enclosed Glass Terminal", "None"),
    "S-402": ("Marina Boulevard Green", 37.8050, -122.4350, "Canopy Shelter", "None"),
    "S-403": ("Presidio East Entrance", 37.7980, -122.4480, "Standard Shelter", "None"),
    "S-404": ("Richmond Center", 37.7800, -122.4600, "Canopy Shelter", "None"),
    "S-405": ("Sunset Boulevard Crossing", 37.7600, -122.4550, "Standard Shelter", "None"),
    "S-406": ("Twin Peaks Panorama", 37.7540, -122.4470, "Digital Modern Pod", "R-202"),
    "S-407": ("Diamond Heights Heights", 37.7440, -122.4400, "Standard Shelter", "None"),
    "S-408": ("Glen Park Rail Connector", 37.7330, -122.4330, "Enclosed Glass Terminal", "None"),
    "S-409": ("Mission Dolores Square", 37.7600, -122.4260, "Canopy Shelter", "R-202"),
    "S-410": ("East Gateway Hub", 37.7700, -122.4000, "Enclosed Glass Terminal", "R-101, R-303"),

    # R-505 Stops (7 stops)
    "S-501": ("Maritime Pier 39", 37.8087, -122.4098, "Enclosed Glass Terminal", "None"),
    "S-502": ("Fisherman's Wharf Central", 37.8080, -122.4177, "Canopy Shelter", "None"),
    "S-503": ("Aquatic Park Promenade", 37.8060, -122.4230, "Standard Shelter", "None"),
    "S-504": ("North Beach Historic Way", 37.8000, -122.4100, "Canopy Shelter", "None"),
    "S-505": ("Ferry Building Plaza", 37.7955, -122.3937, "Digital Modern Pod", "R-101"),
    "S-506": ("Rincon Hill Overlook", 37.7870, -122.3920, "Canopy Shelter", "None"),
    "S-507": ("Financial District Boulevard", 37.7920, -122.4020, "Enclosed Glass Terminal", "R-101, R-202")
}

# Route to sequence of stop IDs
ROUTE_STOPS_MAP = {
    "R-101": ["S-101", "S-102", "S-103", "S-104", "S-105", "S-106", "S-107", "S-108", "S-109", "S-110"],
    "R-202": ["S-201", "S-202", "S-203", "S-204", "S-205", "S-206", "S-207", "S-208", "S-209"],
    "R-303": ["S-301", "S-302", "S-303", "S-304", "S-305", "S-306", "S-307", "S-308"],
    "R-404": ["S-401", "S-402", "S-403", "S-404", "S-405", "S-406", "S-407", "S-408", "S-409", "S-410"],
    "R-505": ["S-501", "S-502", "S-503", "S-504", "S-505", "S-506", "S-507"]
}

# 15 Active Vehicles
VEHICLES_DATA = [
    {"vehicle_id": "BUS-1011", "route_id": "R-101", "vehicle_model": "Nova Electric LFS-60", "capacity": 85, "driver_name": "Marcus Vance", "status": "En Route"},
    {"vehicle_id": "BUS-1012", "route_id": "R-101", "vehicle_model": "New Flyer Xcelsior Charge", "capacity": 75, "driver_name": "Elena Rostova", "status": "En Route"},
    {"vehicle_id": "BUS-1013", "route_id": "R-101", "vehicle_model": "BYD K9M Electric", "capacity": 70, "driver_name": "Devon Hayes", "status": "En Route"},
    {"vehicle_id": "BUS-2021", "route_id": "R-202", "vehicle_model": "Proterra ZX5 Max", "capacity": 75, "driver_name": "Sarah Lin", "status": "En Route"},
    {"vehicle_id": "BUS-2022", "route_id": "R-202", "vehicle_model": "New Flyer Xcelsior Charge", "capacity": 75, "driver_name": "Jamal Washington", "status": "En Route"},
    {"vehicle_id": "BUS-2023", "route_id": "R-202", "vehicle_model": "Nova Electric LFS-60", "capacity": 85, "driver_name": "Chloe Bennett", "status": "Delayed"},
    {"vehicle_id": "BUS-3031", "route_id": "R-303", "vehicle_model": "Gillig Low Floor EV", "capacity": 65, "driver_name": "Kenji Sato", "status": "En Route"},
    {"vehicle_id": "BUS-3032", "route_id": "R-303", "vehicle_model": "Proterra ZX5 Max", "capacity": 75, "driver_name": "Ananya Sharma", "status": "En Route"},
    {"vehicle_id": "BUS-3033", "route_id": "R-303", "vehicle_model": "New Flyer Xcelsior Charge", "capacity": 75, "driver_name": "Mateo Rossi", "status": "En Route"},
    {"vehicle_id": "BUS-4041", "route_id": "R-404", "vehicle_model": "BYD K9M Electric", "capacity": 70, "driver_name": "Hannah Abbott", "status": "En Route"},
    {"vehicle_id": "BUS-4042", "route_id": "R-404", "vehicle_model": "Nova Electric LFS-60", "capacity": 85, "driver_name": "Travis Scott", "status": "At Stop"},
    {"vehicle_id": "BUS-4043", "route_id": "R-404", "vehicle_model": "Gillig Low Floor EV", "capacity": 65, "driver_name": "Maya Patel", "status": "En Route"},
    {"vehicle_id": "BUS-5051", "route_id": "R-505", "vehicle_model": "Proterra ZX5 Max", "capacity": 75, "driver_name": "Liam Gallagher", "status": "En Route"},
    {"vehicle_id": "BUS-5052", "route_id": "R-505", "vehicle_model": "New Flyer Xcelsior Charge", "capacity": 75, "driver_name": "Sofia Gomez", "status": "En Route"},
    {"vehicle_id": "BUS-5053", "route_id": "R-505", "vehicle_model": "BYD K9M Electric", "capacity": 70, "driver_name": "Oliver Twist", "status": "En Route"},
]

def haversine_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2.0)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def generate_all_data():
    db = DatabaseManager()

    # 1. Routes DataFrame
    df_routes = pd.DataFrame(ROUTES_DATA)
    df_routes.to_csv(os.path.join(DATASETS_DIR, "bus_routes.csv"), index=False)
    with db.get_connection() as conn:
        df_routes.to_sql("routes", conn, if_exists="replace", index=False)

    # 2. Stops DataFrame
    stops_rows = []
    for sid, (sname, lat, lon, shelter, trans) in STOPS_MASTER.items():
        stops_rows.append({
            "stop_id": sid,
            "stop_name": sname,
            "latitude": lat,
            "longitude": lon,
            "shelter_type": shelter,
            "has_digital_signage": 1,
            "transfer_routes": trans
        })
    df_stops = pd.DataFrame(stops_rows)
    df_stops.to_csv(os.path.join(DATASETS_DIR, "bus_stops.csv"), index=False)
    with db.get_connection() as conn:
        df_stops.to_sql("stops", conn, if_exists="replace", index=False)

    # 3. Route-Stops mapping with cumulative distance and scheduled time
    route_stops_rows = []
    for r_info in ROUTES_DATA:
        rid = r_info["route_id"]
        stop_ids = ROUTE_STOPS_MAP[rid]
        cum_dist = 0.0
        cum_time = 0

        for seq, sid in enumerate(stop_ids, start=1):
            if seq == 1:
                seg_dist = 0.0
                seg_time = 0
            else:
                prev_sid = stop_ids[seq - 2]
                lat1, lon1 = STOPS_MASTER[prev_sid][1], STOPS_MASTER[prev_sid][2]
                lat2, lon2 = STOPS_MASTER[sid][1], STOPS_MASTER[sid][2]
                seg_dist = max(0.8, haversine_distance_km(lat1, lon1, lat2, lon2) * 1.25) # Road factor
                seg_time = int((seg_dist / 24.0) * 3600) # Average speed 24 km/h

            cum_dist += seg_dist
            cum_time += seg_time

            route_stops_rows.append({
                "route_id": rid,
                "stop_id": sid,
                "stop_sequence": seq,
                "distance_from_start_km": round(cum_dist, 2),
                "scheduled_travel_time_sec": cum_time
            })
    df_route_stops = pd.DataFrame(route_stops_rows)
    with db.get_connection() as conn:
        df_route_stops.to_sql("route_stops", conn, if_exists="replace", index=False)

    # 4. Realistic Vehicle Positions Telemetry
    vehicle_rows = []
    for v in VEHICLES_DATA:
        rid = v["route_id"]
        stop_ids = ROUTE_STOPS_MAP[rid]
        # Pick random active segment along the route
        seg_idx = random.randint(0, len(stop_ids) - 2)
        last_s = stop_ids[seg_idx]
        next_s = stop_ids[seg_idx + 1]

        # Interpolate coordinates between last_s and next_s with progress fraction
        frac = random.uniform(0.15, 0.85)
        lat1, lon1 = STOPS_MASTER[last_s][1], STOPS_MASTER[last_s][2]
        lat2, lon2 = STOPS_MASTER[next_s][1], STOPS_MASTER[next_s][2]
        
        cur_lat = round(lat1 + frac * (lat2 - lat1) + np.random.normal(0, 0.0003), 6)
        cur_lon = round(lon1 + frac * (lon2 - lon1) + np.random.normal(0, 0.0003), 6)
        
        # Calculate bearing
        dlon = np.radians(lon2 - lon1)
        y = np.sin(dlon) * np.cos(np.radians(lat2))
        x = np.cos(np.radians(lat1)) * np.sin(np.radians(lat2)) - np.sin(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.cos(dlon)
        bearing = (np.degrees(np.arctan2(y, x)) + 360) % 360

        dist_next = round((1.0 - frac) * max(0.8, haversine_distance_km(lat1, lon1, lat2, lon2)), 2)
        speed = round(random.uniform(18.0, 38.0), 1)
        delay_sec = round(random.uniform(-45.0, 380.0), 1)
        load_pct = random.randint(25, 92)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        vehicle_rows.append({
            "vehicle_id": v["vehicle_id"],
            "route_id": rid,
            "vehicle_model": v["vehicle_model"],
            "capacity": v["capacity"],
            "driver_name": v["driver_name"],
            "status": v["status"],
            "latitude": cur_lat,
            "longitude": cur_lon,
            "speed_kmh": speed,
            "bearing": round(bearing, 1),
            "last_stop_id": last_s,
            "next_stop_id": next_s,
            "distance_to_next_km": dist_next,
            "current_delay_sec": delay_sec,
            "passenger_load_pct": load_pct,
            "last_updated": now_str
        })
    df_vehicles = pd.DataFrame(vehicle_rows)
    df_vehicles.to_csv(os.path.join(DATASETS_DIR, "vehicle_positions.csv"), index=False)
    with db.get_connection() as conn:
        df_vehicles.to_sql("vehicles", conn, if_exists="replace", index=False)

    # 5. Historical Arrivals Dataset (4,800+ records)
    print("Generating 4,800+ realistic historical arrival records with Autoregressive Delay Dynamics...")
    hist_rows = []
    base_time = datetime.datetime.now() - datetime.timedelta(days=14)
    trip_counter = 1

    time_patterns = [
        # (time_name, start_h, end_h, base_delay_mean, congestion_lvl, weather_dist)
        ("morning_peak", 7, 10, 180.0, 4, ["Clear", "Clear", "Light Rain", "Congested Fog"]),
        ("midday", 11, 15, 45.0, 2, ["Clear", "Clear", "Clear", "Light Rain"]),
        ("evening_peak", 16, 19, 240.0, 5, ["Clear", "Clear", "Rain", "Light Rain"]),
        ("night", 20, 23, -20.0, 1, ["Clear", "Clear", "Clear", "Clear"])
    ]

    for day in range(14):
        current_day_date = base_time + datetime.timedelta(days=day)
        day_of_week = current_day_date.weekday()

        for rid in ROUTE_STOPS_MAP.keys():
            buses_on_route = [v["vehicle_id"] for v in VEHICLES_DATA if v["route_id"] == rid]
            stop_ids = ROUTE_STOPS_MAP[rid]

            # Generate multiple trips per day for this route
            for pattern_name, s_hour, e_hour, delay_mean, cong_base, weather_options in time_patterns:
                for trip_idx in range(3): # 3 trips per time pattern
                    trip_id = f"TRIP-{rid}-{day:02d}{trip_counter:04d}"
                    trip_counter += 1
                    vehicle_id = random.choice(buses_on_route)
                    weather = random.choice(weather_options)
                    congestion = min(5, max(1, cong_base + (1 if weather == "Rain" else 0)))

                    start_hour = random.randint(s_hour, e_hour - 1)
                    start_minute = random.randint(0, 59)
                    trip_start_dt = current_day_date.replace(hour=start_hour, minute=start_minute, second=0)

                    # Dynamic AR(2) delay process across stops along corridor
                    # d[n] = a1 * d[n-1] + a2 * d[n-2] + noise
                    # Stable poles: a1=0.72, a2=0.18
                    delay_prev1 = np.random.normal(delay_mean * 0.4, 25.0)
                    delay_prev2 = delay_prev1 * 0.8
                    cum_sched_time = 0

                    for seq_idx, sid in enumerate(stop_ids):
                        if seq_idx == 0:
                            seg_dist = 0.0
                            sched_trav_sec = 0
                            dwell_sec = random.uniform(30.0, 60.0)
                            delay_cur = max(-60.0, delay_prev1)
                        else:
                            prev_sid = stop_ids[seq_idx - 1]
                            lat1, lon1 = STOPS_MASTER[prev_sid][1], STOPS_MASTER[prev_sid][2]
                            lat2, lon2 = STOPS_MASTER[sid][1], STOPS_MASTER[sid][2]
                            seg_dist = max(0.8, haversine_distance_km(lat1, lon1, lat2, lon2) * 1.25)
                            base_speed_kmh = 24.0 / (1.0 + 0.15 * (congestion - 1))
                            sched_trav_sec = int((seg_dist / 24.0) * 3600)
                            dwell_sec = random.uniform(15.0, 45.0) + (10.0 if congestion >= 4 else 0.0)

                            # Autoregressive delay propagation with disturbance shock
                            shock = np.random.normal(0.0, 18.0) + (25.0 if congestion == 5 else 0.0)
                            delay_cur = 0.72 * delay_prev1 + 0.18 * delay_prev2 + shock
                            delay_prev2 = delay_prev1
                            delay_prev1 = delay_cur

                        cum_sched_time += sched_trav_sec
                        sched_arr = trip_start_dt + datetime.timedelta(seconds=cum_sched_time)
                        actual_arr = sched_arr + datetime.timedelta(seconds=int(delay_cur))

                        actual_trav_sec = max(20.0, sched_trav_sec + delay_cur)
                        effective_speed = round((seg_dist / (actual_trav_sec / 3600.0)), 2) if (seg_dist > 0 and actual_trav_sec > 0) else 0.0

                        hist_rows.append({
                            "trip_id": trip_id,
                            "route_id": rid,
                            "vehicle_id": vehicle_id,
                            "stop_id": sid,
                            "stop_sequence": seq_idx + 1,
                            "scheduled_arrival_time": sched_arr.strftime("%Y-%m-%d %H:%M:%S"),
                            "actual_arrival_time": actual_arr.strftime("%Y-%m-%d %H:%M:%S"),
                            "delay_seconds": round(delay_cur, 2),
                            "dwell_time_seconds": round(dwell_sec, 2),
                            "scheduled_travel_time_sec": sched_trav_sec,
                            "actual_travel_time_sec": round(actual_trav_sec, 2),
                            "segment_distance_km": round(seg_dist, 2),
                            "segment_speed_kmh": effective_speed,
                            "time_of_day": pattern_name,
                            "day_of_week": day_of_week,
                            "weather_condition": weather,
                            "congestion_level": congestion
                        })

    df_hist = pd.DataFrame(hist_rows)
    df_hist.insert(0, "record_id", range(1, len(df_hist) + 1))
    df_hist.to_csv(os.path.join(DATASETS_DIR, "historical_arrivals.csv"), index=False)
    with db.get_connection() as conn:
        df_hist.to_sql("historical_arrivals", conn, if_exists="replace", index=False)

    print(f"Dataset generated successfully!")
    print(f"Routes: {len(df_routes)}")
    print(f"Stops: {len(df_stops)}")
    print(f"Active Vehicles: {len(df_vehicles)}")
    print(f"Historical Records: {len(df_hist)}")

if __name__ == "__main__":
    generate_all_data()
