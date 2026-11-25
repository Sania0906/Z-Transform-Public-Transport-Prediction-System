"""
Generate dedicated non-module conceptual visuals for:
1. Slide 3: Problem Statement (Urban multipath, congestion shockwaves, error accumulation)
2. Slide 5: Objective & Research Contributions (5 Core Pillars Architecture Card)
3. Slide 6: Existing vs Proposed System (Side-by-side comparison matrix with checkmarks and crosses)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "assets", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

DARK_BG = "#0A0F1D"
CARD_BG = "#131B2E"
BORDER_C = "#1E2D4A"
CYAN = "#00F5D4"
BLUE = "#00B4D8"
RED = "#EF476F"
GREEN = "#10B981"
TEXT_COLOR = "#F0F4F8"
MUTED = "#94A3B8"
YELLOW = "#FFB703"

def generate_problem_statement_visual():
    """Visual for Slide 3: Transit Challenges (Multipath GPS, Delay Waves, Error Drift)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 6.8), facecolor=DARK_BG)
    ax1.set_facecolor(CARD_BG)
    ax2.set_facecolor(CARD_BG)

    # Subplot 1: Urban Canyon GPS Multipath Reflection Illustration
    ax1.set_title("Urban Canyon Multipath GPS Error", color=TEXT_COLOR, fontsize=11, weight='bold', pad=8)
    # Draw buildings
    bldg1 = patches.Rectangle((0.1, 0.1), 0.25, 0.75, facecolor="#1E293B", edgecolor="#38BDF8", linewidth=1.5)
    bldg2 = patches.Rectangle((0.65, 0.1), 0.25, 0.75, facecolor="#1E293B", edgecolor="#38BDF8", linewidth=1.5)
    ax1.add_patch(bldg1)
    ax1.add_patch(bldg2)
    ax1.text(0.225, 0.45, "High-Rise\nBuilding A", color="#94A3B8", fontsize=8, ha='center', va='center')
    ax1.text(0.775, 0.45, "High-Rise\nBuilding B", color="#94A3B8", fontsize=8, ha='center', va='center')

    # Satellite at top
    ax1.scatter([0.5], [0.92], color="#FBBF24", s=180, marker="*")
    ax1.text(0.5, 0.96, "GPS Satellite", color="#FBBF24", fontsize=9, ha='center', weight='bold')

    # Bus on street level
    bus = patches.Rectangle((0.42, 0.12), 0.16, 0.08, facecolor="#0284C7", edgecolor="#FFFFFF", linewidth=1.2)
    ax1.add_patch(bus)
    ax1.text(0.5, 0.16, "Bus", color="#FFFFFF", fontsize=8, ha='center', va='center', weight='bold')

    # Direct ray (blocked)
    ax1.plot([0.5, 0.45], [0.88, 0.20], color="#EF4444", linestyle=":", linewidth=1.8, label="Direct LOS Blocked")
    # Multipath reflection
    ax1.plot([0.5, 0.65], [0.88, 0.65], color="#38BDF8", linestyle="--", linewidth=1.8)
    ax1.plot([0.65, 0.50], [0.65, 0.20], color="#38BDF8", linestyle="--", linewidth=1.8, label="Multipath Reflection")
    ax1.scatter([0.65], [0.65], color="#38BDF8", s=40)
    ax1.text(0.5, 0.04, "Multipath Coordinate Jitter: 30-50m Error", color=RED, fontsize=8.5, ha='center', weight='bold')

    ax1.set_xlim(0, 1.0)
    ax1.set_ylim(0, 1.0)
    ax1.axis('off')
    legend1 = ax1.legend(loc="upper right", facecolor=DARK_BG, edgecolor=BORDER_C, fontsize=7.5)
    for t in legend1.get_texts(): t.set_color(TEXT_COLOR)

    # Subplot 2: Error Accumulation: Unbounded Drift vs Stable Z-Transform
    ax2.set_title("Multi-Stop Recursive Forecast Error Accumulation", color=TEXT_COLOR, fontsize=11, weight='bold', pad=8)
    stops = np.arange(1, 9)
    # Unconstrained divergent model: error grows exponentially
    unconstrained_err = 5.0 * (1.28 ** stops)
    # Stable Z-Transform bounded error
    z_transform_err = 6.0 + 1.2 * np.log(stops)

    ax2.plot(stops, unconstrained_err, color=RED, marker='s', linewidth=2.2, label="Unconstrained ML / Neural Model (Error Explosion)")
    ax2.plot(stops, z_transform_err, color=CYAN, marker='o', linewidth=2.5, label="Z-Transform (|p| < 1.0) Bounded Error")
    ax2.axhline(25.0, color=YELLOW, linestyle="--", linewidth=1.2, label="Passenger Acceptance Threshold (25s)")

    ax2.set_xlabel("Multi-Stop Prediction Horizon (Number of Stops Ahead)", color=MUTED, fontsize=8.5)
    ax2.set_ylabel("Forecast Error (seconds)", color=MUTED, fontsize=8.5)
    ax2.tick_params(colors=MUTED, labelsize=8)
    ax2.grid(True, linestyle=':', alpha=0.3, color='#334155')
    legend2 = ax2.legend(loc="upper left", facecolor=DARK_BG, edgecolor=BORDER_C, fontsize=7.5)
    for t in legend2.get_texts(): t.set_color(TEXT_COLOR)

    plt.tight_layout()
    out_path = os.path.join(SCREENSHOTS_DIR, "problem_statement_visual.png")
    plt.savefig(out_path, dpi=200, facecolor=DARK_BG)
    plt.close()
    print(f"Generated {out_path}")

