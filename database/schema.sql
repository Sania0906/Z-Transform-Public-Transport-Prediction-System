-- Z-Transform Public Transport System Database Schema
-- SQLite3 Compatible

CREATE TABLE IF NOT EXISTS routes (
    route_id TEXT PRIMARY KEY,
    route_name TEXT NOT NULL,
    route_short_name TEXT NOT NULL,
    route_color TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    total_distance_km REAL NOT NULL,
    typical_duration_min REAL NOT NULL,
    frequency_min INTEGER NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS stops (
    stop_id TEXT PRIMARY KEY,
    stop_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    shelter_type TEXT NOT NULL,
    has_digital_signage INTEGER DEFAULT 1,
    transfer_routes TEXT
);

CREATE TABLE IF NOT EXISTS route_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id TEXT NOT NULL,
    stop_id TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    distance_from_start_km REAL NOT NULL,
    scheduled_travel_time_sec INTEGER NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    vehicle_model TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    driver_name TEXT NOT NULL,
    status TEXT NOT NULL, -- 'En Route', 'At Stop', 'Delayed', 'Terminal'
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    speed_kmh REAL NOT NULL,
    bearing REAL NOT NULL,
    last_stop_id TEXT,
    next_stop_id TEXT,
    distance_to_next_km REAL NOT NULL,
    current_delay_sec REAL NOT NULL,
    passenger_load_pct INTEGER NOT NULL,
    last_updated DATETIME NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

CREATE TABLE IF NOT EXISTS historical_arrivals (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id TEXT NOT NULL,
    route_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    stop_id TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    scheduled_arrival_time DATETIME NOT NULL,
    actual_arrival_time DATETIME NOT NULL,
    delay_seconds REAL NOT NULL,
    dwell_time_seconds REAL NOT NULL,
    scheduled_travel_time_sec REAL NOT NULL,
    actual_travel_time_sec REAL NOT NULL,
    segment_distance_km REAL NOT NULL,
    segment_speed_kmh REAL NOT NULL,
    time_of_day TEXT NOT NULL, -- 'morning_peak', 'midday', 'evening_peak', 'night'
    day_of_week INTEGER NOT NULL,
    weather_condition TEXT NOT NULL,
    congestion_level INTEGER NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE IF NOT EXISTS prediction_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    route_id TEXT NOT NULL,
    vehicle_id TEXT NOT NULL,
    target_stop_id TEXT NOT NULL,
    scheduled_travel_time_sec REAL NOT NULL,
    baseline_eta_sec REAL NOT NULL,
    z_transform_eta_sec REAL NOT NULL,
    predicted_delay_sec REAL NOT NULL,
    confidence_interval_low REAL NOT NULL,
    confidence_interval_high REAL NOT NULL,
    system_pole_radius REAL NOT NULL,
    stability_status TEXT NOT NULL,
    computation_time_ms REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_hist_route_stop ON historical_arrivals(route_id, stop_id);
CREATE INDEX IF NOT EXISTS idx_hist_trip ON historical_arrivals(trip_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_route ON vehicles(route_id);
