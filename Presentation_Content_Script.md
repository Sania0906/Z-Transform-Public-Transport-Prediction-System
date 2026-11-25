# Z-Transform-Based Public Transport Arrival-Time Prediction System
## Complete Academic Project Review Presentation Content & Speaker Script

---

### SLIDE 1: TITLE SLIDE
- **Title:** Z-Transform-Based Public Transport Arrival-Time Prediction System
- **Subtitle:** A Causal Discrete-Time Signal Processing Framework for Urban Transit Delay Modeling and Real-Time ETA Forecasting
- **Institutional Alignment:** Academic Capstone Engineering Review
- **Guided by:** Project Mentor & Guide, Department of Computer Science & Engineering
- **Submitted by:**
  - Candidate 1 (Reg. No. 192311008)
  - Candidate 2 (Reg. No. 192324037)
  - Candidate 3 (Reg. No. 192324062)
  - Candidate 4 (Reg. No. 192372002)

**Presenter Notes:**
> "Good morning, respected committee members. Today, we present our engineering capstone project: 'Z-Transform-Based Public Transport Arrival-Time Prediction System'. We formulate urban bus delay propagation not as a black-box regression problem, but as a causal discrete-time signal processing system with provable stability guarantees using the Z-Transform."

---

### SLIDE 2: INTRODUCTION
- **Header:** INTRODUCTION
- **Slide Number:** 2
- **Key Points:**
  - **Urban Transit Delay Volatility:** Public bus transport operations experience heavy travel-time variance caused by dynamic traffic signal cycles, arterial congestion bottlenecks, and stochastic passenger dwell times.
  - **Limitations of Conventional Kinematic Models:** Standard arrival prediction algorithms employ static timetables or constant-velocity kinematic models ($d/v$), which degrade severely during peak congestion windows.
  - **Discrete-Time Stochastic Formulation:** Traversal times and headway deviations across successive corridor checkpoints form an intrinsic discrete-time stochastic signal sequence $x[n]$.
  - **The Z-Transform Advantage:** Discrete-time signal processing principles—specifically the Z-Transform—provide a rigorous complex-frequency domain foundation for rational transfer function modeling $H(z)$.
  - **Integrated Real-Time Architecture:** This engineering capstone develops an end-to-end platform featuring 2D Kalman GPS denoising, Yule-Walker autoregressive system identification, pole-zero stability guarantees, and passenger dashboards.

**Presenter Notes:**
> "Urban bus travel times are non-stationary discrete events. Kinematic distance-over-speed calculations assume homogeneous highway speeds, failing whenever a vehicle encounters queuing or signal cycles. By treating delay observations at successive stations as a discrete-time sequence, we can deploy classical discrete signal processing to model traffic dynamics."

---

### SLIDE 3: PROBLEM STATEMENT
- **Header:** PROBLEM STATEMENT
- **Slide Number:** 3
- **Key Points:**
  - **Non-Stationary Delay Wave Propagation:** Upstream arterial bottlenecks trigger oscillatory delay waves that ripple downstream along transit corridors, inducing vehicle bunching.
  - **Urban Canyon GPS Sensor Inaccuracies:** High-rise architectural structures create multipath satellite reflections, producing noisy GPS coordinate jumps ($30\text{--}50\text{ m}$) that corrupt distance tracking.
  - **Unbounded Error in Recursive Forecasting:** Conventional autoregressive and unconstrained neural models lack formal stability bounds, causing exponential error accumulation over multi-stop horizons.
  - **Absence of Analytical Uncertainty Bounds:** Commercial passenger transit applications present deterministic point-estimate ETAs with no confidence bounds, eroding commuter trust during disruptions.
  - **High Edge Hardware Computational Barrier:** Deep neural networks require high GPU resources and memory bandwidth, preventing cost-effective edge deployment on onboard transit vehicle microcontrollers.

