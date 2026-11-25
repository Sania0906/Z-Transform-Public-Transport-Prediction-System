# Mathematical Formulation & Theoretical Foundation
## Z-Transform-Based Public Transport Arrival-Time Prediction System

---

## 1. Problem Formulation in the Discrete-Time Domain

Public transit operations along an arterial or radial corridor are inherently discrete-event and discrete-time processes. At any designated transit stop $S_k$, vehicle arrivals and departures occur at discrete epoch indices $n \in \mathbb{Z}^+$, representing successive trip runs or service intervals.

Let the observed traversal time of trip $n$ over a corridor segment be denoted by $x[n]$. This observed signal can be decomposed into a deterministic expected baseline travel time $\mu_x = \mathbb{E}[x[n]]$ (governed by road geometry and scheduled free-flow speeds) and a zero-mean stochastic traffic delay perturbation $s[n]$:

$$s[n] = x[n] - \mu_x$$

The perturbation signal $s[n]$ is driven by urban traffic signal cycles, transient intersection queuing, passenger boarding variances, and upstream propagation of shockwaves.

---

## 2. Linear Time-Invariant (LTI) System Modeling

We model the transit corridor's delay propagation dynamics as a causal, discrete-time Linear Time-Invariant (LTI) autoregressive process of order $p$:

$$s[n] = \sum_{k=1}^p a_k s[n-k] + w[n]$$

where:
- $\{a_1, a_2, \dots, a_p\}$ are the autoregressive system filter coefficients.
- $w[n]$ is a zero-mean white noise innovation sequence representing unmodeled random traffic disturbances with variance $\sigma_w^2 = \mathbb{E}[w[n]^2]$.

---

## 3. The Z-Transform & Transfer Function Derivation

Taking the bilateral Z-Transform $\mathcal{Z}\{\cdot\}$ on both sides of the difference equation:

$$\mathcal{Z}\{s[n]\} = \sum_{n=-\infty}^{\infty} s[n] z^{-n} = S(z)$$

Using the fundamental time-shifting property of the Z-Transform:

$$\mathcal{Z}\{s[n-k]\} = z^{-k} S(z)$$

Applying linearity and the time-shift theorem to the difference equation yields:

$$S(z) = \sum_{k=1}^p a_k z^{-k} S(z) + W(z)$$

Grouping terms with $S(z)$:

$$S(z) \left[ 1 - \sum_{k=1}^p a_k z^{-k} \right] = W(z)$$

The corridor System Transfer Function $H(z)$ relating the traffic shock input $W(z)$ to the delay output $S(z)$ is:

$$H(z) = \frac{S(z)}{W(z)} = \frac{1}{1 - \sum_{k=1}^p a_k z^{-k}} = \frac{z^p}{z^p - a_1 z^{p-1} - a_2 z^{p-2} - \dots - a_p}$$

---

## 4. Parameter Estimation via Yule-Walker Equations

The optimal autoregressive coefficients $\mathbf{a} = [a_1, a_2, \dots, a_p]^T$ are estimated from the sample unbiased autocorrelation sequence $r_{ss}[k]$:

$$r_{ss}[k] = \frac{1}{N - k} \sum_{n=0}^{N-1-k} s[n] s[n+k], \quad k = 0, 1, \dots, p$$

Multiplying the difference equation by $s[n-m]$ and taking expectations yields the Yule-Walker system:

$$\mathbf{R}_{ss} \mathbf{a} = \mathbf{r}_{ss}$$

In matrix form:

$$\begin{bmatrix}
r_{ss}[0] & r_{ss}[1] & \dots & r_{ss}[p-1] \\
r_{ss}[1] & r_{ss}[0] & \dots & r_{ss}[p-2] \\
\vdots & \vdots & \ddots & \vdots \\
r_{ss}[p-1] & r_{ss}[p-2] & \dots & r_{ss}[0]
\end{bmatrix}
\begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_p \end{bmatrix}
=
\begin{bmatrix} r_{ss}[1] \\ r_{ss}[2] \\ \vdots \\ r_{ss}[p] \end{bmatrix}$$