def generate_objectives_visual():
    """Visual for Slide 5: 5 Core Research Innovation Pillars."""
    fig, ax = plt.subplots(figsize=(6.5, 6.8), facecolor=DARK_BG)
    ax.set_facecolor(CARD_BG)

    ax.set_title("RESEARCH INNOVATION & METHODOLOGY PILLARS", color=TEXT_COLOR, fontsize=12, weight='bold', pad=14)

    pillars = [
        ("PILLAR 1: SPATIAL 2D KALMAN DENOISING", "Constant-velocity state space [x, y, vx, vy]^T suppresses\nurban canyon multipath jitter (68.4% error reduction).", "#0284C7"),
        ("PILLAR 2: YULE-WALKER TRANSFER FUNCTION H(z)", "Autoregressive delay modeling s[n] = sum a_k s[n-k] + w[n]\nsolved via Toeplitz autocorrelation matrix inversion.", "#00B4D8"),
        ("PILLAR 3: COMPLEX POLE BIBO STABILITY", "Roots of characteristic polynomial A(z) mathematically\nconstrained strictly inside the unit circle (|p_k| < 1.0).", "#00F5D4"),
        ("PILLAR 4: INVERSE Z-TRANSFORM VIA RESIDUES", "Partial fraction expansion yields exact impulse response h[n]\nand closed-form 95% analytical confidence intervals.", "#7C4DFF"),
        ("PILLAR 5: REAL-TIME PASSENGER OPERATIONS", "Sub-second ETA generation (<150ms) with live countdown\nclock, delay status pills, and contextual service alerts.", "#10B981")
    ]

    for i, (title, desc, border_col) in enumerate(pillars):
        y = 4.8 - i * 1.15
        # Draw box
        box = patches.FancyBboxPatch((0.4, y), 5.7, 0.95, boxstyle="round,pad=0.12",
                                    facecolor="#0B132B", edgecolor=border_col, linewidth=1.8)
        ax.add_patch(box)
        # Pillar number badge
        badge = patches.Circle((0.85, y + 0.48), 0.30, facecolor=border_col)
        ax.add_patch(badge)
        ax.text(0.85, y + 0.48, str(i + 1), color="#0F172A", fontsize=11, weight='bold', ha='center', va='center')

        # Title & desc
        ax.text(1.35, y + 0.65, title, color="#FFFFFF", fontsize=9.2, weight='bold')
        ax.text(1.35, y + 0.25, desc, color=MUTED, fontsize=8.0, va='center')

    ax.set_xlim(0, 6.5)
    ax.set_ylim(-0.2, 5.8)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(SCREENSHOTS_DIR, "objectives_visual.png")
    plt.savefig(out_path, dpi=200, facecolor=DARK_BG)
    plt.close()
    print(f"Generated {out_path}")