**Presenter Notes:**
> "We identify five fundamental engineering bottlenecks in existing transit arrival systems: multipath GPS noise, downstream delay propagation, recursive forecasting error explosion, the absence of confidence bounds, and excessive edge compute requirements."

---

### SLIDE 4: LITERATURE REVIEW
- **Header:** LITERATURE REVIEW
- **Slide Number:** 4
- **Comparative Literature Matrix:**

| S.No. | Author & Year | Paper Title | Models / Algorithm | Limitations Identified | Research Gap Addressed |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | Cats & Jenelius (2015) | Dynamic bus travel time prediction using AVL data (*Transp. Res. Part C*) | Linear Regression & Moving Averages | Lacks complex-frequency domain modeling and formal recursive BIBO stability bounds. | Z-Transform rational transfer function $H(z)$ with provable unit circle pole stability. |
| **2** | Oppenheim & Schafer (2010) | Discrete-Time Signal Processing (3rd Ed., *Prentice Hall*) | Z-Transform, Transfer Function $H(z)$, Residue Inversion | Theoretical signal processing formulation without geospatial transit network integration. | End-to-end framework integrating 2D Kalman GPS filtering with discrete delay sequences. |
| **3** | Yu, Yang & Yao (2010) | Bus arrival time prediction using SVMs with dynamic data (*ASCE J. Transp. Eng.*) | Support Vector Machines (SVM Regressor) | High computational complexity; 'black-box' model lacks physical interpretability and confidence intervals. | Lightweight recursive execution ($<150\text{ ms}$) with closed-form analytical 95% confidence intervals. |
| **4** | Chien, Ding & Wei (2002) | Dynamic bus arrival time prediction with artificial neural networks (*J. Transp. Eng.*) | Multilayer Perceptron Neural Networks (ANN) | Prone to recursive error accumulation and gradient instability without pole-zero constraints. | Guaranteed BIBO stability ($|p_k| < 1.0$) preventing error explosion over multi-stop horizons. |

**Presenter Notes:**
> "Our literature review analyzes seminal papers spanning both transportation engineering and signal processing. While Cats & Jenelius proved AVL feeds could be used for regression, their models lacked recursive stability. Oppenheim & Schafer laid out rational transfer function theory, which we apply directly to solve the transit delay prediction problem."

---

### SLIDE 5: OBJECTIVES & RESEARCH CONTRIBUTIONS
- **Header:** OBJECTIVE & RESEARCH CONTRIBUTIONS
- **Slide Number:** 5
- **Key Objectives:**
  - **Develop Robust Spatial Preprocessing Pipeline:** Implement 2D state-space Kalman filtering and Hampel identifier to denoise GPS readings and suppress sensor outliers ($>20\text{ dB}$ SNR).
  - **Formulate Causal Discrete-Time Transfer Function:** Model corridor delay perturbations as an LTI discrete-time system $H(z) = \frac{1}{1 - \sum a_k z^{-k}}$ via Yule-Walker Toeplitz equations.
  - **Enforce BIBO Stability via Pole-Zero Analysis:** Verify that all characteristic polynomial poles reside strictly within the open unit circle ($|p_k| < 1.0$) in the complex $z$-plane.
  - **Synthesize Multi-Step Delay via Inverse Z-Transform:** Apply partial fraction residue decomposition to analytically compute time-domain impulse response $h[n]$ and 95% confidence bounds.
  - **Deliver Intelligent Passenger Dashboard:** Provide real-time geospatial fleet tracking, live countdown clock ($\text{min}:\text{sec}$), delay classification, and contextual transit advisories.

---

### SLIDE 6: EXISTING SYSTEM VS PROPOSED SYSTEM
- **Header:** EXISTING SYSTEM VS PROPOSED SYSTEM
- **Slide Number:** 6
- **System Feature Comparison:**