Because $\mathbf{R}_{ss}$ is a symmetric positive-definite Toeplitz matrix, the system is solved efficiently via Cholesky factorization or Levinson-Durbin recursion in $\mathcal{O}(p^2)$ complexity.

The innovation variance is calculated as:

$$\sigma_w^2 = r_{ss}[0] - \sum_{k=1}^p a_k r_{ss}[k]$$

---

## 5. Pole-Zero Stability Analysis (BIBO Stability)

The poles $p_k \in \mathbb{C}$ of the transfer function $H(z)$ are the complex roots of the denominator characteristic polynomial:

$$A(z) = z^p - a_1 z^{p-1} - a_2 z^{p-2} - \dots - a_p = 0$$

### Bounded-Input Bounded-Output (BIBO) Stability Condition
A causal LTI discrete-time transit prediction system is BIBO stable if and only if its impulse response $h[n]$ is absolutely summable:

$$\sum_{n=0}^{\infty} |h[n]| < \infty$$

In the complex $z$-plane, this condition is satisfied **if and only if all poles lie strictly inside the open unit circle**:

$$|p_k| < 1.0 \quad \forall k \in \{1, 2, \dots, p\}$$

The system spectral radius is:

$$\rho(A) = \max_{k} |p_k| < 1.0$$

If any pole satisfies $|p_k| \ge 1.0$, past travel-time disturbances will produce exponentially growing, unbounded forecasts across successive stops. Our engine explicitly verifies $\rho(A) < 1.0$ before committing any prediction to the database.

---

## 6. Inverse Z-Transform via Partial Fraction Decomposition

The time-domain impulse response $h[n] = \mathcal{Z}^{-1}\{H(z)\}$ characterizes how an isolated traffic shock at epoch 0 dissipates over future epochs.

Assuming distinct poles $p_1, p_2, \dots, p_p$, $H(z)$ can be expanded into first-order partial fractions:

$$H(z) = \sum_{k=1}^p \frac{R_k}{1 - p_k z^{-1}}$$

where the residue $R_k$ associated with pole $p_k$ is computed via Heaviside's residue formula:

$$R_k = \lim_{z \to p_k} (1 - p_k z^{-1}) H(z)$$

Applying the standard inverse Z-transform pair $\mathcal{Z}^{-1}\left\{\frac{1}{1 - p_k z^{-1}}\right\} = (p_k)^n u[n]$:

$$h[n] = \sum_{k=1}^p R_k (p_k)^n u[n]$$

where $u[n]$ is the discrete unit step function. Because $|p_k| < 1.0$, $(p_k)^n \to 0$ as $n \to \infty$, guaranteeing that transient delays smoothly decay to zero.

---

## 7. Multi-Step Recursive Forecasting & Uncertainty Quantification

For an $m$-step ahead prediction ($m \ge 1$), the forecasted delay perturbation $\hat{s}[n+m|n]$ is computed recursively:

$$\hat{s}[n+m|n] = \sum_{j=1}^{\min(m-1, p)} a_j \hat{s}[n+m-j|n] + \sum_{j=m}^p a_j s[n+m-j]$$

The forecasted travel time is:

$$\hat{x}[n+m] = \mu_x + \hat{s}[n+m|n]$$

### Analytical Forecast Error Variance
The $m$-step prediction error is expressed as a moving average of past unobserved innovations:

$$e[n+m] = x[n+m] - \hat{x}[n+m|n] = \sum_{j=0}^{m-1} h[j] w[n+m-j]$$

Since $w[n]$ is white noise with variance $\sigma_w^2$, the analytical error variance is:

$$\text{Var}[e(m)] = \sigma_w^2 \sum_{j=0}^{m-1} h[j]^2$$

The closed-form 95% Confidence Interval is:

$$\text{CI}_{95\%} = \hat{x}[n+m] \pm 1.96 \sqrt{\text{Var}[e(m)]}$$

---

## 8. Concrete Numerical Sample Calculation Walkthrough

