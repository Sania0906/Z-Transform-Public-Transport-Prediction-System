"""
Interactive Folium Transit Map Component.
Renders dark navy CartoDB map with routes, bus stop nodes, and active vehicle telemetry pins.
"""

import folium
from folium import plugins
import pandas as pd
from typing import List, Optional, Dict

def create_transit_map(routes_df: pd.DataFrame, 
                       stops_df: pd.DataFrame, 
                       vehicles_df: pd.DataFrame, 
                       selected_route_id: Optional[str] = None,
                       selected_vehicle_id: Optional[str] = None) -> folium.Map:
    """
    Construct full interactive Folium map centered on active transit network.
    """
    # Default center coordinates around Metro Area
    if not stops_df.empty:
        center_lat = float(stops_df['latitude'].mean())
        center_lon = float(stops_df['longitude'].mean())
    else:
        center_lat, center_lon = 37.7749, -122.4194

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="CartoDB dark_matter",
        control_scale=True
    )

    # Route color mapping
    route_colors = {
        "R-101": "#1E88E5",
        "R-202": "#00B0FF",
        "R-303": "#7C4DFF",
        "R-404": "#00E5FF",
        "R-505": "#29B6F6"
    }

    # Filter data if specific route is selected
    if selected_route_id and selected_route_id != "All Routes":
        active_routes = routes_df[routes_df['route_id'] == selected_route_id]
        active_stops = stops_df[stops_df['stop_id'].isin(
            # Filter stops belonging to route
            stops_df['stop_id'] if 'stop_id' in stops_df else []
        )]
        active_vehicles = vehicles_df[vehicles_df['route_id'] == selected_route_id]
    else:
        active_routes = routes_df
        active_stops = stops_df
        active_vehicles = vehicles_df

    # Draw Route Corridors (Polylines connecting stops)
    for _, r in active_routes.iterrows():
        rid = r['route_id']
        rcolor = route_colors.get(rid, "#00B4D8")
        # In a real setup or stops sequence:
        r_stops = stops_df[stops_df.get('route_id', rid) == rid] if 'route_id' in stops_df.columns else stops_df
        if not r_stops.empty and 'latitude' in r_stops.columns:
            coords = list(zip(r_stops['latitude'], r_stops['longitude']))
            if len(coords) >= 2:
                folium.PolyLine(
                    locations=coords,
                    color=rcolor,
                    weight=4,
                    opacity=0.85,
                    popup=f"<b>{r.get('route_name', rid)}</b> ({rid})",
                    tooltip=f"Route {rid}: {r.get('origin', '')} → {r.get('destination', '')}"
                ).add_to(m)

    # Draw Bus Stop Nodes
    for _, s in active_stops.iterrows():
        slat = float(s['latitude'])
        slon = float(s['longitude'])
        sname = s['stop_name']
        sid = s['stop_id']
        shelter = s.get('shelter_type', 'Standard Shelter')
        transfers = s.get('transfer_routes', 'None')

        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 160px; color: #1E293B;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #0284C7;">BUS STOP [{sid}]</div>
            <div style="font-size: 0.95rem; font-weight: 700; margin: 2px 0;">{sname}</div>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #E2E8F0;">
            <div style="font-size: 0.78rem;"><b>Shelter:</b> {shelter}</div>
            <div style="font-size: 0.78rem;"><b>Transfers:</b> {transfers}</div>
        </div>
        """

        folium.CircleMarker(
            location=[slat, slon],
            radius=6,
            color="#00F5D4",
            weight=2,
            fill=True,
            fill_color="#0B132B",
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{sname} ({sid})"
        ).add_to(m)

    # Draw Active Vehicle Pins
    for _, v in active_vehicles.iterrows():
        vlat = float(v['latitude'])
        vlon = float(v['longitude'])
        vid = v['vehicle_id']
        vroute = v.get('route_short_name', v['route_id'])
        vspeed = v['speed_kmh']
        vdelay = v['current_delay_sec']
        vstatus = v.get('status', 'En Route')
        next_sid = v.get('next_stop_id', 'Next Stop')
        is_highlighted = (selected_vehicle_id == vid)

        pin_color = "red" if vdelay > 240 else ("orange" if vdelay > 90 else "cadetblue")
        if is_highlighted:
            pin_color = "purple"

        veh_popup = f"""
        <div style="font-family: sans-serif; min-width: 180px; color: #1E293B;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #2563EB;">VEHICLE TELEMETRY</div>
            <div style="font-size: 1.0rem; font-weight: 800; color: #0F172A;">{vid} ({vroute})</div>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #CBD5E1;">
            <div style="font-size: 0.8rem;"><b>Status:</b> {vstatus}</div>
            <div style="font-size: 0.8rem;"><b>Speed:</b> {vspeed:.1f} km/h</div>
            <div style="font-size: 0.8rem;"><b>Current Delay:</b> {vdelay:+.1f} s</div>
            <div style="font-size: 0.8rem;"><b>Target Stop:</b> {next_sid}</div>
        </div>
        """

        folium.Marker(
            location=[vlat, vlon],
            popup=folium.Popup(veh_popup, max_width=260),
            tooltip=f"{vid} • {vspeed:.0f} km/h • Delay: {vdelay:+.0f}s",
            icon=folium.Icon(color=pin_color, icon="bus", prefix="fa")
        ).add_to(m)

    return m