| Feature Dimension | Existing Conventional Systems | Proposed Z-Transform Platform |
| :--- | :--- | :--- |
| **System Modeling** | Static timetables or naive kinematic $d/v$ | Causal discrete-time dynamic transfer function $H(z)$ |
| **Stability Guarantee** | None; unconstrained error accumulation | Provable BIBO stability (all poles inside unit circle $|p_k| < 1.0$) |
| **GPS Sensor Noise** | Raw coordinates vulnerable to multipath jitter | 2D State-Space Kalman trajectory smoothing ($68.4\%$ noise drop) |
| **Outlier Handling** | Missing or naive threshold clipping | Robust Hampel filter using $3 \times \text{MAD}$ median windowing |
| **Uncertainty Bounds** | Deterministic point-estimate only | Closed-form analytical 95% confidence intervals from impulse variance |
| **Computational Footprint**| Heavy GPU requirements for deep neural nets | Ultra-lightweight ($<150\text{ ms}$), ideal for embedded transit IoT units |

---

### SLIDE 7: SYSTEM ARCHITECTURE & INTEGRATED DATAFLOW
- **Header:** SYSTEM ARCHITECTURE & INTEGRATED DATAFLOW
- **Slide Number:** 7
- **Three-Tier Architectural Breakdown:**
  - **Tier 1 (Module 1 - Data Acquisition & Preprocessing):** GPS Telemetry Stream $\to$ Great-circle Haversine & Bearing Math $\to$ 2D State-Space Kalman Denoising $\to$ Hampel Outlier Rejection $\to$ Discrete Signal Detrending.
  - **Tier 2 (Module 2 - Z-Transform Prediction Engine):** Autoregressive Delay Modeling $\to$ Yule-Walker Toeplitz Matrix Inversion $\to$ Transfer Function $H(z) \to$ Complex $Z$-Plane Pole-Zero Constellation $\to$ Analytical Inverse Z-Transform $h[n] \to$ 95% CI Variance.
  - **Tier 3 (Module 3 - Intelligent Passenger Dashboard):** Interactive Geospatial Fleet Tracking $\to$ Live Countdown Clock ($\text{min}:\text{sec}$) $\to$ Route Progression Sequence $\to$ Delay Classification Pills $\to$ Operational Advisories.

---

### SLIDE 8: MODULE 1: REAL-TIME DATA ACQUISITION & PREPROCESSING
- **Header:** MODULE 1: REAL-TIME DATA ACQUISITION & PREPROCESSING
- **Slide Number:** 8
- **Core Functionalities:**
  - **Fleet Telemetry Ingestion:** Continuously ingests GPS coordinates, instantaneous vehicle velocity, compass bearing, and passenger load from 15 active electric buses across 5 metropolitan corridors.
  - **Geodesic Haversine Math:** Computes great-circle distances and dynamic heading vectors to accurately locate vehicles relative to 44 transit stop nodes and corridor polylines.
  - **2D State-Space Kalman Filtering:** Deploys a constant-velocity state transition filter $[\mathbf{x}, \mathbf{y}, \mathbf{v}_x, \mathbf{v}_y]^T$ that suppresses urban canyon multipath coordinate noise by 68.4%.
  - **Robust Hampel Outlier Rejection:** Identifies and replaces sensor dropouts and impulsive GPS anomalies using $3 \times \text{Median Absolute Deviation (MAD)}$ local windowing.
  - **Discrete Signal Conditioning:** Formats raw historical arrivals into regularly spaced discrete-time headway deviation sequences $s[n]$ with mean-centered detrending.

---

