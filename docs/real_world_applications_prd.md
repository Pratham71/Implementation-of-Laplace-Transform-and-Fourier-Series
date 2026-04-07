# Implementation of Laplace Transform and Fourier Series
## Mathematics III Assignment

## Student Details
- Name: Pratham Nagpal
- ID: 2024A7PS0071U
- Section: L4

## Overview
Build a self-contained learning module that connects Mathematics III concepts to practical systems:

1. Laplace Transform -> Spring-Mass-Damper System
2. Fourier Series -> Audio Compression

The module should include:
- a FastAPI backend with structured educational content
- numeric endpoints for chart-ready data
- a frontend experience that presents the concepts clearly and interactively

The module is read-only. No database, login flow, or persistence is required.

## Product Goals
- Help a student connect abstract mathematics to real engineering and signal-processing examples.
- Provide backend responses that are stable enough for direct frontend rendering.
- Offer lightweight interactions so the user can change parameters and immediately see a graph update.

## User Experience
The application should expose two learning views on the frontend:

### Laplace View
- Title and introduction
- Governing equation
- Variable table
- Why Laplace transforms help
- Interpretation of the physical response
- Real-world use cases
- Assignment relevance
- Interactive simulation controls
- Displacement chart with forcing comparison

### Fourier View
- Title and introduction
- Fourier-series equation
- Signal-decomposition explanation
- Compression steps
- Interpretation of the approximation
- Real-world use cases
- Assignment relevance
- Interactive term selector
- Original-signal vs approximation chart

---

## Backend Scope

### Endpoint 1
`GET /api/applications/laplace`

#### Response
```json
{
  "title": "Spring-Mass-Damper System",
  "description": "A spring-mass-damper model describes mechanical vibration.",
  "learning_objective": "Connect a second-order differential equation to a physical system.",
  "equation": "m y'' + c y' + k y = F(t)",
  "variables": [
    {"symbol": "m", "meaning": "mass"},
    {"symbol": "c", "meaning": "damping coefficient"},
    {"symbol": "k", "meaning": "spring constant"},
    {"symbol": "F(t)", "meaning": "external force"},
    {"symbol": "y(t)", "meaning": "displacement"}
  ],
  "why_laplace": "Transforms the differential equation into an algebraic form.",
  "interpretation": "Explains how damping and stiffness affect oscillation.",
  "limitations": [
    "Uses a simplified single-degree-of-freedom model."
  ],
  "use_cases": [
    "car suspension",
    "shock absorbers",
    "building vibration",
    "mechanical damping"
  ],
  "assignment_link": "The assignment differential equation behaves like forced vibration."
}
```

### Endpoint 2
`GET /api/applications/laplace/simulate`

#### Query Parameters
- `m` default `1.0`, must be `> 0`
- `c` default `0.45`, must be `>= 0`
- `k` default `4.0`, must be `> 0`
- `force_amplitude` default `1.0`, must be `>= 0`
- `time_end` default `12.0`, must be `> 0`
- `num_points` default `300`, must be between `50` and `2000`

#### Response
```json
{
  "t": [0.0, 0.04, 0.08],
  "displacement": [0.0, 0.0005, 0.0021],
  "velocity": [0.0, 0.031, 0.061],
  "forcing": [0.0, 0.0679, 0.1354],
  "error_analysis": {
    "solver_success": true,
    "relative_tolerance": 0.000001,
    "absolute_tolerance": 0.00000001,
    "max_ode_residual": 0.00298,
    "mean_ode_residual": 0.00116,
    "residual_note": "Residual is estimated from sampled output."
  },
  "parameters": {
    "m": 1.0,
    "c": 0.45,
    "k": 4.0,
    "force_amplitude": 1.0,
    "time_end": 12.0,
    "num_points": 300
  }
}
```

## Project Structure

```text
app/
  main.py
  routes/
    applications.py
  services/
    applications_service.py
  schemas/
    applications.py
  static/
    index.html
    styles.css
    app.js

tests/
  test_applications.py

docs/
  real_world_applications_plan.md
```

---

### Endpoint 3
`GET /api/applications/fourier`

#### Response
```json
{
  "title": "Audio Compression",
  "description": "Fourier analysis represents sound as a combination of frequencies.",
  "learning_objective": "Explain how Fourier series decompose signals into reusable frequency parts.",
  "series_equation": "f(t) = a0 + sum(an cos(nt) + bn sin(nt))",
  "concept": "signal decomposition",
  "steps": [
    "break sound into frequencies",
    "measure dominant components",
    "remove low-impact components",
    "reconstruct the signal"
  ],
  "interpretation": "Higher-energy components are kept while smaller ones can be discarded.",
  "limitations": [
    "Real codecs use additional psychoacoustic techniques."
  ],
  "use_cases": [
    "MP3 compression",
    "music streaming",
    "voice transmission",
    "speech recognition"
  ],
  "assignment_link": "The Fourier series of f(x) = x demonstrates signal reconstruction."
}
```

