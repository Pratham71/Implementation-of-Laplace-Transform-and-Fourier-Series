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


class LaplaceSimulationResponse(BaseModel):
    t: list[float] = Field(description="Time axis values.")
    displacement: list[float] = Field(description="Simulated displacement values.")
    velocity: list[float] = Field(description="Simulated velocity values.")
    forcing: list[float] = Field(description="Driving force values.")
    parameters: dict[str, float] = Field(description="Parameters used in the run.")


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


class FourierSignalResponse(BaseModel):
    x: list[float] = Field(description="Sample positions in radians.")
    signal: list[float] = Field(description="Reference waveform samples.")
    approximation: list[float] = Field(description="Fourier approximation samples.")
    terms_used: int = Field(description="The number of Fourier terms used.")