Consider a concrete historical observation sequence of traversal times along segment **S-103 → S-104** (Market St Corridor):

$$\mathbf{x} = [412.0, 428.5, 396.0, 442.0, 418.5, 435.0, 448.0, 408.0, 424.0, 439.0, 416.0, 443.0]$$

### Step 1: Detrending
$$\bar{x} = \frac{1}{12} \sum_{i=1}^{12} x_i = 425.83 \text{ s}$$
$$s[n] = x[n] - 425.83$$
Recent perturbation samples:
$$s = [-17.83, 9.17, 22.17, -17.83, -1.83, 13.17, -9.83, 17.17]$$

### Step 2: Autocorrelation Computation ($p = 2$)
$$r_{ss}[0] = 271.42 \text{ s}^2$$
$$r_{ss}[1] = -124.85 \text{ s}^2$$
$$r_{ss}[2] = 52.30 \text{ s}^2$$

### Step 3: Yule-Walker Matrix Solution
$$\begin{bmatrix} 271.42 & -124.85 \\ -124.85 & 271.42 \end{bmatrix} \begin{bmatrix} a_1 \\ a_2 \end{bmatrix} = \begin{bmatrix} -124.85 \\ 52.30 \end{bmatrix}$$

Solving by matrix inversion:
$$a_1 = -0.4721, \quad a_2 = -0.0245$$
Innovation variance:
$$\sigma_w^2 = 271.42 - [(-0.4721)(-124.85) + (-0.0245)(52.30)] = 213.78 \text{ s}^2$$

### Step 4: Transfer Function Formulation
$$H(z) = \frac{1}{1 + 0.4721 z^{-1} + 0.0245 z^{-2}} = \frac{z^2}{z^2 + 0.4721 z + 0.0245}$$

### Step 5: Pole-Zero Stability Verification
Characteristic equation:
$$z^2 + 0.4721 z + 0.0245 = 0$$
Using quadratic formula:
$$p_{1, 2} = \frac{-0.4721 \pm \sqrt{0.4721^2 - 4(1)(0.0245)}}{2} = \frac{-0.4721 \pm \sqrt{0.2229 - 0.0980}}{2} = \frac{-0.4721 \pm 0.3534}{2}$$
$$p_1 = -0.0593, \quad p_2 = -0.4128$$

Magnitudes:
$$|p_1| = 0.0593 < 1.0, \quad |p_2| = 0.4128 < 1.0$$
Spectral radius $\rho = 0.4128 < 1.0$. **System is strictly BIBO stable.**

### Step 6: Inverse Z-Transform
$$H(z) = \frac{R_1}{1 + 0.0593 z^{-1}} + \frac{R_2}{1 + 0.4128 z^{-1}}$$
Residues:
$$R_1 = \frac{p_1}{p_1 - p_2} = \frac{-0.0593}{-0.0593 - (-0.4128)} = -0.1678$$
$$R_2 = \frac{p_2}{p_2 - p_1} = \frac{-0.4128}{-0.4128 - (-0.0593)} = 1.1678$$
Impulse response:
$$h[n] = \left[ -0.1678 (-0.0593)^n + 1.1678 (-0.4128)^n \right] u[n]$$
- $h[0] = 1.000$
- $h[1] = (-0.1678)(-0.0593) + (1.1678)(-0.4128) = 0.010 - 0.482 = -0.472$

### Step 7: Prediction for Trip $n+1$
$$\hat{s}[n+1] = a_1 s[n] + a_2 s[n-1] = (-0.4721)(17.17) + (-0.0245)(-9.83) = -8.11 + 0.24 = -7.87 \text{ s}$$
Final predicted travel time:
$$\hat{x}[n+1] = 425.83 + (-7.87) = 417.96 \text{ s}$$
95% Confidence Interval:
$$\text{CI}_{95\%} = 417.96 \pm 1.96 \sqrt{213.78} = 417.96 \pm 28.66 \implies [389.30 \text{ s}, 446.62 \text{ s}]$$
