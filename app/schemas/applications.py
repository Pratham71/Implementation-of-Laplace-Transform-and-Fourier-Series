from __future__ import annotations

from pydantic import BaseModel, Field


class VariableDefinition(BaseModel):
    symbol: str
    meaning: str


class LaplaceApplicationResponse(BaseModel):
    title: str
    description: str
    learning_objective: str
    equation: str
    variables: list[VariableDefinition]
    why_laplace: str
    interpretation: str
    limitations: list[str]
    use_cases: list[str]
    assignment_link: str


class LaplaceErrorAnalysis(BaseModel):
    solver_success: bool = Field(description="Whether the numerical ODE solver succeeded.")
    relative_tolerance: float = Field(description="Relative tolerance used by solve_ivp.")
    absolute_tolerance: float = Field(description="Absolute tolerance used by solve_ivp.")
    max_ode_residual: float = Field(description="Maximum absolute ODE residual from sampled output.")
    mean_ode_residual: float = Field(description="Mean absolute ODE residual from sampled output.")
    residual_note: str = Field(description="Short explanation of what the residual means.")


class LaplaceDampingClassification(BaseModel):
    damping_type: str = Field(description="Underdamped, critically damped, or overdamped label.")
    damping_ratio: float = Field(description="Damping ratio zeta = c / (2*sqrt(m*k)).")
    critical_damping: float = Field(description="Critical damping coefficient c_c = 2*sqrt(m*k).")
    formula: str = Field(description="Formula used to classify the damping behavior.")
    explanation: str = Field(description="Plain-language meaning of the damping type.")


class LaplaceSimulationResponse(BaseModel):
    t: list[float] = Field(description="Time axis values.")
    displacement: list[float] = Field(description="Simulated displacement values.")
    velocity: list[float] = Field(description="Simulated velocity values.")
    forcing: list[float] = Field(description="Driving force values.")
    parameters: dict[str, float] = Field(description="Parameters used in the run.")
    error_analysis: LaplaceErrorAnalysis = Field(description="Numerical solver error analysis.")
    damping_classification: LaplaceDampingClassification = Field(
        description="Damping regime classification for the selected m, c, and k values."
    )


class FourierApplicationResponse(BaseModel):
    title: str
    description: str
    learning_objective: str
    series_equation: str
    concept: str
    steps: list[str]
    interpretation: str
    limitations: list[str]
    use_cases: list[str]
    assignment_link: str


class FourierErrorAnalysis(BaseModel):
    mean_absolute_error: float = Field(description="Average absolute difference from the reference signal.")
    root_mean_square_error: float = Field(description="RMS approximation error.")
    max_absolute_error: float = Field(description="Largest pointwise absolute approximation error.")
    error_note: str = Field(description="Short explanation of the Fourier truncation error.")


class FourierCoefficientTerm(BaseModel):
    n: int = Field(description="Harmonic term number.")
    an: float = Field(description="Cosine coefficient.")
    bn: float = Field(description="Sine coefficient.")
    term: str = Field(description="Readable sine term used in the approximation.")


class FourierCoefficients(BaseModel):
    a0: float = Field(description="Constant Fourier coefficient.")
    an_note: str = Field(description="Explanation for cosine coefficients.")
    bn_formula: str = Field(description="Formula used for sine coefficients.")
    terms: list[FourierCoefficientTerm] = Field(
        description="Coefficient rows for each retained Fourier term."
    )


class FourierSignalResponse(BaseModel):
    x: list[float] = Field(description="Sample positions in radians.")
    signal: list[float] = Field(description="Reference waveform samples.")
    approximation: list[float] = Field(description="Fourier approximation samples.")
    absolute_error: list[float] = Field(description="Pointwise absolute approximation error.")
    terms_used: int = Field(description="The number of Fourier terms used.")
    error_analysis: FourierErrorAnalysis = Field(description="Fourier approximation error analysis.")
    coefficients: FourierCoefficients = Field(
        description="Fourier coefficient values for each retained term."
    )