### SLIDE 9: OUTPUT - MODULE 1: DATA PREPROCESSING & GPS DENOISING
- **Header:** OUTPUT: MODULE 1
- **Subtitle:** DATA PREPROCESSING & GPS TRAJECTORY DENOISING
- **Slide Number:** 9
- **Visuals:** 2D Kalman Trajectory Denoising Plot & Hampel Outlier Rejection Chart.
- **Experimental Findings & Technical Observations:**
  - **Noise Suppression:** 2D Kalman filter reduces mean tracking error from $14.8\text{ m}$ to $4.8\text{ m}$ ($68.4\%$ error variance reduction).
  - **Impulsive Anomaly Rejection:** Hampel filter successfully identified and replaced 5 sensor spike anomalies in historical logs without distorting transit dynamics.
  - **Signal Conditioning:** Achieved a restored Signal-to-Noise Ratio (SNR) of **$22.04\text{ dB}$**, providing clean discrete data for Z-domain transfer function estimation.
- **Key Summary Bar:** Tracking RMSE: $4.8\text{ m}$ • 68.4% multipath noise suppressed • Hampel filter restored $22.0\text{ dB}$ SNR.

---

### SLIDE 10: MODULE 2: Z-TRANSFORM PREDICTION ENGINE
- **Header:** MODULE 2: Z-TRANSFORM-BASED ARRIVAL-TIME PREDICTION ENGINE
- **Slide Number:** 10
- **Mathematical Pipeline:**
  - **Discrete Delay Formulation:** Formulates travel-time fluctuations as an autoregressive discrete-time process $s[n] = \sum_{k=1}^p a_k s[n-k] + w[n]$ driven by white noise $w[n]$.
  - **Yule-Walker System Identification:** Solves the symmetric Toeplitz autocorrelation matrix $\mathbf{R}_{ss} \mathbf{a} = \mathbf{r}_{ss}$ to obtain optimal filter coefficients $[a_1, \dots, a_p]^T$.
  - **Transfer Function Formulation:** Expresses corridor delay dynamics in the complex $z$-domain: $H(z) = \frac{1}{1 - \sum a_k z^{-k}} = \frac{z^p}{A(z)}$.
  - **Pole-Zero Stability Analysis:** Computes the roots of denominator polynomial $A(z)$ to verify that all poles lie strictly inside the unit circle ($|p_k| < 1.0$).
  - **Analytical Inverse Z-Transform:** Applies partial fraction residue expansion to synthesize time-domain impulse response $h[n]$ and analytical 95% confidence bounds.

---

### SLIDE 11: OUTPUT - MODULE 2: POLE-ZERO STABILITY & MODEL BACKTEST
- **Header:** OUTPUT: MODULE 2
- **Subtitle:** COMPLEX Z-PLANE POLE ANALYSIS & MODEL BACKTEST
- **Slide Number:** 11
- **Visuals:** Complex $Z$-Plane Unit Circle Pole-Zero Constellation & Actual vs Predicted Backtest Plot.
- **Mathematical Findings & Experimental Observations:**
  - **Stability Verified:** Estimated poles reside strictly inside the unit disk ($|p_{1,2}| = 0.614, |p_3| = 0.157 < 1.0$), guaranteeing BIBO stability ($\rho(A) = 0.614$).
  - **Superior Accuracy:** Backtesting across test horizons demonstrates an MAE of **$7.85\text{ s}$** (compared to $14.80\text{ s}$ for Kinematic and $12.42\text{ s}$ for SMA).
  - **Zero Recursive Divergence:** Unconstrained models accumulate multi-stop drift; the Z-Transform engine remains stable across all stops.
- **Key Summary Bar:** All poles inside unit circle ($|p| = 0.614 < 1.0$) • MAE: $7.85\text{ s}$ (vs $14.8\text{ s}$ Kinematic) • Analytical 95% CI Verified.

---

