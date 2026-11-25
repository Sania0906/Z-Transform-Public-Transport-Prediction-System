"""
UI Card and Component Builders for Streamlit Interface.
Renders executive metric cards, countdown displays, status pills, and alert banners.
"""

from typing import Optional, Dict

def render_metric_card(label: str, value: str, sub: str = "", theme: str = "blue") -> str:
    """Generate HTML string for executive metric card."""
    theme_cls = {
        "blue": "",
        "teal": "teal",
        "purple": "purple",
        "warning": "warning"
    }.get(theme, "")

    return f"""
    <div class="metric-card {theme_cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {f'<div class="metric-sub">{sub}</div>' if sub else ''}
    </div>
    """

def render_countdown_card(minutes: int, seconds: int, target_stop: str, bus_id: str, route_name: str) -> str:
    """Generate HTML string for live countdown card."""
    return f"""
    <div class="countdown-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span class="live-badge"><span class="pulse-dot"></span> Live Tracking</span>
            <span style="font-size: 0.82rem; color: #94A3B8; font-weight: 600;">{bus_id} • {route_name}</span>
        </div>
        <div class="countdown-unit" style="margin-bottom: 4px;">Arriving At: <span style="color: #FFFFFF; font-weight: 700;">{target_stop}</span></div>
        <div class="countdown-digits">{minutes:02d}:{seconds:02d}</div>
        <div class="countdown-unit">Minutes : Seconds Remaining</div>
    </div>
    """

def render_status_pill(status: str, delay_sec: float) -> str:
    """Generate status pill (On-Time / Delayed)."""
    if delay_sec <= 60.0:
        return f'<span class="status-pill status-ontime">● On-Time ({delay_sec:+.0f}s)</span>'
    elif delay_sec <= 300.0:
        return f'<span class="status-pill status-delayed" style="background: rgba(245, 158, 11, 0.15); color: #F59E0B; border-color: rgba(245, 158, 11, 0.3);">▲ Minor Delay (+{delay_sec/60:.1f}m)</span>'
    else:
        return f'<span class="status-pill status-delayed">■ Severe Delay (+{delay_sec/60:.1f}m)</span>'

def render_alert_banner(title: str, message: str, level: str = "info") -> str:
    """Generate passenger advisory banner."""
    colors = {
        "info": ("rgba(0, 180, 216, 0.15)", "rgba(0, 180, 216, 0.4)", "#00E5FF", "ℹ️"),
        "success": ("rgba(16, 185, 129, 0.15)", "rgba(16, 185, 129, 0.4)", "#10B981", "✓"),
        "warning": ("rgba(245, 158, 11, 0.15)", "rgba(245, 158, 11, 0.4)", "#F59E0B", "⚠️"),
        "danger": ("rgba(239, 68, 68, 0.15)", "rgba(239, 68, 68, 0.4)", "#EF4444", "🚨")
    }
    bg, border, text_c, icon = colors.get(level, colors["info"])

    return f"""
    <div style="background: {bg}; border: 1px solid {border}; border-radius: 10px; padding: 12px 18px; margin: 12px 0; display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 1.25rem;">{icon}</span>
        <div>
            <div style="font-weight: 700; color: {text_c}; font-size: 0.9rem;">{title}</div>
            <div style="color: #CBD5E1; font-size: 0.84rem;">{message}</div>
        </div>
    </div>
    """