def generate_existing_vs_proposed_visual():
    """Visual for Slide 6: Existing Systems vs Proposed System Comparison Matrix."""
    fig, ax = plt.subplots(figsize=(6.5, 6.8), facecolor=DARK_BG)
    ax.set_facecolor(CARD_BG)

    ax.set_title("TECHNOLOGY COMPARISON MATRIX", color=TEXT_COLOR, fontsize=12, weight='bold', pad=14)

    # Headers
    h1 = patches.FancyBboxPatch((0.2, 5.0), 2.9, 0.55, boxstyle="round,pad=0.08", facecolor="#1e1b2e", edgecolor=RED, linewidth=1.5)
    h2 = patches.FancyBboxPatch((3.4, 5.0), 2.9, 0.55, boxstyle="round,pad=0.08", facecolor="#0e2a27", edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(h1)
    ax.add_patch(h2)
    ax.text(1.65, 5.28, "EXISTING SYSTEMS", color="#FFA69E", fontsize=9.5, weight='bold', ha='center', va='center')
    ax.text(4.85, 5.28, "PROPOSED Z-TRANSFORM", color="#A7F3D0", fontsize=9.5, weight='bold', ha='center', va='center')

    rows = [
        ("Static Timetables / d/v", "Dynamic Transfer Function H(z)", "System Model"),
        ("None (Unbounded Error)", "BIBO Stability (|p| < 1.0)", "Stability Proof"),
        ("Raw GPS (30-50m Error)", "2D Kalman Filter (4.8m)", "Sensor Denoising"),
        ("Point Estimate Only", "Closed-Form 95% CI", "Uncertainty Bounds"),
        ("High GPU Footprint", "Lightweight (<150 ms)", "Edge Execution")
    ]

    for i, (exist_t, prop_t, dim_t) in enumerate(rows):
        y = 4.15 - i * 0.98

        # Left existing card
        c_left = patches.FancyBboxPatch((0.2, y), 2.9, 0.82, boxstyle="round,pad=0.08", facecolor="#131B2E", edgecolor="#334155", linewidth=1.0)
        ax.add_patch(c_left)
        ax.text(0.45, y + 0.52, f"✗  {exist_t}", color=RED, fontsize=8.5, weight='bold')
        ax.text(0.45, y + 0.22, f"Feature: {dim_t}", color=MUTED, fontsize=7.5)

        # Right proposed card
        c_right = patches.FancyBboxPatch((3.4, y), 2.9, 0.82, boxstyle="round,pad=0.08", facecolor="#0c1d2e", edgecolor=CYAN, linewidth=1.2)
        ax.add_patch(c_right)
        ax.text(3.65, y + 0.52, f"✓  {prop_t}", color=GREEN, fontsize=8.5, weight='bold')
        ax.text(3.65, y + 0.22, f"Feature: {dim_t}", color=CYAN, fontsize=7.5)

    ax.set_xlim(0, 6.5)
    ax.set_ylim(-0.2, 5.8)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(SCREENSHOTS_DIR, "existing_vs_proposed_visual.png")
    plt.savefig(out_path, dpi=200, facecolor=DARK_BG)
    plt.close()
    print(f"Generated {out_path}")

if __name__ == '__main__':
    print("Generating dedicated conceptual visuals for Slides 3, 5, 6...")
    generate_problem_statement_visual()
    generate_objectives_visual()
    generate_existing_vs_proposed_visual()
    print("All dedicated non-module visuals generated successfully!")
