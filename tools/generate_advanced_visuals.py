"""
Generate custom, publication-grade diagrams for:
1. Slide 2: Introduction Concept Visual (assets/screenshots/introduction_concept_visual.png)
   - Visualizes urban transit delay volatility, discrete signal modeling, Z-domain transformation, and the end-to-end framework.
2. Slide 7: System Architecture Diagram (assets/screenshots/system_architecture_diagram.png)
   - Complete 4-layer technical architecture blueprint: Ingestion -> Preprocessing -> Z-Transform Core -> Passenger Dashboard.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "assets", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Theme Palette (Matches Project UI)
DARK_BG = "#0A0F1D"
CARD_BG = "#131B2E"
CARD_INNER = "#0D1527"
BORDER_BLUE = "#0284C7"
BORDER_CYAN = "#00F5D4"
BORDER_PURPLE = "#7C4DFF"
BORDER_MUTED = "#334155"
TEXT_WHITE = "#FFFFFF"
TEXT_CYAN = "#00F5D4"
TEXT_BLUE = "#38BDF8"
TEXT_MUTED = "#94A3B8"
ACCENT_GREEN = "#10B981"
ACCENT_AMBER = "#F59E0B"
ACCENT_RED = "#EF4444"

def generate_introduction_visual():
    """Visual for Slide 2: Introduction Concept Visual (Urban transit delay to Z-transform solution)."""
    fig = plt.figure(figsize=(6.8, 7.2), facecolor=DARK_BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=DARK_BG)
    ax.axis('off')

    # Header Card
    hdr = patches.FancyBboxPatch((0.4, 6.4), 6.0, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=CARD_BG, edgecolor=BORDER_CYAN, linewidth=1.5)
    ax.add_patch(hdr)
    ax.text(3.4, 6.75, "INTELLIGENT TRANSIT SIGNAL PROCESSING", color=TEXT_WHITE,
            fontsize=11.5, weight='bold', ha='center', va='center')
    ax.text(3.4, 6.50, "From Urban Delay Volatility to Causal Z-Domain Modeling",
            color=TEXT_CYAN, fontsize=8.5, ha='center', va='center')

    # --- SECTION 1: Urban Transit Corridor & Delay Volatility ---
    s1_box = patches.FancyBboxPatch((0.4, 4.4), 6.0, 1.85, boxstyle="round,pad=0.08",
                                   facecolor=CARD_INNER, edgecolor=BORDER_BLUE, linewidth=1.2)
    ax.add_patch(s1_box)
    ax.text(0.6, 6.05, "1. URBAN TRANSIT CORRIDOR & DELAY PERTURBATIONS", color=TEXT_BLUE,
            fontsize=9.2, weight='bold')

    # Draw Road/Corridor
    road = patches.Rectangle((0.7, 4.85), 5.4, 0.45, facecolor="#1E293B", edgecolor="#475569", linewidth=1.0)
    ax.add_patch(road)
    # Dashed center line
    ax.plot([0.7, 6.1], [5.075, 5.075], color="#FBBF24", linestyle="--", linewidth=1.2, alpha=0.7)

    # Bus Stops along corridor
    stop_x = [1.2, 2.7, 4.2, 5.7]
    stop_names = ["Stop S[n-2]", "Stop S[n-1]", "Stop S[n]", "Stop S[n+1]"]
    delays = ["+0s", "+45s", "+140s (Shock)", "+185s"]
    for sx, sname, dval in zip(stop_x, stop_names, delays):
        # Stop shelter
        ax.scatter([sx], [5.38], color=TEXT_CYAN, s=60, marker="P")
        ax.text(sx, 5.52, sname, color=TEXT_WHITE, fontsize=7.2, ha='center', weight='bold')
        dcol = ACCENT_GREEN if "+0s" in dval else (ACCENT_RED if "Shock" in dval else ACCENT_AMBER)
        ax.text(sx, 4.65, f"Delay: {dval}", color=dcol, fontsize=7.2, ha='center', weight='bold')

    # Buses moving
    b1 = patches.Rectangle((1.8, 4.95), 0.55, 0.25, facecolor="#0284C7", edgecolor="#FFFFFF", linewidth=1.0)
    ax.add_patch(b1)
    ax.text(2.075, 5.075, "Bus 101", color="#FFFFFF", fontsize=6.8, ha='center', va='center', weight='bold')

    b2 = patches.Rectangle((3.4, 4.95), 0.55, 0.25, facecolor="#EF4444", edgecolor="#FFFFFF", linewidth=1.0)
    ax.add_patch(b2)
    ax.text(3.675, 5.075, "Bus 102", color="#FFFFFF", fontsize=6.8, ha='center', va='center', weight='bold')

    # Congestion shockwave annotation
    ax.annotate("Traffic Bottleneck\nShockwave Ripple", xy=(3.95, 5.075), xytext=(4.6, 5.38),
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.2),
                color=ACCENT_RED, fontsize=7.2, weight='bold', ha='center')

    # Arrow Down
    arr1 = patches.FancyArrowPatch((3.4, 4.35), (3.4, 4.10), arrowstyle='->', mutation_scale=15,
                                  color=BORDER_CYAN, linewidth=2)
    ax.add_patch(arr1)
    ax.text(3.55, 4.22, "Discrete Delay Extraction x[n]", color=TEXT_CYAN, fontsize=7.5)

    # --- SECTION 2: Signal Representation & Z-Transform Mapping ---
    s2_box = patches.FancyBboxPatch((0.4, 2.2), 6.0, 1.85, boxstyle="round,pad=0.08",
                                   facecolor=CARD_INNER, edgecolor=BORDER_CYAN, linewidth=1.2)
    ax.add_patch(s2_box)
    ax.text(0.6, 3.85, "2. DISCRETE-TIME SIGNAL TO COMPLEX Z-PLANE", color=TEXT_CYAN,
            fontsize=9.2, weight='bold')

    # Left: Discrete sequence plot x[n]
    ax_sub1 = fig.add_axes([0.10, 0.34, 0.36, 0.15], facecolor="#0B132B")
    n_pts = np.arange(0, 10)
    x_sig = np.array([0, 12, 45, 110, 140, 125, 95, 60, 35, 18])
    markerline, stemlines, baseline = ax_sub1.stem(n_pts, x_sig)
    plt.setp(stemlines, color=TEXT_CYAN, linewidth=1.2)
    plt.setp(markerline, color=TEXT_CYAN, markersize=3.5)
    plt.setp(baseline, color=BORDER_MUTED, linewidth=0.8)
    ax_sub1.set_title("Discrete Delay Sequence x[n]", color=TEXT_WHITE, fontsize=7.5, pad=3)
    ax_sub1.tick_params(colors=TEXT_MUTED, labelsize=6.5)
    ax_sub1.grid(True, linestyle=':', alpha=0.3, color='#334155')

    # Middle: Formula box
    ax.text(3.4, 3.10, r"$X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$" + "\n\n" + r"$H(z) = \frac{1}{1 - \sum a_k z^{-k}}$",
            color="#FFFFFF", fontsize=8.2, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#1E293B", edgecolor=BORDER_CYAN, lw=1.0))

    # Right: Unit Circle Pole plot
    ax_sub2 = fig.add_axes([0.56, 0.34, 0.34, 0.15], facecolor="#0B132B")
    uc = plt.Circle((0, 0), 1.0, fill=False, color=TEXT_CYAN, linestyle='--', linewidth=1.0)
    ax_sub2.add_artist(uc)
    ax_sub2.scatter([-0.106, -0.106, -0.157], [0.605, -0.605, 0.0], color=ACCENT_RED, marker='x', s=35, linewidth=1.5)
    ax_sub2.axhline(0, color=BORDER_MUTED, lw=0.6)
    ax_sub2.axvline(0, color=BORDER_MUTED, lw=0.6)
    ax_sub2.set_xlim(-1.4, 1.4)
    ax_sub2.set_ylim(-1.4, 1.4)
    ax_sub2.set_aspect('equal')
    ax_sub2.set_title("Unit Circle Stability (|p|<1)", color=TEXT_WHITE, fontsize=7.5, pad=3)
    ax_sub2.tick_params(colors=TEXT_MUTED, labelsize=6)

    # Arrow Down
    arr2 = patches.FancyArrowPatch((3.4, 2.15), (3.4, 1.90), arrowstyle='->', mutation_scale=15,
                                  color=BORDER_PURPLE, linewidth=2)
    ax.add_patch(arr2)
    ax.text(3.55, 2.02, "Inverse Z-Transform Inversion", color=BORDER_PURPLE, fontsize=7.5)

    # --- SECTION 3: Real-Time Operational Output ---
    s3_box = patches.FancyBboxPatch((0.4, 0.25), 6.0, 1.60, boxstyle="round,pad=0.08",
                                   facecolor=CARD_INNER, edgecolor=BORDER_PURPLE, linewidth=1.2)
    ax.add_patch(s3_box)
    ax.text(0.6, 1.65, "3. PASSENGER ETA ESTIMATION & CONFIDENCE BOUNDS", color=BORDER_PURPLE,
            fontsize=9.2, weight='bold')

    # Card 1: Countdown Output
    c1 = patches.FancyBboxPatch((0.6, 0.45), 2.7, 1.05, boxstyle="round,pad=0.08",
                               facecolor="#0B132B", edgecolor=BORDER_CYAN, linewidth=1.0)
    ax.add_patch(c1)
    ax.text(1.95, 1.25, "DIGITAL COUNTDOWN", color=TEXT_MUTED, fontsize=7.2, ha='center', weight='bold')
    ax.text(1.95, 0.95, "05 : 42", color=TEXT_CYAN, fontsize=15, ha='center', weight='bold')
    ax.text(1.95, 0.65, "95% CI: [05:15 — 06:09]", color=ACCENT_GREEN, fontsize=7.5, ha='center', weight='bold')

    # Card 2: Performance Gain
    c2 = patches.FancyBboxPatch((3.5, 0.45), 2.7, 1.05, boxstyle="round,pad=0.08",
                               facecolor="#0B132B", edgecolor=ACCENT_GREEN, linewidth=1.0)
    ax.add_patch(c2)
    ax.text(4.85, 1.25, "BENCHMARK ACCURACY", color=TEXT_MUTED, fontsize=7.2, ha='center', weight='bold')
    ax.text(4.85, 0.95, "-47.0% ERROR", color=ACCENT_GREEN, fontsize=14, ha='center', weight='bold')
    ax.text(4.85, 0.65, "MAE: 7.85s vs Kinematic 14.80s", color=TEXT_WHITE, fontsize=7.5, ha='center')

    out_path = os.path.join(SCREENSHOTS_DIR, "introduction_concept_visual.png")
    plt.savefig(out_path, dpi=200, facecolor=DARK_BG)
    plt.close()
    print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

def generate_system_architecture_advanced():
    """Figure 8: Slide 7 Publication-Grade System Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(10.5, 5.8), facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)

    # Title & Subtitle inside plot
    ax.text(5.25, 5.50, "SYSTEM ARCHITECTURE & INTEGRATED DATA PIPELINE",
            color=TEXT_WHITE, fontsize=13, weight='bold', ha='center')
    ax.text(5.25, 5.22, "End-to-End Three-Tier Architecture: Real-Time Ingestion → Z-Transform Engine → Passenger Operations",
            color=TEXT_CYAN, fontsize=9.2, ha='center')

    # 3 Primary Module Container Columns
    # Module 1 Box
    m1_box = patches.FancyBboxPatch((0.4, 0.4), 2.9, 4.6, boxstyle="round,pad=0.15",
                                    facecolor=CARD_BG, edgecolor=BORDER_BLUE, linewidth=1.8)
    ax.add_patch(m1_box)
    # Header 1
    h1 = patches.FancyBboxPatch((0.55, 4.45), 2.6, 0.45, boxstyle="round,pad=0.08",
                               facecolor="#0B2545", edgecolor=BORDER_BLUE, linewidth=1.2)
    ax.add_patch(h1)
    ax.text(1.85, 4.67, "MODULE 1: DATA PIPELINE", color=TEXT_WHITE, fontsize=9.5, weight='bold', ha='center', va='center')

    # Module 1 Inner Component Cards
    m1_cards = [
        ("Fleet Telemetry Ingestion", "15 active buses, 5 corridors\nGPS lat/lon, speed, heading, load", "#0D1E38"),
        ("Spatial Geodesic Engine", "Haversine great-circle distance\nDynamic compass bearing math", "#0D1E38"),
        ("2D State-Space Kalman Filter", "CV model [x, y, vx, vy]^T\nSuppresses multipath noise (4.8m)", "#082640"),
        ("Hampel Outlier Rejection", "3x MAD sliding-window filter\nPurges impulsive dropouts (22 dB)", "#082640"),
        ("Discrete Time Resampling", "Standardized delay sequence s[n]\nMean-centered station dwell times", "#082640")
    ]
    for i, (title, desc, bg) in enumerate(m1_cards):
        y = 3.65 - i * 0.76
        c = patches.FancyBboxPatch((0.55, y), 2.6, 0.65, boxstyle="round,pad=0.08",
                                  facecolor=bg, edgecolor="#1E3A5F", linewidth=1.0)
        ax.add_patch(c)
        ax.text(0.70, y + 0.45, f"1.{i+1} {title}", color=TEXT_BLUE, fontsize=8.2, weight='bold')
        ax.text(0.70, y + 0.20, desc, color=TEXT_MUTED, fontsize=6.8)

    # Connecting Arrow 1 -> 2
    arr1 = patches.FancyArrowPatch((3.35, 2.7), (3.75, 2.7), arrowstyle='->', mutation_scale=18,
                                  color=BORDER_CYAN, linewidth=2.5)
    ax.add_patch(arr1)
    ax.text(3.55, 2.92, "s[n]\nClean Signal", color=TEXT_CYAN, fontsize=7.2, ha='center', weight='bold')

    # Module 2 Box
    m2_box = patches.FancyBboxPatch((3.8, 0.4), 2.9, 4.6, boxstyle="round,pad=0.15",
                                    facecolor=CARD_BG, edgecolor=BORDER_CYAN, linewidth=1.8)
    ax.add_patch(m2_box)
    # Header 2
    h2 = patches.FancyBboxPatch((3.95, 4.45), 2.6, 0.45, boxstyle="round,pad=0.08",
                               facecolor="#053238", edgecolor=BORDER_CYAN, linewidth=1.2)
    ax.add_patch(h2)
    ax.text(5.25, 4.67, "MODULE 2: Z-TRANSFORM CORE", color=TEXT_WHITE, fontsize=9.5, weight='bold', ha='center', va='center')

    # Module 2 Inner Component Cards
    m2_cards = [
        ("Toeplitz Autocorrelation", "Sample autocorrelation R_ss(k)\nSymmetric positive-definite matrix", "#062A30"),
        ("Yule-Walker System ID", "Solves R_ss * a = r_ss\nOptimal AR(p) model order p=3", "#062A30"),
        ("Transfer Function H(z)", "Rational H(z) = 1 / (1 - sum a_k z^-k)\nRoots of characteristic poly A(z)", "#062A30"),
        ("Unit-Circle BIBO Stability", "Verifies |p_k| < 1.0 (p=0.614)\nGuarantees bounded error drift", "#053B34"),
        ("Analytical Inverse Z-Transform", "Partial fractions h[n] = sum R_k p_k^n\nClosed-form 95% Confidence Intervals", "#053B34")
    ]
    for i, (title, desc, bg) in enumerate(m2_cards):
        y = 3.65 - i * 0.76
        c = patches.FancyBboxPatch((3.95, y), 2.6, 0.65, boxstyle="round,pad=0.08",
                                  facecolor=bg, edgecolor="#0E4E57", linewidth=1.0)
        ax.add_patch(c)
        ax.text(4.10, y + 0.45, f"2.{i+1} {title}", color=TEXT_CYAN, fontsize=8.2, weight='bold')
        ax.text(4.10, y + 0.20, desc, color=TEXT_MUTED, fontsize=6.8)

    # Connecting Arrow 2 -> 3
    arr2 = patches.FancyArrowPatch((6.75, 2.7), (7.15, 2.7), arrowstyle='->', mutation_scale=18,
                                  color=BORDER_PURPLE, linewidth=2.5)
    ax.add_patch(arr2)
    ax.text(6.95, 2.92, "ETA + CI\nForecast", color=BORDER_PURPLE, fontsize=7.2, ha='center', weight='bold')

    # Module 3 Box
    m3_box = patches.FancyBboxPatch((7.2, 0.4), 2.9, 4.6, boxstyle="round,pad=0.15",
                                    facecolor=CARD_BG, edgecolor=BORDER_PURPLE, linewidth=1.8)
    ax.add_patch(m3_box)
    # Header 3
    h3 = patches.FancyBboxPatch((7.35, 4.45), 2.6, 0.45, boxstyle="round,pad=0.08",
                               facecolor="#2A1B4E", edgecolor=BORDER_PURPLE, linewidth=1.2)
    ax.add_patch(h3)
    ax.text(8.65, 4.67, "MODULE 3: PASSENGER DASHBOARD", color=TEXT_WHITE, fontsize=9.5, weight='bold', ha='center', va='center')

    # Module 3 Inner Component Cards
    m3_cards = [
        ("Transit Geospatial Map", "Folium dark-matter tiles\nLive vehicle vectors & stop nodes", "#1F143D"),
        ("Live Digital Countdown", "Real-time clock (MM:SS)\nSub-second refresh (<150 ms)", "#1F143D"),
        ("Dynamic Status Classification", "On-Time (±60s), Minor Delay,\nSevere Delay (>4m) alert badges", "#1F143D"),
        ("Analytical Uncertainty Display", "Honest 95% CI [T_low — T_high]\nRestores passenger trust", "#29134D"),
        ("Contextual Transit Advisories", "Proactive traffic incident alerts\nWeather and headway notifications", "#29134D")
    ]
    for i, (title, desc, bg) in enumerate(m3_cards):
        y = 3.65 - i * 0.76
        c = patches.FancyBboxPatch((7.35, y), 2.6, 0.65, boxstyle="round,pad=0.08",
                                  facecolor=bg, edgecolor="#4B2A8A", linewidth=1.0)
        ax.add_patch(c)
        ax.text(7.50, y + 0.45, f"3.{i+1} {title}", color="#A78BFA", fontsize=8.2, weight='bold')
        ax.text(7.50, y + 0.20, desc, color=TEXT_MUTED, fontsize=6.8)

    # Global Database Bar at Bottom
    db_box = patches.FancyBboxPatch((0.4, 0.05), 9.7, 0.30, boxstyle="round,pad=0.04",
                                   facecolor="#0B132B", edgecolor="#334155", linewidth=1.0)
    ax.add_patch(db_box)
    ax.text(5.25, 0.20, "Persistence Layer: SQLite Database (transport.db) • Routes, Stops, Fleet Telemetry, Historical Traversal Records, Prediction Logs",
            color=TEXT_MUTED, fontsize=7.5, ha='center', va='center')

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(SCREENSHOTS_DIR, "system_architecture_diagram.png")
    plt.savefig(out_path, dpi=200, facecolor=DARK_BG)
    plt.close()
    print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    print("Generating custom diagrams for Introduction and System Architecture...")
    generate_introduction_visual()
    generate_system_architecture_advanced()
    print("All visuals generated successfully!")
