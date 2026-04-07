# Implementation of Laplace Transform and Fourier Series
## Mathematics III Assignment Report

### Student Details
- Name: Pratham Nagpal
- Student ID: 2024A7PS0071U
- Section: L4
- Instructor Name: Dr. Soma Sundaram
- Date of Submission: 8 April 2026

## Abstract
This report presents two Mathematics III applications chosen from different topics: Laplace Transform and Fourier Series. The first problem studies a spring-mass-damper system, which is a standard model for mechanical vibration. The second problem studies the Fourier series of `f(x) = x` on `[-pi, pi]`, which provides a clean mathematical explanation of how signals can be decomposed into simpler frequency components. In both cases, the mathematical derivation is shown first, followed by the computational procedure used in Python. The final implementation includes numerical output and graphs so that the theory can be connected to practical engineering and signal-processing applications.

## Introduction
One of the main goals of Mathematics III is to show that topics such as differential equations, Laplace transforms, and Fourier series are not only theoretical ideas but also working tools used in engineering and applied computation. In this assignment, I selected two problems from two different parts of the course so that the report would reflect both mathematical understanding and programming-based execution.

The first selected application is the spring-mass-damper system. This example is useful because it connects a second-order differential equation to a real physical system. The second selected application is the Fourier series of `f(x) = x`, which is useful because it demonstrates how a nontrivial waveform can be reconstructed using trigonometric terms. Together, these two problems show how Mathematics III supports both mechanical modeling and signal analysis.

## Selected Problems
1. Laplace Transform application: Spring-Mass-Damper System
2. Fourier Series application: Signal representation for audio compression

## Problem 1: Laplace Transform Application
### Problem Statement
Consider the spring-mass-damper model governed by

`m y'' + c y' + k y = F(t)`

where `m` is mass, `c` is the damping coefficient, `k` is the spring constant, `F(t)` is the external force, and `y(t)` is the displacement. The objective is to solve the system using Laplace-transform ideas and explain the real-life significance of the result.

### Physical Meaning Of The Equation
This equation represents a body attached to a spring and a damper. The mass resists acceleration, the spring tries to pull the system back to equilibrium, and the damper reduces motion by dissipating energy. If an external force is applied, the body moves according to the balance of these three effects.

For the implemented model, the default values used in the application are:
- `m = 1.0`
- `c = 0.45`
- `k = 4.0`
- `force_amplitude = 1.0`

The forcing function used is

`F(t) = A sin(omega t)`

with `A = 1.0` and `omega = 0.85 sqrt(k / m) = 1.7`.

### Manual Solution Using Laplace Transform
We start with

`m y'' + c y' + k y = F(t)`

Taking Laplace transform on both sides gives

`m L{y''} + c L{y'} + k L{y} = L{F(t)}`

Using the standard Laplace formulas:
- `L{y'} = sY(s) - y(0)`
- `L{y''} = s^2 Y(s) - s y(0) - y'(0)`

substitution gives

`m[s^2Y(s) - s y(0) - y'(0)] + c[sY(s) - y(0)] + kY(s) = F(s)`

For this assignment, zero initial conditions were assumed:
- `y(0) = 0`
- `y'(0) = 0`

Therefore the equation simplifies to

`m s^2Y(s) + c sY(s) + kY(s) = F(s)`

Factoring `Y(s)`:

`Y(s)[m s^2 + c s + k] = F(s)`

Hence,

`Y(s) = F(s) / (m s^2 + c s + k)`

This is the transformed displacement. It shows that the system response in the Laplace domain depends on the forcing term divided by the characteristic polynomial of the system.

### Substituting The Chosen Forcing Function
For

`F(t) = A sin(omega t)`

the Laplace transform is

`F(s) = A omega / (s^2 + omega^2)`

So the transformed displacement becomes

`Y(s) = A omega / [(s^2 + omega^2)(m s^2 + c s + k)]`

Substituting the default values:
- `m = 1`
- `c = 0.45`
- `k = 4`
- `A = 1`
- `omega = 1.7`

gives

`Y(s) = 1.7 / [(s^2 + 1.7^2)(s^2 + 0.45s + 4)]`

This is the manually derived transformed solution used to explain the model.

### Interpretation Of The Result
The denominator

`s^2 + 0.45s + 4`

indicates that the system is underdamped. The damping ratio for the default values is

`zeta = c / (2 sqrt(mk)) = 0.45 / 4 = 0.1125`

Since the damping ratio is less than 1, the motion is oscillatory, but the amplitude gradually decays over time. This is exactly what is expected in a lightly damped vibration system such as a vehicle suspension or a machine mount.