### Endpoint 4
`GET /api/applications/fourier/signal`

#### Query Parameters
- `terms` default `10`, must be between `1` and `100`
- `num_points` default `600`, must be between `100` and `4000`

#### Response
```json
{
  "x": [-3.14, -3.13, -3.12],
  "signal": [-3.14, -3.13, -3.12],
  "approximation": [-0.02, -0.08, -0.14],
  "absolute_error": [3.12, 3.05, 2.98],
  "terms_used": 10,
  "coefficients": {
    "a0": 0.0,
    "an_note": "an = 0 for all n because f(x)=x is odd.",
    "bn_formula": "bn = 2*(-1)^(n+1)/n",
    "terms": [
      {"n": 1, "an": 0.0, "bn": 2.0, "term": "2.0 sin(1x)"},
      {"n": 2, "an": 0.0, "bn": -1.0, "term": "-1.0 sin(2x)"}
    ]
  },
  "error_analysis": {
    "mean_absolute_error": 0.1184,
    "root_mean_square_error": 0.2472,
    "max_absolute_error": 3.1416,
    "error_note": "Truncation error from using finite Fourier terms."
  }
}
```

---

## Legacy Sketch (Superseded)

```
app/
 ├── routes/
 │   └── applications.py
 │
 ├── services/
 │   └── applications_service.py
 │
 └── schemas/
     └── applications.py
```

---

## Route Outline

```python
router = APIRouter(prefix="/api/applications", tags=["applications"])

@router.get("/laplace")
def laplace_application()

@router.get("/laplace/simulate")
def laplace_simulation()

@router.get("/fourier")
def fourier_application()

@router.get("/fourier/signal")
def fourier_signal()
```

## Service Responsibilities

### `applications_service.py`
- `laplace_application()` returns explanation text, equation, variable definitions, interpretation, limitations, use cases, and assignment relevance.
- `laplace_simulation()` computes a damped oscillator response and returns equal-length chart arrays.
- `fourier_application()` returns audio-compression explanation content and learning steps.
- `fourier_signal()` generates a Fourier approximation and returns chart-ready comparison data.

## Mathematical Logic

### Laplace Application
Model the system as:

`m y'' + c y' + k y = F(t)`

Implementation notes:
- Solve the time-domain system numerically with `scipy.integrate.solve_ivp`.
- Use a smooth sinusoidal forcing term for a clean classroom demonstration.
- Return arrays that are equal in length and directly plottable on the frontend.

### Fourier Application
Use a truncated Fourier series for `f(x) = x` on `[-pi, pi]`.

Implementation notes:
- Generate the original signal and the approximation using the requested number of terms.
- Show how the approximation improves as `terms` increases.
- Keep the output chart-ready and deterministic.

## Frontend Scope

### Rendering Requirements
- Serve a responsive interface that works on mobile and desktop.
- Keep the Laplace and Fourier sections visible as dedicated views or panels.
- Present equations in a readable highlighted block.
- Render variable and step data from API responses, not hardcoded duplicates.

### Interaction Requirements
- Laplace section should let the user change `m`, `c`, `k`, and `force_amplitude`.
- Fourier section should let the user change the number of retained terms.
- The frontend should fetch new chart data after a valid form submission.
- The frontend should display error analysis next to each graph.
- The frontend should display visible Fourier coefficient values for the requested approximation.
- The frontend should plot Fourier coefficient values `an` and `bn` against the term index `n`.
- The frontend should display an axis guide explaining what the x-axis, y-axis, and sampled point index mean for each graph.
- The frontend should include a visible color legend inside each rendered SVG so downloaded graph images identify each curve without extra context.

### State Requirements
- Show a loading message while content or charts are being requested.
- Show recoverable inline errors if simulation or signal calls fail.
- Keep explanatory text on screen even if a visualization request fails.

### Accessibility Requirements
- Use semantic headings, labels, and button text.
- Keep keyboard focus visible.
- Ensure controls have a minimum touch target size of `44px`.
- Provide text labels for charts and explanatory fallback text.

## Validation And Error Handling
- Invalid query parameters should produce standard FastAPI `422` validation errors.
- Numeric endpoints must always return same-length arrays.
- Content endpoints should remain available even if a chart endpoint fails.

## Testing Requirements
- Root frontend route should render the application shell.
- Content endpoints should return `200` with all required fields.
- Numeric endpoints should return nonempty numeric arrays.
- Invalid parameters should return `422`.
- Fourier signal responses should echo the active term count.

## Deliverables
- FastAPI application with four API endpoints
- Static frontend served from the same project
- Updated PRD
- Plan file in `docs/real_world_applications_plan.md`
- Automated tests covering the main contract