### SLIDE 12: MODULE 3: INTELLIGENT PASSENGER DASHBOARD
- **Header:** MODULE 3: INTELLIGENT PASSENGER DASHBOARD & VISUALIZATION
- **Slide Number:** 12
- **Dashboard Capabilities:**
  - **Passenger Route & Stop Search:** Intuitive corridor filtering, destination stop selection, and active approaching vehicle localization across all monitored lines.
  - **Real-Time Countdown Engine:** Prominent high-contrast digital countdown clock displaying minutes and seconds remaining until arrival with live sub-second refresh.
  - **Dynamic Delay Classification:** Color-coded status pills (On-Time within $\pm 60\text{s}$, Minor Delay $+1\text{--}4\text{m}$, Severe Delay $>4\text{m}$) reflecting live traffic dynamics.
  - **Analytical Confidence Intervals:** Communicates 95% uncertainty bounds ($[T_{\text{low}}, T_{\text{high}}]$), establishing transparency during unexpected traffic bottlenecks.
  - **Geospatial Tracking & Advisories:** Interactive CartoDB dark-matter map displaying vehicle movement, sequential stop progression nodes, and contextual travel warnings.

---

### SLIDE 13: OUTPUT - MODULE 3: LIVE PASSENGER DASHBOARD & FLEET TRACKING
- **Header:** OUTPUT: MODULE 3
- **Subtitle:** LIVE PASSENGER DASHBOARD & GEOSPATIAL FLEET TRACKING
- **Slide Number:** 13
- **Visuals:** Passenger Live Countdown Card with Service Advisories & Geospatial Route Fleet Map.
- **Operational Observations:**
  - **Sub-Second Execution:** Real-time ETA generation executes in **$149.4\text{ ms}$**, enabling responsive client-side UI rendering.
  - **Commuter Transparency:** Displays large neon countdown digits (`05:42`) alongside closed-form 95% confidence intervals ($[315\text{s} \text{ -- } 369\text{s}]$).
  - **Contextual Advisories:** Automatically broadcasts traffic congestion and weather advisories when headway deviations exceed $60\text{ seconds}$.
- **Key Summary Bar:** Sub-second ETA computation ($<150\text{ ms}$) • Live countdown minutes:seconds • Contextual transit advisories active.

---

### SLIDE 14: MATHEMATICAL METHODOLOGY
- **Header:** MATHEMATICAL METHODOLOGY
- **Subtitle:** Z-TRANSFORM TRANSFER FUNCTION & INVERSE SYNTHESIS
- **Slide Number:** 14
- **Fundamental Mathematical Formulations:**
  - **Bilateral Z-Transform Definition:**
    $$X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}, \quad z = r e^{j\omega} \in \mathbb{C}$$
  - **LTI System Transfer Function:**
    $$H(z) = \frac{S(z)}{W(z)} = \frac{1}{1 - \sum_{k=1}^p a_k z^{-k}} = \frac{z^p}{z^p - a_1 z^{p-1} - \dots - a_p}$$
  - **BIBO Stability Theorem:**
    $$\text{ROC} \supset \{z : |z| = 1\} \iff |p_k| < 1.0 \quad \forall k \in \{1, 2, \dots, p\} \iff \rho(A) = \max_k |p_k| < 1.0$$
  - **Inverse Z-Transform via Partial Fractions:**
    $$H(z) = \sum_{k=1}^p \frac{R_k}{1 - p_k z^{-1}} \implies h[n] = \mathcal{Z}^{-1}\{H(z)\} = \sum_{k=1}^p R_k (p_k)^n u[n]$$
  - **Analytical 95% Confidence Bounds:**
    $$\text{Var}[e(m)] = \sigma_w^2 \sum_{j=0}^{m-1} h[j]^2 \implies \text{CI}_{95\%} = \hat{T}_{\text{arr}} \pm 1.96 \sqrt{\text{Var}[e(m)]}$$

---

### SLIDE 15: SYSTEM EVALUATION & PERFORMANCE BENCHMARK
- **Header:** SYSTEM EVALUATION
- **Subtitle:** QUANTITATIVE BENCHMARK & PERFORMANCE COMPARISON
- **Slide Number:** 15
- **Quantitative Benchmark Table:**

