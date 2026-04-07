# Implementation of Laplace Transform and Fourier Series

Mathematics III assignment project by Pratham Nagpal.

## Student Details
- Name: Pratham Nagpal
- ID: 2024A7PS0071U
- Section: L4
- Instructor: Dr. Soma Sundaram

## Project Overview
This project implements two Mathematics III applications:

1. Laplace Transform -> Spring-Mass-Damper System
2. Fourier Series -> Signal Representation for Audio Compression

The project includes:
- a FastAPI backend
- a browser-based frontend served from the same app
- interactive graph generation
- graph download buttons for report use
- Markdown documentation and a final PDF report

## Features
- `GET /api/applications/laplace`
  - Returns the learning content for the spring-mass-damper model.
- `GET /api/applications/laplace/simulate`
  - Generates time-domain data for displacement, velocity, forcing, and ODE residual error analysis.
- `GET /api/applications/fourier`
  - Returns the learning content for Fourier-series-based signal decomposition.
- `GET /api/applications/fourier/signal`
  - Generates original signal, approximation, pointwise absolute error, and summary error metrics.
- Frontend at `/`
  - Shows both applications in one page.
  - Supports parameter input for simulation.
  - Shows error analysis for both graphs.
  - Lets you download the rendered graphs as PNG files.
- Report generator
  - Produces the final assignment PDF in `docs/2024A7PS0071U.pdf`.

## Tech Stack
- Python 3.12
- FastAPI
- NumPy
- SciPy
- ReportLab
- Vanilla HTML, CSS, and JavaScript

## Project Structure
```text
app/
  main.py
  routes/
  schemas/
  services/
  static/

docs/
  2024A7PS0071U.pdf
  final_assignment_report.md
  guidlines.txt
  manual_solution_report.md
  real_world_applications_plan.md
  real_world_applications_prd.md

tests/
  test_applications.py

tools/
  generate_assignment_report_pdf.py

requirements.txt
README.md
```

## Setup
Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run The Application
Start the FastAPI development server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open:
- `http://127.0.0.1:8000/` for the frontend
- `http://127.0.0.1:8000/docs` for the API docs

## Tests
Run the automated test suite with:

```powershell
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider tests/test_applications.py
```

## Regenerate The Final PDF
If you update the final report source or the generated output logic, rebuild the PDF with:

```powershell
.\.venv\Scripts\python.exe tools\generate_assignment_report_pdf.py
```

The generated file is:
- `docs/2024A7PS0071U.pdf`

## Included Documentation
- `docs/real_world_applications_prd.md`
  - Expanded project requirements document.
- `docs/real_world_applications_plan.md`
  - Implementation plan for the project.
- `docs/manual_solution_report.md`
  - Manual derivation notes for both selected topics.
- `docs/final_assignment_report.md`
  - Polished final report source.
- `docs/2024A7PS0071U.pdf`
  - Submission-ready PDF report.
- `docs/guidlines.txt`
  - Assignment instructions provided for the report structure.

## Notes
- This project runs through Python and FastAPI. There is no `npm run dev` workflow in this repository.
- The graph download buttons are intended to help capture report-ready visuals directly from the frontend.
- The final PDF already includes derived explanation, results, code excerpts, and generated graphs.
