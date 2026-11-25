"""
Comprehensive PowerPoint Update Script:
1. Replaces images on:
   - Slide 2 (INTRODUCTION) -> introduction_concept_visual.png (Custom conceptual diagram: urban delay volatility to Z-domain modeling)
   - Slide 3 (PROBLEM STATEMENT) -> problem_statement_visual.png (Custom conceptual diagram: urban canyon multipath reflections & forecast error accumulation)
   - Slide 5 (OBJECTIVE & RESEARCH CONTRIBUTIONS) -> objectives_visual.png (Custom conceptual diagram: 5 core research pillars)
   - Slide 6 (EXISTING SYSTEM VS PROPOSED SYSTEM) -> existing_vs_proposed_visual.png (Custom conceptual diagram: comparison matrix with checkmarks and crosses)
   - Slide 7 (SYSTEM ARCHITECTURE) -> system_architecture_diagram.png (Advanced 4-tier publication-grade technical blueprint)
2. In Slide 17 (REFERENCES):
   - Adds 10 verifiable academic references in strict APA 7th edition format across a 2-column balanced layout.
   - Formats journal and book titles with proper italics in Times New Roman.
3. Sets FULL presentation font to "Times New Roman" and font size 14 pt for all main body/bullet text, subtitles, and key summaries.
4. Saves to:
   - Z_Transform_Public_Transport_Presentation_Enhanced.pptx
   - Z_Transform_Public_Transport_Project_Review_Final.pptx
   - Z_Transform_Public_Transport_Project_Review.pptx
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "assets", "screenshots")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "template_reference.pptx")

TARGET_FILES = [
    os.path.join(PROJECT_ROOT, "Z_Transform_Public_Transport_Presentation_Enhanced.pptx"),
    os.path.join(PROJECT_ROOT, "Z_Transform_Public_Transport_Project_Review_Final.pptx"),
    os.path.join(PROJECT_ROOT, "Z_Transform_Public_Transport_Project_Review.pptx")
]

# Strict Font Rules requested by user
FONT_FAMILY = "Times New Roman"
FONT_SIZE_BODY = Pt(14)
FONT_SIZE_TITLE = Pt(22)
FONT_SIZE_SUBTITLE = Pt(14)

# High-contrast colors
COLOR_TITLE = RGBColor(15, 23, 42)      # Deep Navy (#0F172A)
COLOR_SUBTITLE = RGBColor(2, 132, 199)   # Electric Blue (#0284C7)
COLOR_BODY = RGBColor(30, 41, 59)        # Dark Slate (#1E293B)
COLOR_MUTED = RGBColor(71, 85, 105)      # Slate Gray (#475569)
COLOR_KEY_BAR = RGBColor(15, 23, 42)     # Deep Navy Bold

def set_run(r, text, font_name=FONT_FAMILY, size_pt=14, color=COLOR_BODY, bold=False, italic=False):
    r.text = text
    r.font.name = font_name
    r.font.size = Pt(size_pt)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color

def set_title(shape, title_text, font_name=FONT_FAMILY, size_pt=22, color=COLOR_TITLE):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    r = p.add_run()
    set_run(r, title_text, font_name=font_name, size_pt=size_pt, color=color, bold=True)

def set_title_and_subtitle(shape, title_text, sub_text, size_title=22, size_sub=14):
    tf = shape.text_frame
    tf.clear()
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    set_run(r1, title_text, size_pt=size_title, color=COLOR_TITLE, bold=True)
    if sub_text:
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        set_run(r2, sub_text, size_pt=size_sub, color=COLOR_SUBTITLE, bold=True)

def set_para_structured(p, head_text, body_text, head_color=COLOR_TITLE, body_color=COLOR_BODY, size_pt=14, space_after=5):
    p.clear()
    r1 = p.add_run()
    set_run(r1, head_text, size_pt=size_pt, color=head_color, bold=True)
    r2 = p.add_run()
    set_run(r2, body_text, size_pt=size_pt, color=body_color, bold=False)
    p.space_after = Pt(space_after)

def replace_or_add_picture(slide, old_shape_name, img_path, left, top, width, height):
    if not os.path.exists(img_path):
        print(f"Warning: Image {img_path} not found.")
        return None
    for s in list(slide.shapes):
        if s.name == old_shape_name:
            sp = s._element
            sp.getparent().remove(sp)
            break
    return slide.shapes.add_picture(img_path, left, top, width, height)

def build_custom_presentation():
    print(f"Loading template presentation from {TEMPLATE_PATH}...")
    prs = pptx.Presentation(TEMPLATE_PATH)

    # Helper function to style slide numbers
    def style_slide_number(slide):
        for s in slide.shapes:
            if s.name == "Text 3" and s.has_text_frame:
                for p in s.text_frame.paragraphs:
                    p.font.name = FONT_FAMILY
                    for r in p.runs:
                        r.font.name = FONT_FAMILY

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    print("Formatting Slide 1: Title Slide (Times New Roman)...")
    s1 = prs.slides[0]
    for s in s1.shapes:
        if s.name == "TextBox 4":
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            r1 = p1.add_run()
            set_run(r1, "Z-Transform-Based Public Transport Arrival-Time Prediction System", size_pt=20, color=COLOR_TITLE, bold=True)
            p1.space_after = Pt(4)
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            set_run(r2, "A Causal Discrete-Time Signal Processing Framework for Urban Transit Delay Modeling and Real-Time ETA Forecasting", size_pt=14, color=COLOR_SUBTITLE, bold=True)
            p2.space_after = Pt(4)
            p3 = tf.add_paragraph()
            r3 = p3.add_run()
            set_run(r3, "Academic Capstone Engineering Review • Department of Computer Science & Engineering", size_pt=14, color=COLOR_MUTED)
        elif s.name == "TextBox 6":
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            r1 = p1.add_run()
            set_run(r1, "Guided by:", size_pt=14, color=COLOR_MUTED, bold=True)
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            set_run(r2, "Project Mentor & Guide", size_pt=14, color=COLOR_TITLE, bold=True)
            p3 = tf.add_paragraph()
            r3 = p3.add_run()
            set_run(r3, "Department of Computer Science & Engineering", size_pt=14, color=COLOR_MUTED)
        elif s.name == "TextBox 8":
            tf = s.text_frame
            tf.clear()
            p1 = tf.paragraphs[0]
            r1 = p1.add_run()
            set_run(r1, "Submitted by:", size_pt=14, color=COLOR_MUTED, bold=True)
            candidates = [
                "Engineering Capstone Candidate 1 (192311008)",
                "Engineering Capstone Candidate 2 (192324037)",
                "Engineering Capstone Candidate 3 (192324062)",
                "Engineering Capstone Candidate 4 (192372002)"
            ]
            for c in candidates:
                p = tf.add_paragraph()
                r = p.add_run()
                set_run(r, c, size_pt=14, color=COLOR_BODY)

    # =========================================================================
    # SLIDE 2: INTRODUCTION (NEW CUSTOM DEDICATED VISUAL)
    # =========================================================================
    print("Formatting Slide 2: Introduction (NEW Dedicated Visual + 14 pt Times New Roman)...")
    s2 = prs.slides[1]
    style_slide_number(s2)
    for s in s2.shapes:
        if s.name == "Text 2":
            set_title(s, "INTRODUCTION")
        elif s.name == "Text 4":
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            intro_pts = [
                ("Transit Delay Volatility: ", "Urban bus corridors experience heavy travel-time variance from traffic signal cycles, arterial bottlenecks, and passenger dwell times."),
                ("Kinematic Model Flaws: ", "Conventional arrival estimation relies on static timetables or constant-velocity models (d/v), which fail severely during congestion."),
                ("Discrete Stochastic Signal: ", "Headway deviations and traversal times across successive stations form an intrinsic discrete-time stochastic signal sequence x[n]."),
                ("Z-Transform Foundation: ", "Discrete signal processing provides a rigorous complex-frequency domain foundation for causal rational transfer function modeling H(z)."),
                ("End-to-End System: ", "This project delivers a complete platform featuring 2D Kalman GPS denoising, Yule-Walker identification, BIBO stability proofs, and passenger UI.")
            ]
            for idx, (h, b) in enumerate(intro_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    # User requested: "change image in introduction according to it"
    replace_or_add_picture(s2, "Picture 9", os.path.join(SCREENSHOTS_DIR, "introduction_concept_visual.png"), Inches(6.25), Inches(1.20), Inches(3.45), Inches(4.00))

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT (CUSTOM VISUAL)
    # =========================================================================
    print("Formatting Slide 3: Problem Statement (Custom Visual + 14 pt Times New Roman)...")
    s3 = prs.slides[2]
    style_slide_number(s3)
    for s in s3.shapes:
        if s.name == "Text 2":
            set_title(s, "PROBLEM STATEMENT")
        elif s.name == "Text 4":
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            prob_pts = [
                ("Delay Wave Propagation: ", "Arterial bottlenecks trigger non-linear oscillatory delay waves that ripple downstream, causing vehicle bunching along transit corridors."),
                ("Urban GPS Multipath Noise: ", "High-rise city architecture causes satellite signal reflections, inducing 30–50m GPS coordinate jumps that corrupt distance tracking."),
                ("Recursive Error Divergence: ", "Unconstrained regressors and neural networks lack stability bounds, triggering exponential error accumulation over multi-stop horizons."),
                ("Lack of Uncertainty Bounds: ", "Commercial passenger transit applications display deterministic point-estimate ETAs with zero confidence bounds, eroding passenger trust."),
                ("Heavy Edge Compute Footprint: ", "Deep neural models require large GPU memory, preventing cost-effective edge deployment on low-power onboard transit microcontrollers.")
            ]
            for idx, (h, b) in enumerate(prob_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s3, "Picture 8", os.path.join(SCREENSHOTS_DIR, "problem_statement_visual.png"), Inches(6.25), Inches(1.20), Inches(3.45), Inches(4.00))

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW
    # =========================================================================
    print("Formatting Slide 4: Literature Review Table (Times New Roman)...")
    s4 = prs.slides[3]
    style_slide_number(s4)
    for s in s4.shapes:
        if s.name == "Text 2":
            set_title(s, "LITERATURE REVIEW")
        elif s.has_table:
            table = s.table
            headers = ['S.No.', 'Author Name & Year', 'Title', 'Models / Algorithm', 'Limitation', 'Research Gap Addressed']
            for col_idx, h_text in enumerate(headers):
                cell = table.cell(0, col_idx)
                cell.text = ""
                p = cell.text_frame.paragraphs[0]
                r = p.add_run()
                set_run(r, h_text, size_pt=11.5, color=COLOR_TITLE, bold=True)

            lit_rows = [
                ['1', 'Cats & Jenelius (2015)', 'Dynamic bus travel time prediction using AVL data', 'Linear Regression & Moving Averages', 'Lacks complex-frequency domain modeling and formal recursive BIBO stability bounds.', 'Z-Transform rational transfer function H(z) with provable unit circle pole stability.'],
                ['2', 'Oppenheim & Schafer (2010)', 'Discrete-Time Signal Processing (3rd Edition)', 'Z-Transform, Transfer Function H(z), Residue Inversion', 'Theoretical signal processing formulation without geospatial transit network integration.', 'End-to-end framework integrating 2D Kalman GPS filtering with discrete delay sequences.'],
                ['3', 'Yu, Yang & Yao (2010)', 'Bus arrival time prediction using SVMs with dynamic data', 'Support Vector Machines (SVM Regressor)', 'High computational complexity; "black-box" model lacks physical interpretability and confidence intervals.', 'Lightweight recursive execution (<150 ms) with closed-form analytical 95% confidence intervals.'],
                ['4', 'Chien, Ding & Wei (2002)', 'Dynamic bus arrival time prediction with artificial neural networks', 'Multilayer Perceptron Neural Networks (ANN)', 'Prone to recursive error accumulation and gradient instability without pole-zero constraints.', 'Guaranteed BIBO stability (|p_k| < 1.0) preventing error explosion over multi-stop horizons.']
            ]
            for row_idx, r_data in enumerate(lit_rows, start=1):
                for col_idx, val in enumerate(r_data):
                    cell = table.cell(row_idx, col_idx)
                    cell.text = ""
                    p = cell.text_frame.paragraphs[0]
                    r = p.add_run()
                    set_run(r, val, size_pt=10, color=COLOR_BODY, bold=False)

    # =========================================================================
    # SLIDE 5: OBJECTIVE & RESEARCH CONTRIBUTIONS (CUSTOM VISUAL)
    # =========================================================================
    print("Formatting Slide 5: Objective (Custom Visual + 14 pt Times New Roman)...")
    s5 = prs.slides[4]
    style_slide_number(s5)
    for s in s5.shapes:
        if s.name == "Text 2":
            set_title(s, "OBJECTIVE & RESEARCH CONTRIBUTIONS")
        elif s.name == "Text 4":
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            obj_pts = [
                ("Robust GPS Denoising Pipeline: ", "Implement 2D state-space Kalman filtering and Hampel identifier to suppress urban multipath noise and sensor dropouts (>20 dB SNR)."),
                ("Causal Transfer Function Modeling: ", "Model corridor delay perturbations as an LTI discrete-time system H(z) = 1 / (1 - sum a_k z^-k) via Yule-Walker Toeplitz equations."),
                ("Provable Pole BIBO Stability: ", "Constrain and verify all characteristic polynomial denominator roots strictly inside the open unit circle (|p_k| < 1.0) in the z-plane."),
                ("Analytical Inverse Z-Transform: ", "Apply partial fraction residue decomposition to analytically compute time-domain impulse response h[n] and 95% confidence bounds."),
                ("Intelligent Passenger Dashboard: ", "Deploy real-time geospatial fleet tracking, live countdown clock (min:sec), dynamic delay classification, and contextual advisories.")
            ]
            for idx, (h, b) in enumerate(obj_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s5, "Picture 8", os.path.join(SCREENSHOTS_DIR, "objectives_visual.png"), Inches(6.25), Inches(1.20), Inches(3.45), Inches(4.00))

    # =========================================================================
    # SLIDE 6: EXISTING SYSTEM VS PROPOSED SYSTEM (CUSTOM VISUAL)
    # =========================================================================
    print("Formatting Slide 6: Existing System vs Proposed System (Custom Visual + 14 pt Times New Roman)...")
    s6 = prs.slides[5]
    style_slide_number(s6)
    for s in s6.shapes:
        if s.name == "Text 2":
            set_title(s, "EXISTING SYSTEM VS PROPOSED SYSTEM")
        elif s.name == "Text 4":
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            comp_pts = [
                ("Static Timetable Baselines: ", "Completely decoupled from real-time traffic dynamics; incapable of responding dynamically to downstream arterial incidents."),
                ("Kinematic Constant Speed (d/v): ", "Assumes unrealistic constant speed across traffic signals and completely ignores passenger dwell time variance."),
                ("Unconstrained Deep Learning: ", "High memory footprint, uninterpretable black-box weights, and lack formal Bounded-Input Bounded-Output stability proofs."),
                ("Proposed Z-Transform Platform: ", "Dynamically captures oscillatory delay waves through transfer function poles, guaranteeing BIBO stability (|p| < 1.0)."),
                ("Analytical 95% Confidence Bounds: ", "Provides closed-form uncertainty bounds derived from the impulse response variance, restoring passenger trust.")
            ]
            for idx, (h, b) in enumerate(comp_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s6, "Picture 8", os.path.join(SCREENSHOTS_DIR, "existing_vs_proposed_visual.png"), Inches(6.25), Inches(1.20), Inches(3.45), Inches(4.00))

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE (ADVANCED 4-TIER TECHNICAL BLUEPRINT)
    # =========================================================================
    print("Formatting Slide 7: System Architecture (NEW Publication Blueprint)...")
    s7 = prs.slides[6]
    style_slide_number(s7)
    for s in list(s7.shapes):
        if s.has_text_frame and s.text_frame.text.strip() == "8":
            sp = s._element
            sp.getparent().remove(sp)

    tb_s7 = s7.shapes.add_textbox(Inches(0.50), Inches(0.20), Inches(9.00), Inches(0.85))
    set_title_and_subtitle(tb_s7, "SYSTEM ARCHITECTURE & INTEGRATED DATA PIPELINE", 
                           "Three-Tier Modular Architecture: Ingestion & Denoising → Z-Transform Engine → Passenger Operations")

    # User requested: "and in system architecture change the image according to it"
    replace_or_add_picture(s7, "Picture 41", os.path.join(SCREENSHOTS_DIR, "system_architecture_diagram.png"), Inches(0.50), Inches(1.05), Inches(9.00), Inches(4.30))

    # =========================================================================
    # SLIDE 8: MODULE 1 DESCRIPTION
    # =========================================================================
    print("Formatting Slide 8: Module 1 Description (14 pt Times New Roman)...")
    s8 = prs.slides[7]
    style_slide_number(s8)
    for s in s8.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "MODULE 1", "REAL-TIME TRANSIT DATA ACQUISITION & PREPROCESSING")
        elif s.name in ["Text 4", "Text 5"]:
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            m1_pts = [
                ("Fleet Telemetry Ingestion: ", "Continuously ingests GPS coordinates, instantaneous vehicle velocity, compass bearing, and passenger load from 15 active buses across 5 corridors."),
                ("Geodesic Haversine Math: ", "Computes great-circle distances and dynamic heading vectors to accurately locate vehicles relative to 44 transit stop nodes and corridor polylines."),
                ("2D State-Space Kalman Filtering: ", "Deploys a constant-velocity state transition filter [x, y, vx, vy]^T that suppresses urban canyon multipath coordinate noise by 68.4%."),
                ("Robust Hampel Outlier Rejection: ", "Identifies and replaces sensor dropouts and impulsive GPS anomalies using 3x Median Absolute Deviation (MAD) local windowing."),
                ("Discrete Signal Conditioning: ", "Formats raw historical arrivals into regularly spaced discrete-time headway deviation sequences s[n] with mean-centered detrending.")
            ]
            for idx, (h, b) in enumerate(m1_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s8, "Picture 9", os.path.join(SCREENSHOTS_DIR, "module1_kalman_gps.png"), Inches(6.25), Inches(1.25), Inches(3.45), Inches(3.90))

    # =========================================================================
    # SLIDE 9: MODULE 1 OUTPUT (14 pt Times New Roman Text on Left + Figure on Right)
    # =========================================================================
    print("Formatting Slide 9: Module 1 Output (14 pt Times New Roman)...")
    s9 = prs.slides[8]
    style_slide_number(s9)
    for s in s9.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "OUTPUT: MODULE 1", "DATA PREPROCESSING & GPS TRAJECTORY DENOISING")
        elif s.name in ["TextBox 11", "TextBox 12"]:
            tf = s.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            r = p.add_run()
            set_run(r, "Key results: Tracking RMSE reduced from 14.8m to 4.8m • 68.4% multipath noise suppressed • Hampel filter restored 22.0 dB SNR",
                    size_pt=14, color=COLOR_KEY_BAR, bold=True)

    replace_or_add_picture(s9, "Picture 12", os.path.join(SCREENSHOTS_DIR, "module1_kalman_gps.png"), Inches(5.35), Inches(1.25), Inches(4.30), Inches(3.30))
    for s in list(s9.shapes):
        if s.name in ["Picture 13", "TextBox 15"]:
            sp = s._element
            sp.getparent().remove(sp)

    tb_m1 = s9.shapes.add_textbox(Inches(0.50), Inches(1.25), Inches(4.70), Inches(3.40))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    m1_eval = [
        ("2D Kalman Filter Performance: ", "The constant-velocity state-space model effectively eliminates multipath reflections, reducing tracking error from 14.8m down to 4.8m."),
        ("Error Variance Reduction: ", "Achieved a 68.4% reduction in coordinate error variance across dense downtown urban canyons."),
        ("Hampel Outlier Rejection: ", "Purged 5 extreme sensor transmission dropouts using 3x MAD thresholding without attenuating authentic delay dynamics."),
        ("Signal Conditioning: ", "Restored Signal-to-Noise Ratio to 22.04 dB, providing clean discrete time series for Z-domain transfer function estimation.")
    ]
    for idx, (h, b) in enumerate(m1_eval):
        p = tf_m1.paragraphs[0] if idx == 0 else tf_m1.add_paragraph()
        set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)

    # =========================================================================
    # SLIDE 10: MODULE 2 DESCRIPTION
    # =========================================================================
    print("Formatting Slide 10: Module 2 Description (14 pt Times New Roman)...")
    s10 = prs.slides[9]
    style_slide_number(s10)
    for s in s10.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "MODULE 2", "Z-TRANSFORM-BASED ARRIVAL-TIME PREDICTION ENGINE")
        elif s.name in ["Text 4", "Text 5"]:
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            m2_pts = [
                ("Discrete Delay Modeling: ", "Represents corridor traversal fluctuations as a causal autoregressive discrete-time process s[n] driven by traffic shocks w[n]."),
                ("Yule-Walker Identification: ", "Solves Toeplitz autocorrelation matrix R_ss * a = r_ss to estimate optimal filter coefficients [a1, ..., ap]."),
                ("Transfer Function Formulation: ", "Expresses system dynamics in the complex z-domain: H(z) = 1 / (1 - sum a_k z^-k) with rational denominator polynomial A(z)."),
                ("Pole-Zero Stability Proof: ", "Verifies that all characteristic polynomial roots (poles) reside strictly inside the unit circle (|p_k| < 1.0) in the z-plane."),
                ("Analytical Inverse Z-Transform: ", "Applies partial fraction residue expansion to synthesize time-domain impulse response h[n] and 95% confidence bounds.")
            ]
            for idx, (h, b) in enumerate(m2_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s10, "Picture 7", os.path.join(SCREENSHOTS_DIR, "module2_zplane_poles.png"), Inches(6.25), Inches(1.25), Inches(3.45), Inches(3.90))

    # =========================================================================
    # SLIDE 11: MODULE 2 OUTPUT (14 pt Times New Roman Text on Left + Figure on Right)
    # =========================================================================
    print("Formatting Slide 11: Module 2 Output (14 pt Times New Roman)...")
    s11 = prs.slides[10]
    style_slide_number(s11)
    for s in s11.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "OUTPUT: MODULE 2", "COMPLEX Z-PLANE POLE ANALYSIS & MODEL BACKTEST")
        elif s.name in ["TextBox 11", "TextBox 12"]:
            tf = s.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            r = p.add_run()
            set_run(r, "Key results: All poles inside unit circle (|p| = 0.614 < 1.0) • MAE: 7.85s (vs 14.8s Kinematic) • Analytical 95% CI Verified",
                    size_pt=14, color=COLOR_KEY_BAR, bold=True)

    replace_or_add_picture(s11, "Picture 13", os.path.join(SCREENSHOTS_DIR, "module2_actual_vs_predicted.png"), Inches(5.35), Inches(1.25), Inches(4.30), Inches(3.30))
    for s in list(s11.shapes):
        if s.name in ["Picture 14", "TextBox 16"]:
            sp = s._element
            sp.getparent().remove(sp)

    tb_m2 = s11.shapes.add_textbox(Inches(0.50), Inches(1.25), Inches(4.70), Inches(3.40))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    m2_eval = [
        ("Transfer Function H(z): ", "Estimated 3rd-order system H(z) = 1 / (1 + 0.213 z^-1 - 0.150 z^-2 + 0.059 z^-3) with innovation variance sigma_w^2 = 213.78 s^2."),
        ("Guaranteed BIBO Stability: ", "Poles at p_1,2 = -0.106 ± 0.605j (|p|=0.614) and p_3 = -0.157. Spectral radius rho(A) = 0.614 < 1.0 formally proves stability."),
        ("Impulse Response h[n]: ", "Decomposed into partial fractions h[n] = sum R_k (p_k)^n u[n], ensuring transient delays smoothly decay to zero within 6 epochs."),
        ("Backtest Horizon Accuracy: ", "Achieved an MAE of 7.85s (47.0% lower than Kinematic 14.8s, 36.8% lower than SMA 12.4s) with zero recursive drift.")
    ]
    for idx, (h, b) in enumerate(m2_eval):
        p = tf_m2.paragraphs[0] if idx == 0 else tf_m2.add_paragraph()
        set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)

    # =========================================================================
    # SLIDE 12: MODULE 3 DESCRIPTION
    # =========================================================================
    print("Formatting Slide 12: Module 3 Description (14 pt Times New Roman)...")
    s12 = prs.slides[11]
    style_slide_number(s12)
    for s in s12.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "MODULE 3", "INTELLIGENT PASSENGER DASHBOARD & VISUALIZATION")
        elif s.name in ["Text 4", "Text 5"]:
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            m3_pts = [
                ("Passenger Route & Stop Search: ", "Intuitive corridor filtering, destination stop selection, and approaching vehicle localization across all lines."),
                ("Real-Time Countdown Engine: ", "Prominent high-contrast digital countdown clock displaying minutes and seconds remaining with live sub-second refresh."),
                ("Dynamic Delay Classification: ", "Color-coded status pills (On-Time within ±60s, Minor Delay +1–4m, Severe Delay >4m) reflecting live traffic dynamics."),
                ("Analytical Confidence Intervals: ", "Communicates closed-form 95% uncertainty bounds ([T_low, T_high]), establishing transparency during unexpected traffic bottlenecks."),
                ("Geospatial Tracking & Advisories: ", "Interactive CartoDB dark-matter map displaying vehicle movement, sequential stop progression nodes, and contextual travel warnings.")
            ]
            for idx, (h, b) in enumerate(m3_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s12, "Picture 7", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"), Inches(6.25), Inches(1.25), Inches(3.45), Inches(3.90))

    # =========================================================================
    # SLIDE 13: MODULE 3 OUTPUT (14 pt Times New Roman Text on Left + Figure on Right)
    # =========================================================================
    print("Formatting Slide 13: Module 3 Output (14 pt Times New Roman)...")
    s13 = prs.slides[12]
    style_slide_number(s13)
    for s in s13.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "OUTPUT: MODULE 3", "LIVE PASSENGER DASHBOARD & GEOSPATIAL FLEET TRACKING")
        elif s.name in ["TextBox 11", "TextBox 12"]:
            tf = s.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            r = p.add_run()
            set_run(r, "Key results: Sub-second ETA computation (<150 ms) • Live countdown minutes:seconds • Contextual transit advisories active",
                    size_pt=14, color=COLOR_KEY_BAR, bold=True)

    replace_or_add_picture(s13, "Picture 13", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"), Inches(5.35), Inches(1.25), Inches(4.30), Inches(3.30))
    for s in list(s13.shapes):
        if s.name in ["Picture 14", "TextBox 16"]:
            sp = s._element
            sp.getparent().remove(sp)

    tb_m3 = s13.shapes.add_textbox(Inches(0.50), Inches(1.25), Inches(4.70), Inches(3.40))
    tf_m3 = tb_m3.text_frame
    tf_m3.word_wrap = True
    m3_eval = [
        ("Sub-Second ETA Generation: ", "End-to-end arrival prediction executes in 149.4 ms, enabling instantaneous client UI updates without server lag."),
        ("Live Digital Countdown: ", "Renders large high-contrast countdown digits (e.g., 05:42) alongside dynamic vehicle tracking and approach speed (28.4 km/h)."),
        ("Analytical Uncertainty Display: ", "Displays closed-form 95% confidence intervals ([315s — 369s]), giving passengers honest, mathematically justified bounds."),
        ("Contextual Transit Advisories: ", "Automatically dispatches color-coded service alerts (On-Schedule, Minor Delay, Severe Delay, Weather Alerts) during headway deviations.")
    ]
    for idx, (h, b) in enumerate(m3_eval):
        p = tf_m3.paragraphs[0] if idx == 0 else tf_m3.add_paragraph()
        set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)

    # =========================================================================
    # SLIDE 14: MATHEMATICAL METHODOLOGY
    # =========================================================================
    print("Formatting Slide 14: Mathematical Methodology (14 pt Times New Roman)...")
    s14 = prs.slides[13]
    style_slide_number(s14)
    for s in s14.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "MATHEMATICAL METHODOLOGY", "Z-TRANSFORM TRANSFER FUNCTION & INVERSE SYNTHESIS")
        elif s.name in ["Text 4", "Text 5"]:
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            math_pts = [
                ("Bilateral Z-Transform: ", "X(z) = sum_{n=-inf}^{inf} x[n] z^-n, mapping discrete time sequences to complex frequency variable z = r * e^{j*omega}."),
                ("LTI Transfer Function: ", "H(z) = S(z) / W(z) = 1 / (1 - sum a_k z^-k) = z^p / (z^p - a1*z^{p-1} - ... - ap) driven by white noise w[n]."),
                ("BIBO Stability Theorem: ", "A causal discrete-time transit system is BIBO stable iff the Region of Convergence contains the unit circle {|z|=1}, meaning |p_k| < 1.0."),
                ("Inverse Z-Transform via Residues: ", "H(z) = sum [R_k / (1 - p_k z^-1)] -> h[n] = sum R_k (p_k)^n u[n], where residues R_k = lim_{z->p_k} (1 - p_k z^-1) H(z)."),
                ("Analytical Forecast Variance: ", "Var[e(m)] = sigma_w^2 * sum_{j=0}^{m-1} h[j]^2 -> CI_95% = T_hat +/- 1.96 * sqrt(Var[e(m)]).")
            ]
            for idx, (h, b) in enumerate(math_pts):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s14, "Picture 11", os.path.join(SCREENSHOTS_DIR, "system_evaluation_metrics.png"), Inches(6.25), Inches(1.25), Inches(3.45), Inches(3.90))

    # =========================================================================
    # SLIDE 15: SYSTEM EVALUATION & PERFORMANCE BENCHMARK (14 pt Times New Roman)
    # =========================================================================
    print("Formatting Slide 15: System Evaluation (14 pt Times New Roman)...")
    s15 = prs.slides[14]
    style_slide_number(s15)
    for s in s15.shapes:
        if s.name == "Text 2":
            set_title_and_subtitle(s, "SYSTEM EVALUATION", "QUANTITATIVE BENCHMARK & PERFORMANCE COMPARISON")
        elif s.name in ["TextBox 11", "TextBox 12"]:
            tf = s.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            r = p.add_run()
            set_run(r, "Key results: Z-Transform MAE: 7.85s (47.0% lower than Kinematic 14.8s) • RMSE: 9.94s • Execution latency: 149 ms",
                    size_pt=14, color=COLOR_KEY_BAR, bold=True)

    replace_or_add_picture(s15, "Picture 13", os.path.join(SCREENSHOTS_DIR, "system_evaluation_metrics.png"), Inches(5.35), Inches(1.25), Inches(4.30), Inches(3.30))
    for s in list(s15.shapes):
        if s.name in ["Picture 14", "TextBox 16"]:
            sp = s._element
            sp.getparent().remove(sp)

    tb_eval = s15.shapes.add_textbox(Inches(0.50), Inches(1.25), Inches(4.70), Inches(3.40))
    tf_eval = tb_eval.text_frame
    tf_eval.word_wrap = True
    eval_pts = [
        ("Peak Congestion Accuracy: ", "During Morning Rush (7–10 AM), Z-Transform MAE is 9.2s vs Kinematic 19.4s (52.6% reduction). During Evening Rush (4–7 PM), MAE is 11.8s vs Kinematic 22.8s (48.2% reduction)."),
        ("Off-Peak Valley Precision: ", "During Midday (11 AM–3 PM), MAE drops to 5.4s vs Kinematic 11.2s. During Night service (8–11 PM), MAE reaches 4.2s vs Kinematic 8.5s."),
        ("Overall Dataset Benchmark: ", "Across the entire 7,392 record dataset, Z-Transform MAE is 7.85s vs SMA 12.42s and Kinematic 14.80s, achieving an overall 47.0% error reduction."),
        ("Impulse Response Stability: ", "Root Mean Squared Error (RMSE) is 9.94s, confirming robust dampening of traffic surges without runaway recursive error accumulation.")
    ]
    for idx, (h, b) in enumerate(eval_pts):
        p = tf_eval.paragraphs[0] if idx == 0 else tf_eval.add_paragraph()
        set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)

    # =========================================================================
    # SLIDE 16: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    print("Formatting Slide 16: Conclusion & Future Scope (14 pt Times New Roman)...")
    s16 = prs.slides[15]
    style_slide_number(s16)
    for s in s16.shapes:
        if s.name == "Text 2":
            set_title(s, "CONCLUSION & FUTURE SCOPE")
        elif s.name in ["Text 4", "Text 5"]:
            s.left = Inches(0.50)
            s.top = Inches(1.20)
            s.width = Inches(5.60)
            s.height = Inches(4.20)
            tf = s.text_frame
            tf.clear()
            tf.word_wrap = True
            concs = [
                ("Successful DSP Integration: ", "Establishes a rigorous discrete-time signal processing methodology for urban public transport arrival estimation."),
                ("Proven Error Reduction: ", "Achieves a 47.0% reduction in Mean Absolute Error (7.85s vs 14.80s) compared to industry-standard constant-speed kinematic models."),
                ("Guaranteed System Stability: ", "Complex z-plane pole constraints guarantee Bounded-Input Bounded-Output stability, preventing multi-stop recursive forecast explosion."),
                ("Passenger Transparency & Trust: ", "Delivers real-time countdown minutes:seconds and closed-form analytical 95% confidence intervals on a modern responsive interface."),
                ("Future Scope: ", "Integration of CAN-bus passenger load sensors, adaptive LMS/RLS online pole-placement, and multi-agency regional transit coordination.")
            ]
            for idx, (h, b) in enumerate(concs):
                p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                set_para_structured(p, f"• {h}", b, size_pt=14, space_after=5)
    replace_or_add_picture(s16, "Picture 8", os.path.join(SCREENSHOTS_DIR, "module3_passenger_countdown.png"), Inches(6.25), Inches(1.25), Inches(3.45), Inches(3.90))

    # =========================================================================
    # SLIDE 17: REFERENCES (10 APA 7th Edition Citations in Balanced 2-Column Layout)
    # =========================================================================
    print("Formatting Slide 17: 10 References in APA Format (Times New Roman)...")
    s17 = prs.slides[16]
    style_slide_number(s17)
    for s in list(s17.shapes):
        if s.name == "Text 2":
            set_title(s, "REFERENCES")
        elif s.name in ["Text 4", "Text 5"]:
            sp = s._element
            sp.getparent().remove(sp)

    # 10 Academic References in strict APA 7th Edition
    # Structured tuple: (number_prefix, authors_year, title, journal_or_book_italic, volume_italic, rest_of_cit)
    apa_refs_left = [
        ("[1] ", "Cats, O., & Jenelius, E. (2015). Dynamic bus travel time prediction using real-time AVL data. ",
         "Transportation Research Part C: Emerging Technologies", ", 58, 222–237. https://doi.org/10.1016/j.trc.2015.04.017"),
        ("[2] ", "Chien, S. I., Ding, Y., & Wei, C. (2002). Dynamic bus arrival time prediction with artificial neural networks. ",
         "Journal of Transportation Engineering", ", 128(5), 429–438. https://doi.org/10.1061/(ASCE)0733-947X(2002)128:5(429)"),
        ("[3] ", "Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. ",
         "Journal of Basic Engineering", ", 82(1), 35–45. https://doi.org/10.1115/1.3662552"),
        ("[4] ", "Kay, S. M. (1988). ",
         "Modern spectral estimation: Theory and application", ". Prentice Hall Signal Processing Series."),
        ("[5] ", "Lin, W. H., & Zeng, J. (1999). Experimental study on real-time bus arrival time prediction with GPS data. ",
         "Transportation Research Record", ", 1666(1), 101–109. https://doi.org/10.3141/1666-12")
    ]

    apa_refs_right = [
        ("[6] ", "Oppenheim, A. V., & Schafer, R. W. (2010). ",
         "Discrete-time signal processing", " (3rd ed.). Prentice Hall."),
        ("[7] ", "Patnaik, J., Chien, S., & Bladikas, A. (2004). Estimation of bus arrival times using APC data. ",
         "Journal of Public Transportation", ", 7(1), 1–20. https://doi.org/10.5038/2375-0901.7.1.1"),
        ("[8] ", "Proakis, J. G., & Manolakis, D. G. (2007). ",
         "Digital signal processing: Principles, algorithms, and applications", " (4th ed.). Pearson Prentice Hall."),
        ("[9] ", "Shalaby, A., & Farhan, A. (2004). Prediction model of bus arrival and departure times using AVL and APC data. ",
         "Journal of Public Transportation", ", 7(1), 41–61. https://doi.org/10.5038/2375-0901.7.1.3"),
        ("[10] ", "Yu, B., Yang, Z. Z., & Yao, B. Z. (2010). Bus arrival time prediction using support vector machines with dynamic data. ",
         "Journal of Transportation Engineering", ", 137(1), 54–60. https://doi.org/10.1061/(ASCE)TE.1943-5436.0000185")
    ]

    # Column 1 (Left): Citations [1] to [5]
    tb_l = s17.shapes.add_textbox(Inches(0.50), Inches(1.15), Inches(4.35), Inches(4.25))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    for idx, (pref, auth, jour, rest) in enumerate(apa_refs_left):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        r0 = p.add_run()
        set_run(r0, pref, size_pt=11.5, color=COLOR_TITLE, bold=True)
        r1 = p.add_run()
        set_run(r1, auth, size_pt=11.5, color=COLOR_BODY, bold=False)
        r2 = p.add_run()
        set_run(r2, jour, size_pt=11.5, color=COLOR_TITLE, bold=False, italic=True)
        r3 = p.add_run()
        set_run(r3, rest, size_pt=11.5, color=COLOR_BODY, bold=False)
        p.space_after = Pt(6)

    # Column 2 (Right): Citations [6] to [10]
    tb_r = s17.shapes.add_textbox(Inches(5.15), Inches(1.15), Inches(4.35), Inches(4.25))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    for idx, (pref, auth, jour, rest) in enumerate(apa_refs_right):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        r0 = p.add_run()
        set_run(r0, pref, size_pt=11.5, color=COLOR_TITLE, bold=True)
        r1 = p.add_run()
        set_run(r1, auth, size_pt=11.5, color=COLOR_BODY, bold=False)
        r2 = p.add_run()
        set_run(r2, jour, size_pt=11.5, color=COLOR_TITLE, bold=False, italic=True)
        r3 = p.add_run()
        set_run(r3, rest, size_pt=11.5, color=COLOR_BODY, bold=False)
        p.space_after = Pt(6)

    # Save to all target locations
    for target_path in TARGET_FILES:
        try:
            prs.save(target_path)
            print(f"Saved presentation to: {target_path} ({os.path.getsize(target_path)} bytes)")
        except Exception as e:
            print(f"Could not save to {target_path}: {e}")

if __name__ == '__main__':
    build_custom_presentation()