The app now also classifies the damping case automatically. The classification uses the formula `zeta = c / (2 sqrt(mk))`. If `zeta < 1`, the system is underdamped and oscillates while the amplitude decays. If `zeta = 1`, the system is critically damped and returns to equilibrium as fast as possible without oscillating. If `zeta > 1`, the system is overdamped and returns to equilibrium without oscillating, but more slowly than the critically damped case.

### Why A Numerical Method Was Used In The Code
The Laplace-domain expression explains the mathematics clearly, but for plotting displacement against time, the application uses a numerical approach. This was done for three practical reasons:
- it is more convenient to generate time-domain points directly
- it avoids a long inverse-Laplace expansion
- it allows the user to change the system parameters interactively

So, the manual derivation shows the mathematics, while the numerical method produces the final graph.

### Computational Method For Problem 1
The second-order differential equation is converted into a first-order system:
- `y1 = y`
- `y2 = y'`
- `y1' = y2`
- `y2' = (F(t) - c y2 - k y1) / m`

The program then:
1. creates a time grid from `0` to `12` seconds
2. computes the sinusoidal forcing term
3. solves the first-order system using `scipy.integrate.solve_ivp`
4. returns arrays for time, displacement, velocity, and forcing
5. plots the results in the frontend

### Output Discussion For Problem 1
For the default parameter set used in the implementation:
- maximum displacement is approximately `0.8088`
- minimum displacement is approximately `-0.7995`
- displacement at the final sampled time is approximately `0.6407`

These values confirm that the response remains oscillatory but is bounded and shaped by damping. The graph also makes it clear that the forcing and displacement are not perfectly aligned, which is physically reasonable because the system has inertia and damping.

### Error Analysis For Problem 1
The application now includes numerical error analysis for the Laplace simulation. Since the solution is generated with `scipy.integrate.solve_ivp`, the solver uses strict tolerance values:
- relative tolerance: `1e-6`
- absolute tolerance: `1e-8`

The app also estimates the residual of the original differential equation using the sampled output:

`residual = m y'' + c y' + k y - F(t)`

For the default settings, the displayed residual values are small. The residual is not treated as a symbolic error because it is estimated from the plotted sample points. It is mainly used as a practical consistency check to show that the numerical curve still satisfies the original differential equation closely.

### Real-Life Application Of Problem 1
The spring-mass-damper system has many practical uses:
- car suspension systems
- shock absorbers
- machine vibration control
- building vibration analysis
- earthquake-resistant structural design

This is an important application of Laplace transform because it converts a difficult differential-equation problem into a much easier algebraic form in the `s`-domain.

## Problem 2: Fourier Series Application
### Problem Statement
The second selected problem is to determine the Fourier series of

`f(x) = x` on `[-pi, pi]`

and use the result to explain signal decomposition and the basic idea of audio compression.

### Why This Problem Is Useful
Audio signals are often complicated waveforms, but mathematically they can be expressed as combinations of simpler sine and cosine waves. Fourier series is one of the most important tools for understanding this decomposition. In this assignment, the function `f(x) = x` is used because it has a clean derivation and clearly shows how a waveform can be reconstructed from sine terms alone.

### Manual Solution Using Fourier Series
The general Fourier series is

`f(x) = a0/2 + sum(an cos(nx) + bn sin(nx))`

where

`a0 = (1/pi) integral from -pi to pi of f(x) dx`

`an = (1/pi) integral from -pi to pi of f(x) cos(nx) dx`

`bn = (1/pi) integral from -pi to pi of f(x) sin(nx) dx`

Now consider `f(x) = x`.

Because `x` is an odd function:
- `a0 = 0`

Also, `x cos(nx)` is odd, so:
- `an = 0`

Therefore only the sine coefficients `bn` remain.

### Determination Of `bn`
We calculate

`bn = (1/pi) integral from -pi to pi of x sin(nx) dx`

Since `x sin(nx)` is even, this becomes

`bn = (2/pi) integral from 0 to pi of x sin(nx) dx`

Using integration by parts:
- `u = x`, so `du = dx`
- `dv = sin(nx) dx`, so `v = -cos(nx)/n`

Then

`integral x sin(nx) dx = -x cos(nx)/n + sin(nx)/n^2`

Applying limits from `0` to `pi`:

`integral from 0 to pi of x sin(nx) dx = [-x cos(nx)/n + sin(nx)/n^2] from 0 to pi`

Now use:
- `sin(n pi) = 0`
- `cos(n pi) = (-1)^n`

This gives

