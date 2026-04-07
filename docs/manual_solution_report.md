# Implementation of Laplace Transform and Fourier Series
## Mathematics III Assignment Report Notes

## Cover Page Details
- Assignment Title: Implementation of Laplace Transform and Fourier Series
- Student Name: Pratham Nagpal
- Student ID: 2024A7PS0071U
- Section: L4
- Instructor Name: Dr. Soma Sundaram
- Date of Submission: 8 April 2026

## Purpose Of This Document
This document is written to match the submission expectations in `guidlines.txt`. It explains:
- the two selected problems
- the manual solution method
- the coding approach used in Python
- the interpretation of the generated graphs
- the real-life applications

The two selected topics are from different parts of the course:
1. Laplace Transform: Spring-Mass-Damper System
2. Fourier Series: Signal Representation for Audio Compression

## Problem 1: Laplace Transform Application
### Problem Description
The spring-mass-damper system is modeled by the differential equation

`m y'' + c y' + k y = F(t)`

where:
- `m` is the mass
- `c` is the damping coefficient
- `k` is the spring constant
- `F(t)` is the external force
- `y(t)` is the displacement

In the implemented example, the app uses the default values:
- `m = 1.0`
- `c = 0.45`
- `k = 4.0`
- `force_amplitude = 1.0`

The forcing function used in the simulation is sinusoidal:

`F(t) = A sin(omega t)`

where `A = 1.0` and `omega = 0.85 sqrt(k / m)`.

### Manual Procedure And Method
Start from the differential equation:

`m y'' + c y' + k y = F(t)`

Take the Laplace transform of both sides:

`m L{y''} + c L{y'} + k L{y} = L{F(t)}`

Using the standard formulas:
- `L{y'} = sY(s) - y(0)`
- `L{y''} = s^2 Y(s) - s y(0) - y'(0)`

So,

`m[s^2 Y(s) - s y(0) - y'(0)] + c[sY(s) - y(0)] + kY(s) = F(s)`

Assuming zero initial conditions:
- `y(0) = 0`
- `y'(0) = 0`

the equation becomes:

`m s^2 Y(s) + c s Y(s) + k Y(s) = F(s)`

Factor out `Y(s)`:

`Y(s) [m s^2 + c s + k] = F(s)`

Therefore,

`Y(s) = F(s) / (m s^2 + c s + k)`

This is the transformed solution. It shows that the output displacement in the Laplace domain is the input force divided by the system polynomial.

### Substituting The Chosen Force
For

`F(t) = A sin(omega t)`

the Laplace transform is

`F(s) = A omega / (s^2 + omega^2)`

Hence,

`Y(s) = A omega / [(s^2 + omega^2)(m s^2 + c s + k)]`

For the default values used in the app:
- `m = 1`
- `c = 0.45`
- `k = 4`
- `omega = 0.85 sqrt(4/1) = 1.7`
- `A = 1`

so the transformed displacement becomes

`Y(s) = 1.7 / [(s^2 + 1.7^2)(s^2 + 0.45 s + 4)]`

This formula is the manual transformed result that explains the behavior of the system.

### Interpretation
The denominator

`m s^2 + c s + k`

controls the physical behavior of the system:
- the `m s^2` term represents inertia
- the `c s` term represents damping
- the `k` term represents stiffness

If damping is small, the response oscillates for longer time. If damping increases, the oscillations decay faster.

### Why Numerical Simulation Was Also Used
The transformed expression is correct mathematically, but the graph in the application was generated numerically because:
- it is faster to produce time-domain points for plotting
- it avoids lengthy inverse Laplace expansion
- it lets the user change parameters interactively

So the manual solution establishes the transformed model, while the code generates the final plotted response.

## Algorithm / Coding Approach For Problem 1
The Laplace feature is implemented in Python as follows:
1. Accept the physical parameters `m`, `c`, `k`, `force_amplitude`, `time_end`, and `num_points`.
2. Compute the driving frequency from the natural frequency.
3. Convert the second-order equation into a first-order system:
   - `y1 = y`
   - `y2 = y'`
   - `y1' = y2`
   - `y2' = (F(t) - c y2 - k y1) / m`
