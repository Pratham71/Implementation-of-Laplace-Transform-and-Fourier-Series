from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp

from app.schemas.applications import (
    FourierCoefficientTerm,
    FourierCoefficients,
    FourierErrorAnalysis,
    FourierApplicationResponse,
    FourierSignalResponse,
    LaplaceErrorAnalysis,
    LaplaceApplicationResponse,
    LaplaceSimulationResponse,
    VariableDefinition,
)


SOLVER_RTOL = 1e-6
SOLVER_ATOL = 1e-8


def get_laplace_application() -> LaplaceApplicationResponse:
    return LaplaceApplicationResponse(
        title="Spring-Mass-Damper System",
        description=(
            "A spring-mass-damper model describes how a mass moves when attached "
            "to a spring and a damper while an external force acts on it."
        ),
        learning_objective=(
            "Connect a second-order differential equation to a physical vibration "
            "system and explain why Laplace transforms help solve forced motion."
        ),
        equation="m y'' + c y' + k y = F(t)",
        variables=[
            VariableDefinition(symbol="m", meaning="mass"),
            VariableDefinition(symbol="c", meaning="damping coefficient"),
            VariableDefinition(symbol="k", meaning="spring constant"),
            VariableDefinition(symbol="F(t)", meaning="external force"),
            VariableDefinition(symbol="y(t)", meaning="displacement"),
        ],
        why_laplace=(
            "Laplace transforms convert the differential equation into an algebraic "
            "expression in the transform domain, which makes initial conditions "
            "and forcing functions easier to handle."
        ),
        interpretation=(
            "The simulation shows how inertia, damping, and stiffness interact. "
            "Higher damping reduces oscillation faster, while larger stiffness "
            "pulls the mass back toward equilibrium more strongly."
        ),
        limitations=[
            "The example uses a single-degree-of-freedom model rather than a full mechanical system.",
            "The forcing term is idealized as a smooth sinusoidal input for teaching purposes.",
        ],
        use_cases=[
            "car suspension",
            "shock absorbers",
            "building vibration",
            "mechanical damping",
        ],
        assignment_link=(
            "The given differential equation behaves like a forced vibration model, "
            "which makes the Laplace transform interpretation concrete."
        ),
    )


def simulate_laplace(
    *,
    m: float,
    c: float,
    k: float,
    force_amplitude: float,
    time_end: float,
    num_points: int,
) -> LaplaceSimulationResponse:
    time = np.linspace(0.0, time_end, num_points)
    natural_frequency = math.sqrt(k / m)
    driving_frequency = 0.85 * natural_frequency

    def forcing_term(t: float | np.ndarray) -> float | np.ndarray:
        return force_amplitude * np.sin(driving_frequency * t)

    def dynamics(t: float, state: np.ndarray) -> list[float]:
        displacement, velocity = state
        acceleration = (forcing_term(t) - c * velocity - k * displacement) / m
        return [velocity, acceleration]

    solution = solve_ivp(
        dynamics,
        (0.0, time_end),
        y0=[0.0, 0.0],
        t_eval=time,
        rtol=SOLVER_RTOL,
        atol=SOLVER_ATOL,
    )

    displacement = solution.y[0]
    velocity = solution.y[1]
    forcing = forcing_term(time)
    estimated_acceleration = np.gradient(velocity, time, edge_order=2)
    residual = m * estimated_acceleration + c * velocity + k * displacement - forcing
    absolute_residual = np.abs(residual)

    return LaplaceSimulationResponse(
        t=np.round(time, 6).tolist(),
        displacement=np.round(displacement, 6).tolist(),
        velocity=np.round(velocity, 6).tolist(),
        forcing=np.round(forcing, 6).tolist(),
        parameters={
            "m": float(m),
            "c": float(c),
            "k": float(k),
            "force_amplitude": float(force_amplitude),
            "time_end": float(time_end),
            "num_points": float(num_points),
        },
        error_analysis=LaplaceErrorAnalysis(
            solver_success=bool(solution.success),
            relative_tolerance=SOLVER_RTOL,
            absolute_tolerance=SOLVER_ATOL,
            max_ode_residual=round(float(np.max(absolute_residual)), 8),
            mean_ode_residual=round(float(np.mean(absolute_residual)), 8),
            residual_note=(
                "Residual is estimated from the sampled velocity curve, so it measures "
                "plot-resolution/numerical consistency rather than an exact symbolic error."
            ),
        ),
    )


def get_fourier_application() -> FourierApplicationResponse:
    return FourierApplicationResponse(
        title="Audio Compression",
        description=(
            "Fourier analysis explains how a complex sound can be represented as a "
            "combination of simpler frequency components."
        ),
        learning_objective=(
            "Explain how Fourier series decompose a signal into frequencies and why "
            "keeping only dominant components supports compression."
        ),
        series_equation="f(t) = a0 + sum(an cos(nt) + bn sin(nt))",
        concept="signal decomposition",
        steps=[
            "break sound into frequencies",
            "measure which components carry most of the energy",
            "remove low-impact components",
            "reconstruct the signal from dominant frequencies",
        ],
        interpretation=(
            "A truncated Fourier series keeps the strongest frequency content while "
            "ignoring detail that contributes less to perceived sound quality."
        ),
        limitations=[
            "Real audio codecs use transforms, psychoacoustics, and framing beyond a simple Fourier series demo.",
            "The plotted waveform is a teaching signal rather than recorded audio data.",
        ],
        use_cases=[
            "MP3 compression",
            "music streaming",
            "voice transmission",
            "speech recognition",
        ],
        assignment_link=(
            "The Fourier series of f(x) = x shows how a complicated waveform can be "
            "rebuilt from sinusoidal pieces."
        ),
    )


def generate_fourier_signal(*, terms: int, num_points: int) -> FourierSignalResponse:
    x = np.linspace(-math.pi, math.pi, num_points)
    signal = x
    approximation = np.zeros_like(x)

    for n in range(1, terms + 1):
        approximation += 2.0 * ((-1) ** (n + 1)) * np.sin(n * x) / n

    absolute_error = np.abs(signal - approximation)
    visible_coefficient_count = min(terms, 10)
    coefficient_terms = [
        FourierCoefficientTerm(
            n=n,
            an=0.0,
            bn=round(float(2.0 * ((-1) ** (n + 1)) / n), 6),
            term=f"{round(float(2.0 * ((-1) ** (n + 1)) / n), 6)} sin({n}x)",
        )
        for n in range(1, visible_coefficient_count + 1)
    ]

    return FourierSignalResponse(
        x=np.round(x, 6).tolist(),
        signal=np.round(signal, 6).tolist(),
        approximation=np.round(approximation, 6).tolist(),
        absolute_error=np.round(absolute_error, 6).tolist(),
        terms_used=terms,
        error_analysis=FourierErrorAnalysis(
            mean_absolute_error=round(float(np.mean(absolute_error)), 8),
            root_mean_square_error=round(float(np.sqrt(np.mean(absolute_error**2))), 8),
            max_absolute_error=round(float(np.max(absolute_error)), 8),
            error_note=(
                "This is truncation error from using a finite number of Fourier terms. "
                "Mean error usually decreases as more terms are retained."
            ),
        ),
        coefficients=FourierCoefficients(
            a0=0.0,
            an_note="an = 0 for all n because f(x)=x is odd.",
            bn_formula="bn = 2*(-1)^(n+1)/n",
            terms=coefficient_terms,
        ),
    )