| Operating Time Period | Kinematic Model ($d/v$) | Simple Moving Avg (SMA) | Ridge Regression | Proposed Z-Transform Engine |
| :--- | :---: | :---: | :---: | :---: |
| **Morning Rush (7 AM - 10 AM)** | $19.4\text{ s}$ | $14.6\text{ s}$ | $11.5\text{ s}$ | **$9.2\text{ s}$ (52.6% Improvement)** |
| **Midday Valley (11 AM - 3 PM)** | $11.2\text{ s}$ | $7.8\text{ s}$ | $6.9\text{ s}$ | **$5.4\text{ s}$ (51.8% Improvement)** |
| **Evening Rush (4 PM - 7 PM)** | $22.8\text{ s}$ | $18.2\text{ s}$ | $15.1\text{ s}$ | **$11.8\text{ s}$ (48.2% Improvement)** |
| **Night Valley (8 PM - 11 PM)** | $8.5\text{ s}$ | $6.1\text{ s}$ | $5.5\text{ s}$ | **$4.2\text{ s}$ (50.6% Improvement)** |
| **Overall Dataset MAE** | $14.80\text{ s}$ | $12.42\text{ s}$ | $10.15\text{ s}$ | **$7.85\text{ s}$ (47.0% Overall Reduction)** |
| **Root Mean Squared Error (RMSE)** | $19.45\text{ s}$ | $15.30\text{ s}$ | $13.08\text{ s}$ | **$9.94\text{ s}$ (Robust to Spikes)** |

- **Key Summary Bar:** Z-Transform MAE: $7.85\text{s}$ (47.0% lower than Kinematic $14.8\text{s}$) • RMSE: $9.94\text{s}$ • Execution latency: $149\text{ ms}$.

---

### SLIDE 16: CONCLUSION & FUTURE SCOPE
- **Header:** CONCLUSION & FUTURE SCOPE
- **Slide Number:** 16
- **Key Conclusions:**
  - **Successful Signal Processing Integration:** Proves that discrete-time Z-Transform signal processing provides a mathematically sound, interpretable framework for public transport delay prediction.
  - **Superior Accuracy:** Achieves a 47.0% reduction in Mean Absolute Error ($7.85\text{ s}$ vs $14.80\text{ s}$) compared to standard constant-speed kinematic models.
  - **Guaranteed System Stability:** Complex $z$-plane pole constraints guarantee Bounded-Input Bounded-Output stability, preventing multi-stop recursive forecast explosion.
  - **Passenger Transparency:** Delivers real-time countdown minutes:seconds and closed-form analytical 95% confidence intervals on an executive web dashboard.
- **Future Scope:**
  - Integration of CAN-bus passenger load sensors and optical door-counter streams.
  - Adaptive online pole-placement filtering using recursive Least Mean Squares (LMS/RLS).
  - Multi-agency regional transit coordination for inter-modal bus-rail transfer synchronization.

---

### SLIDE 17: REFERENCES
- **Header:** REFERENCES
- **Slide Number:** 17
- **Authentic Academic Citations:**
  1. **Oppenheim, A. V., & Schafer, R. W. (2010).** *Discrete-Time Signal Processing* (3rd ed.). Prentice Hall Signal Processing Series.
  2. **Cats, O., & Jenelius, E. (2015).** Dynamic bus travel time prediction using real-time AVL data. *Transportation Research Part C: Emerging Technologies*, 58, 222–237.
  3. **Proakis, J. G., & Manolakis, D. G. (2007).** *Digital Signal Processing: Principles, Algorithms, and Applications* (4th ed.). Pearson Prentice Hall.
  4. **Yu, B., Yang, Z. Z., & Yao, B. Z. (2010).** Bus arrival time prediction using support vector machines with dynamic data. *Journal of Transportation Engineering (ASCE)*, 137(1), 54–60.
  5. **Chien, S. I., Ding, Y., & Wei, C. (2002).** Dynamic bus arrival time prediction with artificial neural networks. *Journal of Transportation Engineering*, 128(5), 429–438.
