# Implementation of Laplace Transform and Fourier Series

A Mathematics III web application that demonstrates two course topics through a working FastAPI backend and an interactive browser frontend.

## Student Details

- Name: Pratham Nagpal
- ID: 2024A7PS0071U
- Section: L4
- Instructor: Dr. Soma Sundaram

## What This Project Does

This project implements two applied mathematics demonstrations:

1. **Laplace Transform Application:** a spring-mass-damper vibration system governed by `m y'' + c y' + k y = F(t)`.
2. **Fourier Series Application:** reconstruction of `f(x)=x` on `[-pi, pi]` using a finite Fourier sine series.

The goal is to connect the manual Mathematics III theory with actual numerical computation and graph-based interpretation.

## Main Features

- FastAPI backend with typed JSON endpoints for both applications.
- Static frontend built with HTML, CSS, and vanilla JavaScript.
- Laplace simulation for displacement, velocity, and applied force.
- Laplace damping classification using `zeta = c / (2*sqrt(m*k))`.
- Visible damping regimes: underdamped, critically damped, and overdamped.
- Fourier approximation graph comparing the original signal and reconstructed signal.
- Fourier coefficient table showing `a0`, `a_n`, `b_n`, and the retained sine terms.
- Fourier coefficient plot that updates when the selected number of terms changes.
- Error analysis for both mathematical models.
- Axis guides and legends so downloaded graphs are report-ready.
- PNG download buttons for the generated graphs.
- Automated tests for API contracts and frontend hooks.

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- NumPy
- SciPy
- Uvicorn
- Pytest
- HTML
- CSS
- Vanilla JavaScript
- SVG charts

## Project Structure

```text
app/
  main.py
  routes/
    applications.py
  schemas/
    applications.py
  services/
    applications_service.py
  static/
    index.html
    styles.css
    app.js

tests/
  test_applications.py

requirements.txt
README.md
```

## API Endpoints

- `GET /api/applications/laplace`
  - Returns explanation content for the spring-mass-damper Laplace application.
- `GET /api/applications/laplace/simulate`
  - Returns chart-ready simulation data, ODE residual error metrics, and damping classification.
- `GET /api/applications/fourier`
  - Returns explanation content for the Fourier series application.
- `GET /api/applications/fourier/signal`
  - Returns original signal data, Fourier approximation data, coefficient values, and approximation error metrics.

## How To Run

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000/
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## How To Use The App

In the Laplace section, change the mass `m`, damping coefficient `c`, spring constant `k`, and force amplitude, then run the simulation. The app updates the graph, error analysis, and damping type.

In the Fourier section, change the number of terms `n` and update the approximation. The app updates the reconstructed wave, the coefficient table, and the coefficient plot.

Use the download buttons to save the graphs as PNG images for a report or presentation.

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/test_applications.py
```

## Notes

- This is a Python/FastAPI project, so there is no `npm run dev` workflow.
- The frontend is served directly by FastAPI from `app/static`.
- The `/docs` URL refers to FastAPI's generated API documentation, not a project folder.
- The project is intentionally lightweight: no database, no authentication, and no separate frontend build step.

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