`integral from 0 to pi of x sin(nx) dx = -pi (-1)^n / n`

Hence,

`bn = (2/pi)[-pi (-1)^n / n] = 2 (-1)^(n+1) / n`

### Final Fourier Series
Therefore,

`x = 2 sum[(-1)^(n+1) sin(nx) / n]`

This is the final manual solution for the selected Fourier-series problem.

### Visible Fourier Coefficients
The frontend also shows the actual Fourier coefficient values used in the approximation. For `f(x)=x`, the coefficients are:
- `a0 = 0`
- `an = 0` for all `n`, because `f(x)=x` is an odd function
- `bn = 2(-1)^(n+1)/n`

Some visible values are:
- for `n=1`, `b1 = 2`
- for `n=2`, `b2 = -1`
- for `n=3`, `b3 = 0.6667`
- for `n=4`, `b4 = -0.5`

These values are displayed in a coefficient table and a separate coefficient plot so that the graph is connected directly to the terms used in the Fourier approximation. In the coefficient plot, the x-axis represents the term index `n`, while the y-axis represents the coefficient value. The plot updates when the selected number of Fourier terms is changed, so choosing `n=20` displays coefficients from `1` to `20`. The cosine coefficients `an` lie on the zero line, and the sine coefficients `bn` alternate in sign while decreasing in magnitude.

### Interpretation Of The Result
This expansion proves that the original function can be reconstructed from sine waves. That is the main idea behind signal decomposition:
- a complicated shape can be expressed using simpler frequency components
- fewer terms give a rough approximation
- more terms give a more accurate reconstruction

This is exactly why Fourier methods are so useful in communication systems and signal processing.

### Computational Method For Problem 2
The Python implementation follows these steps:
1. generate sample points on `[-pi, pi]`
2. store the original function as `signal = x`
3. start with a zero approximation array
4. for each `n` from `1` to `terms`, add

   `2 (-1)^(n+1) sin(nx) / n`

   to the approximation
5. return both the original function and the approximation
6. plot the two curves together

### Output Discussion For Problem 2
To make the effect of truncation visible, the implementation was checked with different numbers of terms.

Observed mean absolute error values are:
- for `5` terms: approximately `0.3300`
- for `20` terms: approximately `0.1184`

This confirms that increasing the number of retained terms improves the approximation significantly. At the same time, some overshoot remains near the endpoints because of the Gibbs phenomenon, which is normal for truncated Fourier representations of functions with jump-like periodic extensions.

### Error Analysis For Problem 2
The Fourier section now calculates pointwise absolute error:

`absolute error = |original signal - Fourier approximation|`

It also reports:
- mean absolute error
- root mean square error
- maximum absolute error

For the report, the most useful value is the mean absolute error because it clearly shows improvement when more terms are included. In the implementation, the mean absolute error decreased from about `0.3300` with 5 terms to about `0.1184` with 20 terms. This confirms that increasing the number of Fourier terms improves the approximation.

### Real-Life Application Of Problem 2
This mathematical idea is directly connected to:
- MP3 and audio compression
- music streaming
- voice transmission
- speech processing
- digital signal analysis

Real compression systems are more advanced than a simple Fourier series, but the central idea is the same: represent the signal using frequency components and keep the most important information.

## Python Implementation Summary
The assignment was implemented in Python using:
- `FastAPI` for endpoint structure
- `NumPy` for numerical arrays
- `SciPy` for solving the vibration model
- a lightweight frontend for plotting and interaction

The backend is organized into:
- route definitions
- schema models
- service functions for mathematics and data generation
- static frontend assets

This structure keeps the code clean and makes it easy to connect theory, implementation, and visual output.

## Algorithm / Coding Approach
### Laplace Module
1. Receive input parameters.
2. Compute forcing frequency.
3. Convert the second-order equation to a first-order system.
4. Solve the system numerically.
5. Return chart-ready arrays.

### Fourier Module
1. Receive the requested number of terms.
2. Generate points on `[-pi, pi]`.
3. Build the approximation term by term.
4. Calculate visible coefficient values `a0`, `an`, and `bn`.
5. Return original signal, approximated signal, coefficient values, and error metrics.

This approach satisfies the assignment requirement of combining mathematical procedure with coding logic.

## Output Results And Graph Discussion
The Laplace graph shows how displacement changes with time for a forced, lightly damped system. The curve oscillates and gradually stabilizes because the damping coefficient removes energy from the system. The forcing curve is also displayed so that the relationship between input and response can be observed directly.