4. Solve the system numerically using `scipy.integrate.solve_ivp`.
5. Return arrays for time, displacement, velocity, and forcing.
6. Plot the returned arrays in the frontend.

This implementation is in:
- [applications_service.py](/C:/Users/prath/OneDrive/Desktop/Maths-3/Trial%202/app/services/applications_service.py#L63)

## Expected Output For Problem 1
The graph shows:
- time on the x-axis
- displacement on the y-axis
- the forcing curve for comparison

You should include:
- one screenshot of the code
- one screenshot of the output graph
- a short note stating how changing `c` changes damping behavior

## Error Analysis For Problem 1
For the Laplace simulation, error analysis is based on the numerical solver tolerance and the residual of the original differential equation:

`residual = m y'' + c y' + k y - F(t)`

The app reports:
- whether the ODE solver succeeded
- relative tolerance
- absolute tolerance
- maximum ODE residual
- mean ODE residual

This is useful because it shows whether the plotted numerical result is consistent with the original differential equation.

## Real-Life Application Of Problem 1
This model appears in:
- car suspension systems
- shock absorbers
- machine vibration control
- earthquake-resistant structural design

The importance of Laplace transform here is that it converts a difficult differential-equation problem into an algebraic form that is easier to analyze.

## Problem 2: Fourier Series Application
### Problem Description
The second selected problem is based on the Fourier series of

`f(x) = x` on the interval `[-pi, pi]`

This is used as a model to explain signal decomposition and the basic idea behind audio compression.

### Manual Procedure And Method
The general Fourier series is

`f(x) = a0/2 + sum(an cos(nx) + bn sin(nx))`

where

`a0 = (1/pi) integral from -pi to pi of f(x) dx`

`an = (1/pi) integral from -pi to pi of f(x) cos(nx) dx`

`bn = (1/pi) integral from -pi to pi of f(x) sin(nx) dx`

For `f(x) = x`, note that:
- `x` is an odd function
- `cos(nx)` is even
- `sin(nx)` is odd

So:
- `x cos(nx)` is odd, therefore `an = 0`
- `x` itself is odd, therefore `a0 = 0`

Only the sine coefficients remain.

### Finding `bn`

`bn = (1/pi) integral from -pi to pi of x sin(nx) dx`

Since the integrand is even, we can write

`bn = (2/pi) integral from 0 to pi of x sin(nx) dx`

Use integration by parts:
- let `u = x`, so `du = dx`
- let `dv = sin(nx) dx`, so `v = -cos(nx)/n`

Then

`integral x sin(nx) dx = -x cos(nx)/n + integral cos(nx)/n dx`

Therefore,

`integral x sin(nx) dx = -x cos(nx)/n + sin(nx)/n^2`

Now apply limits from `0` to `pi`:

`integral from 0 to pi of x sin(nx) dx = [-x cos(nx)/n + sin(nx)/n^2] from 0 to pi`

Since `sin(n pi) = 0` and `cos(n pi) = (-1)^n`,

the result becomes

`-pi (-1)^n / n`

Thus,

`bn = (2/pi) * [-pi (-1)^n / n]`

which simplifies to

`bn = 2 (-1)^(n+1) / n`

### Final Fourier Series
So the Fourier series for `f(x) = x` is

`x = 2 sum[(-1)^(n+1) sin(nx) / n]`

This is the exact manual result used in the application.

### Visible Fourier Coefficients
The application also displays the coefficient values used in the approximation:
- `a0 = 0`
- `an = 0` for all `n`
- `bn = 2(-1)^(n+1)/n`

Examples:
- `b1 = 2`
- `b2 = -1`
- `b3 = 0.6667`
- `b4 = -0.5`

These values help show how the Fourier approximation is actually built term by term.
The application also plots these coefficients against the term index `n`. The `an` values appear as a zero line because `f(x)=x` is odd, while the `bn` values alternate sign and reduce in size as `n` increases.

### Interpretation
This result shows that a nontrivial waveform can be built using a sum of sine waves. That is the key idea behind signal decomposition:
- a complicated signal can be expressed as simple frequency components
- keeping only the important components gives an approximation
- this idea is the mathematical basis for compression

## Algorithm / Coding Approach For Problem 2
The Fourier feature is implemented in Python as follows:
1. Create a set of x-values on `[-pi, pi]`.
2. Store the original function `signal = x`.
3. Initialize an array for the approximation.
4. For each `n` from `1` to `terms`, add

   `2 (-1)^(n+1) sin(nx) / n`

   to the approximation.
5. Return the original signal and the truncated Fourier approximation.
6. Plot both curves together in the frontend.
7. Plot the Fourier coefficient values `an` and `bn` against the term index `n`.

This implementation is in:
- [applications_service.py](/C:/Users/prath/OneDrive/Desktop/Maths-3/Trial%202/app/services/applications_service.py#L153)

## Expected Output For Problem 2
The Fourier graph shows:
- the original line `f(x) = x`
- the approximation formed from a finite number of sine terms
- the coefficient plot for `an` and `bn`

You should include:
- one screenshot of the code
- one screenshot of the graph for a smaller number of terms
- one screenshot of the graph for a larger number of terms

This helps show that the approximation improves as more terms are included.

## Error Analysis For Problem 2
For the Fourier approximation, error analysis is calculated using:

`absolute error = |signal - approximation|`

The app reports:
- mean absolute error
- root mean square error
- maximum absolute error

This is useful for the report because it proves numerically that the approximation improves as more Fourier terms are added.

## Real-Life Application Of Problem 2
This concept is useful in:
- MP3 and audio compression
- music streaming
- voice transmission
- speech processing
- digital signal analysis

In real systems, the compression process is more advanced than a simple Fourier series, but the main mathematical idea is the same: represent a signal using frequency components and keep the most important information.

## Output Results Section You Can Use In The Final Report
### Result Summary
- The Laplace-transform model gave the transformed displacement equation for the spring-mass-damper system and showed how damping, stiffness, and forcing interact.
- The numerical graph confirmed oscillatory behavior and damping decay in the time domain.
- The Fourier-series model gave the coefficients for `f(x) = x` and showed how a sum of sine waves reconstructs the signal.
- The approximation graph confirmed that more terms produce a better reconstruction.

### Axis And Index Meaning
- Laplace graph: the x-axis is time `t` in seconds, and the y-axis is the system response value. Each plotted index is one sampled time point.
- Fourier graph: the x-axis is `x` in radians from `-pi` to `pi`, and the y-axis is signal amplitude. Each plotted index is one sampled `x` point.
- The downloaded graph contains axis labels and a visible legend so it can be used directly in the report.
- Laplace legend: dark teal means displacement `y(t)`, and green means applied force `F(t)`.
- Fourier legend: dark teal means original signal `f(x)=x`, and orange means Fourier approximation.

## Conclusion
This assignment showed how two important mathematical tools are used in practical systems.

Laplace transform was used to study a mechanical vibration model by converting the differential equation into an algebraic equation in the `s`-domain. This made the system structure easier to understand and connected the mathematics to real engineering systems.

Fourier series was used to express a signal as a sum of sine functions. This demonstrated how complex waveforms can be reconstructed from simpler frequency components and explained the basic idea behind audio compression.

Together, these two examples show that Mathematics III is not only theoretical but also directly useful in engineering, computation, and real-world modeling.

## References
1. Mathematics III course handout
2. Standard Laplace transform formulas from engineering mathematics
3. Standard Fourier series formulas for periodic functions
4. Python documentation for numerical scientific computing

## Final Submission Checklist
- Add instructor name on the cover page
- Add screenshots of the code from the Python project
- Add downloaded graphs from the application
- Export the final report as PDF
- Name the final PDF file as `2024A7PS0071U.pdf`
