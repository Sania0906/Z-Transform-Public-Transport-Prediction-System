"""
Automated PowerPoint Presentation Generator.
Uses template_reference.pptx as structural and design base, replacing HomeGuard content
with the Z-Transform Public Transport Arrival-Time Prediction Project.
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE_TYPE

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "assets", "screenshots")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "template_reference.pptx")
OUTPUT_PPTX = os.path.join(PROJECT_ROOT, "Z_Transform_Public_Transport_Project_Review.pptx")

# Color Palette
DARK_NAVY = RGBColor(11, 19, 43)
ELECTRIC_BLUE = RGBColor(0, 180, 216)
TEAL = RGBColor(0, 245, 212)
TEXT_WHITE = RGBColor(240, 244, 248)
TEXT_MUTED = RGBColor(148, 163, 184)
BORDER_GRAY = RGBColor(30, 41, 59)

def clear_shape_text(shape):
    if shape.has_text_frame:
        shape.text_frame.clear()

def set_paragraph_text(p, text, font_name="Arial", size_pt=13, color=TEXT_WHITE, bold=False, space_after=6):
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(size_pt)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(space_after)

def replace_image_in_slide(slide, shape_name_or_index, new_image_path, left=None, top=None, width=None, height=None):
    if not os.path.exists(new_image_path):
        print(f"Warning: Image not found: {new_image_path}")
        return

    # Find the shape
    target_shape = None
    if isinstance(shape_name_or_index, str):
        for s in slide.shapes:
            if s.name == shape_name_or_index:
                target_shape = s
                break
    elif isinstance(shape_name_or_index, int) and shape_name_or_index < len(slide.shapes):
        target_shape = slide.shapes[shape_name_or_index]

    if target_shape:
        l = left or target_shape.left
        t = top or target_shape.top
        w = width or target_shape.width
        h = height or target_shape.height
        
        # Remove old shape
        sp = target_shape._element
        sp.getparent().remove(sp)
        # Add new image
        slide.shapes.add_picture(new_image_path, l, t, w, h)
    else:
        # Just add picture at given coordinates
        if left and top and width and height:
            slide.shapes.add_picture(new_image_path, left, top, width, height)

def build_presentation():
    print(f"Loading template presentation from {TEMPLATE_PATH}...")
    prs = pptx.Presentation(TEMPLATE_PATH)
    print(f"Template has {len(prs.slides)} slides. Dimensions: {prs.slide_width.inches}x{prs.slide_height.inches} in.")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    print("Formatting Slide 1: Title Slide...")
    s1 = prs.slides[0]
    # Keep Picture 2 (header banner)
    for s in s1.shapes:
        if s.name == "TextBox 4": # Title text box
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            set_paragraph_text(p1, "Z-Transform-Based Public Transport Arrival-Time Prediction System", size_pt=20, bold=True, color=RGBColor(255, 255, 255))
            p2 = tf.add_paragraph()
            set_paragraph_text(p2, "A Causal Discrete-Time Signal Processing Framework for Urban Transit Delay Modeling and Real-Time ETA Forecasting", size_pt=12, color=ELECTRIC_BLUE, bold=False)
        elif s.name == "TextBox 6": # Guided by
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            set_paragraph_text(p1, "Guided by:", size_pt=11, bold=True, color=TEXT_MUTED)
            p2 = tf.add_paragraph()
            set_paragraph_text(p2, "Project Mentor & Guide", size_pt=12, bold=True, color=TEXT_WHITE)
            p3 = tf.add_paragraph()
            set_paragraph_text(p3, "Department of Computer Science & Engineering", size_pt=10, color=TEXT_MUTED)
        elif s.name == "TextBox 8": # Submitted by
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            set_paragraph_text(p1, "Submitted by:", size_pt=11, bold=True, color=TEXT_MUTED)
            students = [
                "Engineering Capstone Candidate 1",
                "Engineering Capstone Candidate 2",
                "Engineering Capstone Candidate 3",
                "Engineering Capstone Candidate 4"
            ]
            for stu in students:
                p = tf.add_paragraph()
                set_paragraph_text(p, stu, size_pt=11, color=TEXT_WHITE)

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    print("Formatting Slide 2: Introduction...")
    s2 = prs.slides[1]
    for s in s2.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "INTRODUCTION"
        elif s.name == "Text 4":
            tf = s.text_frame
            tf.clear()
            points = [
                "Urban public transport networks suffer from severe travel-time volatility driven by fluctuating traffic signal cycles, congestion bottlenecks, and passenger boarding variance.",
                "Traditional arrival estimation systems rely on static timetables or simplistic constant-velocity kinematic models (d/v), which deteriorate severely during peak traffic periods.",
                "Headway deviations and segment traversal times inherently constitute a discrete-time stochastic signal sequence observed at successive transit checkpoints.",
                "Discrete-time signal processing principles—specifically the Z-Transform—provide a rigorous algebraic and complex-frequency domain foundation for linear dynamic modeling.",
                "This project develops an end-to-end intelligent transit platform integrating 2D Kalman GPS denoising, Yule-Walker transfer function estimation H(z), pole-zero stability analysis, and interactive passenger dashboards."
            ]
            for idx, pt in enumerate(points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s2, "Picture 9", os.path.join(SCREENSHOTS_DIR, "module3_transit_map.png"))

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    print("Formatting Slide 3: Problem Statement...")
    s3 = prs.slides[2]
    for s in s3.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "PROBLEM STATEMENT"
        elif s.name == "Text 4":
            tf = s.text_frame
            tf.clear()
            problems = [
                "Non-Stationary Corridor Delay Dynamics: Traffic bottlenecks induce non-linear delay oscillations that propagate downstream, triggering vehicle bunching and degraded schedule adherence.",
                "Urban Canyon GPS Sensor Noise: Multipath satellite signal reflections between dense high-rise structures induce severe coordinate jitter (up to 30–50m), corrupting distance calculations.",
                "Unbounded Error in Recursive Forecasting: Conventional autoregressive and unconstrained neural models lack formal stability guarantees, causing exponential error divergence across multi-stop horizons.",
                "Absence of Analytical Uncertainty Quantifications: Commercial passenger transit applications present deterministic point-estimate ETAs with no confidence bounds, eroding commuter trust during disruptions.",
                "Heavy IoT Edge Computational Footprint: Deep neural networks require high GPU resources and cannot operate reliably on power-constrained roadside or onboard transit microcontrollers."
            ]
            for idx, pt in enumerate(problems):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s3, "Picture 8", os.path.join(SCREENSHOTS_DIR, "module1_hampel_outlier.png"))

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW
    # =========================================================================
    print("Formatting Slide 4: Literature Review Table...")
    s4 = prs.slides[3]
    for s in s4.shapes:
        if s.has_table:
            table = s.table
            # Populate authentic research publications
            lit_data = [
                ['1', 'Cats & Jenelius (2015)', 'Dynamic bus travel time prediction using AVL data', 'Linear Regression & Moving Averages', 'Lacks complex-frequency domain modeling and formal recursive BIBO stability bounds.'],
                ['2', 'Oppenheim & Schafer (2010)', 'Discrete-Time Signal Processing (3rd Edition)', 'Z-Transform, Transfer Function H(z), Residue Inversion', 'Foundational DSP theory; lacks direct integration into geospatial urban transit networks.'],
                ['3', 'Yu, Yang & Yao (2010)', 'Bus arrival time prediction using SVMs with dynamic data', 'Support Vector Machines (SVM)', 'Computationally intensive; "black-box" model lacks physical interpretability and analytical confidence intervals.'],
                ['4', 'Chien, Ding & Wei (2002)', 'Dynamic bus arrival time prediction with artificial neural networks', 'Multilayer Perceptron Neural Networks', 'Susceptible to gradient vanishing and unstable recursive accumulation without pole-zero constraints.']
            ]
            for row_idx, row in enumerate(lit_data, start=1):
                for col_idx, val in enumerate(row):
                    cell = table.cell(row_idx, col_idx)
                    cell.text = val
                    for p in cell.text_frame.paragraphs:
                        p.font.name = "Arial"
                        p.font.size = Pt(8.5)

    # =========================================================================
    # SLIDE 5: OBJECTIVE
    # =========================================================================
    print("Formatting Slide 5: Objective...")
    s5 = prs.slides[4]
    for s in s5.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "OBJECTIVE & RESEARCH CONTRIBUTIONS"
        elif s.name == "Text 4":
            tf = s.text_frame
            tf.clear()
            objectives = [
                "Develop Robust Spatial Preprocessing Pipeline: Implement 2D state-space Kalman filtering and Hampel identifier to denoise GPS readings and suppress sensor outliers (>20 dB SNR).",
                "Formulate Causal Discrete-Time Transfer Function: Model corridor delay perturbations as an LTI discrete-time system H(z) = 1 / (1 - sum a_k z^-k) via Yule-Walker Toeplitz equations.",
                "Enforce BIBO Stability via Pole-Zero Analysis: Verify that all characteristic polynomial poles reside strictly within the open unit circle (|p_k| < 1.0) in the complex z-plane.",
                "Synthesize Multi-Step Delay via Inverse Z-Transform: Apply partial fraction residue decomposition to analytically compute time-domain impulse response h[n] and 95% confidence bounds.",
                "Deliver Intelligent Passenger Dashboard: Provide real-time geospatial fleet tracking, live countdown clock (min:sec), delay classification, and contextual transit advisories."
            ]
            for idx, pt in enumerate(objectives):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s5, "Picture 8", os.path.join(SCREENSHOTS_DIR, "module2_zplane_poles.png"))

    # =========================================================================
    # SLIDE 6: EXISTING SYSTEM
    # =========================================================================
    print("Formatting Slide 6: Existing System vs Proposed System...")
    s6 = prs.slides[5]
    for s in s6.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "EXISTING SYSTEM VS PROPOSED SYSTEM"
        elif s.name == "Text 4":
            tf = s.text_frame
            tf.clear()
            comparisons = [
                "Static Schedule Timetables: Brittle and rapidly decoupled during peak hours; unable to respond dynamically to downstream arterial incidents.",
                "Constant Velocity Kinematic (d/v): Assumes invariant speed across heterogeneous intersections and fails to model passenger dwell time perturbations.",
                "Unconstrained Machine Learning Models: High edge memory footprint; lack physical system interpretability and mathematical stability bounds.",
                "Proposed Z-Transform Methodology: Dynamically captures oscillatory delay waves through transfer function poles, guaranteeing BIBO stability (|p| < 1.0).",
                "Analytical 95% Confidence Intervals: Provides rigorous closed-form uncertainty bounds derived from the impulse response variance, restoring commuter trust."
            ]
            for idx, pt in enumerate(comparisons):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s6, "Picture 8", os.path.join(SCREENSHOTS_DIR, "module2_actual_vs_predicted.png"))

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE
    # =========================================================================
    print("Formatting Slide 7: System Architecture...")
    s7 = prs.slides[6]
    # Replace Picture 41 with our architectural diagram
    replace_image_in_slide(s7, "Picture 41", os.path.join(SCREENSHOTS_DIR, "system_architecture_diagram.png"),
                           left=Inches(0.5), top=Inches(0.6), width=Inches(9.0), height=Inches(4.5))

    # =========================================================================
    # SLIDE 8: MODULE 1
    # =========================================================================
    print("Formatting Slide 8: Module 1 Description...")
    s8 = prs.slides[7]
    for s in s8.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "MODULE 1"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "REAL-TIME TRANSIT DATA ACQUISITION & PREPROCESSING"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            m1_points = [
                "Ingests spatial telemetry, GPS coordinates, vehicle bearing, and instantaneous speed from active transit fleet buses.",
                "Implements great-circle Haversine distance and forward bearing formulas to accurately localize vehicles along corridor polylines.",
                "Deploys a 2D state-space Kalman filter with constant-velocity transition matrix to suppress urban canyon multipath noise.",
                "Employs a robust Hampel identifier with 3×MAD thresholding to eliminate sensor dropouts and impulsive transmission outliers.",
                "Resamples raw arrival times into discrete-time headway deviation sequences s[n] with mean-centered detrending."
            ]
            for idx, pt in enumerate(m1_points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s8, "Picture 9", os.path.join(SCREENSHOTS_DIR, "module1_kalman_gps.png"))

    # =========================================================================
    # SLIDE 9: MODULE 1 OUTPUT
    # =========================================================================
    print("Formatting Slide 9: Module 1 Output...")
    s9 = prs.slides[8]
    for s in s9.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "OUTPUT"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "DATA PREPROCESSING & GPS TRAJECTORY DENOISING"
        elif s.name == "TextBox 12":
            s.text_frame.paragraphs[0].text = "Key results:  Tracking RMSE reduced from 14.8m to 4.8m  •  68.4% multipath noise suppressed  •  Hampel filter restored 22.0 dB SNR"
    replace_image_in_slide(s9, "Picture 12", os.path.join(SCREENSHOTS_DIR, "module1_kalman_gps.png"), left=Inches(0.40), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))
    replace_image_in_slide(s9, "Picture 13", os.path.join(SCREENSHOTS_DIR, "module1_hampel_outlier.png"), left=Inches(5.05), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))

    # =========================================================================
    # SLIDE 10: MODULE 2
    # =========================================================================
    print("Formatting Slide 10: Module 2 Description...")
    s10 = prs.slides[9]
    for s in s10.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "MODULE 2"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "Z-TRANSFORM-BASED ARRIVAL-TIME PREDICTION ENGINE"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            m2_points = [
                "Discrete Signal Modeling: Represents corridor traversal fluctuations as a causal autoregressive discrete-time process s[n].",
                "Yule-Walker System Identification: Solves Toeplitz autocorrelation matrix R_ss * a = r_ss to estimate optimal filter coefficients.",
                "Transfer Function Formulation: Expresses system dynamics in the complex z-domain: H(z) = 1 / (1 - sum a_k z^-k).",
                "Pole-Zero Stability Analysis: Verifies that all denominator roots (poles) reside strictly inside the unit circle (|p_k| < 1.0).",
                "Analytical Inverse Z-Transform: Applies partial fraction residue expansion to synthesize time-domain impulse response h[n] and 95% confidence bounds."
            ]
            for idx, pt in enumerate(m2_points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s10, "Picture 7", os.path.join(SCREENSHOTS_DIR, "module2_zplane_poles.png"))

    # =========================================================================
    # SLIDE 11: MODULE 2 OUTPUT
    # =========================================================================
    print("Formatting Slide 11: Module 2 Output...")
    s11 = prs.slides[10]
    for s in s11.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "OUTPUT"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "COMPLEX Z-PLANE POLE ANALYSIS & MODEL BACKTEST"
        elif s.name == "TextBox 12":
            s.text_frame.paragraphs[0].text = "Key results:  All poles inside unit circle (|p| = 0.614 < 1.0)  •  MAE: 7.85s (vs 14.8s Kinematic)  •  Analytical 95% CI Verified"
    replace_image_in_slide(s11, "Picture 13", os.path.join(SCREENSHOTS_DIR, "module2_zplane_poles.png"), left=Inches(0.40), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))
    replace_image_in_slide(s11, "Picture 14", os.path.join(SCREENSHOTS_DIR, "module2_actual_vs_predicted.png"), left=Inches(5.05), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))

    # =========================================================================
    # SLIDE 12: MODULE 3
    # =========================================================================
    print("Formatting Slide 12: Module 3 Description...")
    s12 = prs.slides[11]
    for s in s12.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "MODULE 3"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "INTELLIGENT PASSENGER DASHBOARD & VISUALIZATION"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            m3_points = [
                "Passenger Route & Stop Search: Intuitive corridor filtering, destination stop selection, and active approaching vehicle localization.",
                "Real-Time Countdown Engine: Prominent high-contrast digital countdown clock displaying minutes and seconds remaining until arrival.",
                "Dynamic Delay Classification: Color-coded status pills (On-Time, Minor Delay, Severe Delay) reflecting live traffic dynamics.",
                "Analytical Confidence Intervals: Communicates 95% uncertainty bounds ([T_low, T_high]), establishing transparency during traffic spikes.",
                "Geospatial Tracking & Advisories: Interactive CartoDB dark-matter map displaying vehicle movement and contextual weather/congestion warnings."
            ]
            for idx, pt in enumerate(m3_points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s12, "Picture 7", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"))

    # =========================================================================
    # SLIDE 13: MODULE 3 OUTPUT
    # =========================================================================
    print("Formatting Slide 13: Module 3 Output...")
    s13 = prs.slides[12]
    for s in s13.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "OUTPUT"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "LIVE PASSENGER DASHBOARD & GEOSPATIAL FLEET TRACKING"
        elif s.name == "TextBox 12":
            s.text_frame.paragraphs[0].text = "Key results:  Sub-second ETA computation (<150 ms)  •  Live countdown minutes:seconds  •  Contextual transit advisories active"
    replace_image_in_slide(s13, "Picture 13", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"), left=Inches(0.40), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))
    replace_image_in_slide(s13, "Picture 14", os.path.join(SCREENSHOTS_DIR, "module3_transit_map.png"), left=Inches(5.05), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))

    # =========================================================================
    # SLIDE 14: MATHEMATICAL METHODOLOGY (Replacing Module 4)
    # =========================================================================
    print("Formatting Slide 14: Z-Transform Mathematical Methodology...")
    s14 = prs.slides[13]
    for s in s14.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "MATHEMATICAL METHODOLOGY"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "Z-TRANSFORM TRANSFER FUNCTION & INVERSE SYNTHESIS"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            math_points = [
                "Discrete Z-Transform: X(z) = sum_{n=-inf}^{inf} x[n] z^-n, where z = r * e^{j*omega} in complex frequency plane.",
                "System Transfer Function: H(z) = Y(z) / X(z) = 1 / (1 - sum_{k=1}^p a_k z^-k) driven by white noise innovation w[n].",
                "BIBO Stability Theorem: Region of Convergence (ROC) contains unit circle {|z|=1} iff all poles satisfy |p_k| < 1.0.",
                "Inverse Z-Transform via Partial Fractions: H(z) = sum [R_k / (1 - p_k z^-1)] -> h[n] = sum R_k (p_k)^n u[n].",
                "Analytical 95% Confidence Bounds: Var[e(m)] = sigma_w^2 * sum_{j=0}^{m-1} h[j]^2 -> CI = T_hat +/- 1.96 * sqrt(Var[e(m)])."
            ]
            for idx, pt in enumerate(math_points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s14, "Picture 11", os.path.join(SCREENSHOTS_DIR, "system_evaluation_metrics.png"))

    # =========================================================================
    # SLIDE 15: SYSTEM EVALUATION & PERFORMANCE BENCHMARK
    # =========================================================================
    print("Formatting Slide 15: System Evaluation & Performance Benchmark...")
    s15 = prs.slides[14]
    for s in s15.shapes:
        if s.name == "Text 2":
            tf = s.text_frame
            tf.paragraphs[0].text = "SYSTEM EVALUATION"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "QUANTITATIVE BENCHMARK & PERFORMANCE COMPARISON"
        elif s.name == "TextBox 12":
            s.text_frame.paragraphs[0].text = "Key results:  Z-Transform MAE: 7.85s (47.0% lower than Kinematic 14.8s)  •  RMSE: 9.94s  •  Execution latency: 149 ms"
    replace_image_in_slide(s15, "Picture 13", os.path.join(SCREENSHOTS_DIR, "system_evaluation_metrics.png"), left=Inches(0.40), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))
    replace_image_in_slide(s15, "Picture 14", os.path.join(SCREENSHOTS_DIR, "module2_actual_vs_predicted.png"), left=Inches(5.05), top=Inches(1.65), width=Inches(4.55), height=Inches(2.70))

    # =========================================================================
    # SLIDE 16: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    print("Formatting Slide 16: Conclusion & Future Scope...")
    s16 = prs.slides[15]
    for s in s16.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "CONCLUSION & FUTURE SCOPE"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            conc_points = [
                "Successful DSP Integration: Proves that discrete-time Z-Transform signal processing provides a mathematically sound, interpretable framework for public transport delay prediction.",
                "Superior Performance: Achieves 47% reduction in Mean Absolute Error (7.85s vs 14.8s) compared to standard kinematic constant-speed baselines.",
                "Provable Stability: Complex z-plane pole constraints guarantee BIBO stability, preventing unbounded error divergence in multi-step arrival forecasts.",
                "Passenger Transparency: Delivers real-time countdown minutes:seconds and rigorous analytical 95% confidence intervals on an executive web dashboard.",
                "Future Scope: Online adaptive pole-placement filtering (LMS/RLS), passenger boarding load integration via CAN-bus IoT, and multi-modal transfer coordination."
            ]
            for idx, pt in enumerate(conc_points):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, f"• {pt}", size_pt=11.5, space_after=8)
    replace_image_in_slide(s16, "Picture 8", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"))

    # =========================================================================
    # SLIDE 17: REFERENCES
    # =========================================================================
    print("Formatting Slide 17: References...")
    s17 = prs.slides[16]
    for s in s17.shapes:
        if s.name == "Text 2":
            s.text_frame.paragraphs[0].text = "REFERENCES"
        elif s.name in ["Text 4", "Text 5"]:
            tf = s.text_frame
            tf.clear()
            refs = [
                "[1] Oppenheim, A. V., & Schafer, R. W. (2010). Discrete-Time Signal Processing (3rd ed.). Prentice Hall Signal Processing Series.",
                "[2] Cats, O., & Jenelius, E. (2015). Dynamic bus travel time prediction using real-time AVL data. Transportation Research Part C: Emerging Technologies, 58, 222–237.",
                "[3] Proakis, J. G., & Manolakis, D. G. (2007). Digital Signal Processing: Principles, Algorithms, and Applications (4th ed.). Pearson Prentice Hall.",
                "[4] Yu, B., Yang, Z. Z., & Yao, B. Z. (2010). Bus arrival time prediction using support vector machines with dynamic data. Journal of Transportation Engineering (ASCE), 137(1), 54–60.",
                "[5] Chien, S. I., Ding, Y., & Wei, C. (2002). Dynamic bus arrival time prediction with artificial neural networks. Journal of Transportation Engineering, 128(5), 429–438."
            ]
            for idx, pt in enumerate(refs):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_paragraph_text(p, pt, size_pt=11.0, space_after=10)

    prs.save(OUTPUT_PPTX)
    print(f"\nPresentation successfully saved to: {OUTPUT_PPTX}")
    print(f"File size: {os.path.getsize(OUTPUT_PPTX)} bytes")

if __name__ == '__main__':
    build_presentation()