The Fourier graph shows the original signal together with the truncated Fourier approximation. For a small number of terms, the approximation is rough. When more terms are used, the reconstructed signal becomes closer to the original. This provides a direct visual demonstration of how Fourier methods improve with additional retained components.

The Fourier coefficient plot shows the actual coefficient values used to build the approximation. It changes with the selected value of `n`, so the plotted coefficient range matches the number of terms used in the waveform approximation. This makes it easier to see why the approximation is made mostly from sine terms for `f(x)=x`: all cosine coefficients are zero, while the sine coefficients contribute the alternating terms.

### Axis And Index Meaning
For the Laplace graph, the x-axis represents time `t` in seconds. The y-axis represents the system response values, mainly displacement `y(t)`, with the forcing signal shown as a comparison curve. Each plotted index corresponds to one sampled time value returned by the backend.

For the Fourier graph, the x-axis represents sampled `x` values in radians from `-pi` to `pi`. The y-axis represents signal amplitude for the original function and the Fourier approximation. Each plotted index corresponds to one sampled `x` value returned by the backend.

The downloaded graph image includes axis labels, a short guide line, and a visible color legend so that the saved graph is understandable when inserted into the final report. In the Laplace graph, the dark teal curve is the displacement `y(t)` and the green curve is the applied force `F(t)`. In the Fourier graph, the dark teal curve is the original signal `f(x)=x` and the orange curve is the Fourier approximation.

## Error Analysis Summary
The final application includes error analysis directly in the frontend. For the Laplace simulation, the app reports solver status, tolerance values, maximum ODE residual, and mean ODE residual. For the Fourier approximation, the app reports mean absolute error, root mean square error, maximum absolute error, and the number of terms used. This makes the output more complete because it does not only show the graph; it also gives numerical evidence about the quality of the computed result.

## Real-Life Applications
### Laplace Transform
Laplace transform is widely used in control systems, electrical circuits, vibration analysis, structural engineering, and mechanical design. It is especially useful when a system is modeled by differential equations and has nontrivial forcing or initial conditions.

### Fourier Series
Fourier series is widely used in telecommunications, sound engineering, image processing, filtering, and frequency-domain analysis. It forms the foundation for many compression and reconstruction techniques used in modern digital systems.

## Conclusion
This assignment showed how two important mathematical techniques from Mathematics III can be connected to real systems and implemented computationally. The spring-mass-damper model demonstrated how Laplace transform helps simplify and interpret a second-order differential equation. The Fourier-series example demonstrated how a function can be decomposed into sine components and reconstructed progressively.

Working through the manual derivation and then implementing the same ideas in Python made the concepts clearer. The manual work showed the underlying mathematics, while the code and graphs showed how the theory behaves in practice. This combination of mathematical reasoning, algorithmic thinking, and visual interpretation is the most useful outcome of the assignment.

## References
1. Simmons, G. F. *Differential Equations with Applications and Historical Notes*, 2nd ed., McGraw-Hill, 1991.
2. Braun, M. *Differential Equations and Their Applications: An Introduction to Applied Mathematics*, 4th ed., Springer, 1993.
3. Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., et al. "SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python." *Nature Methods*, vol. 17, 2020, pp. 261-272. https://doi.org/10.1038/s41592-019-0686-2
4. Oliphant, T. E. *A Guide to NumPy*. Trelgol Publishing, 2006.
5. SciPy Developers. "scipy.integrate.solve_ivp." *SciPy API Reference*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html
6. NumPy Developers. *NumPy Documentation*. https://numpy.org/doc/stable/
7. Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
8. FastAPI. *FastAPI Documentation*. https://fastapi.tiangolo.com/
9. Pydantic. *Pydantic Documentation*. https://docs.pydantic.dev/latest/
10. Uvicorn. *Uvicorn Documentation*. https://www.uvicorn.org/
11. pytest Development Team. *pytest Documentation*. https://docs.pytest.org/en/stable/
12. MDN Web Docs. "SVG: Scalable Vector Graphics." https://developer.mozilla.org/en-US/docs/Web/SVG
13. ReportLab. *ReportLab User Guide*. https://docs.reportlab.com/reportlab/userguide/ch1_intro/
14. Nagpal, Pratham. *Implementation of Laplace Transform and Fourier Series*. GitHub repository, 2026. https://github.com/Pratham71/Implementation-of-Laplace-Transform-and-Fourier-Series

## Final Submission Checklist
- Add instructor name before final submission
- Add one or two screenshots of the relevant code sections if required by the evaluator
- Include the downloaded graphs in the final PDF if a custom version is prepared later
- Submit the PDF through META LMS
- Use file name `2024A7PS0071U.pdf`
