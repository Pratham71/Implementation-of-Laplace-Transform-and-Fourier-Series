from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.applications import (
    FourierApplicationResponse,
    FourierSignalResponse,
    LaplaceApplicationResponse,
    LaplaceSimulationResponse,
)
from app.services import applications_service


router = APIRouter(prefix="/api/applications", tags=["applications"])


@router.get("/laplace", response_model=LaplaceApplicationResponse)
def laplace_application() -> LaplaceApplicationResponse:
    return applications_service.get_laplace_application()


@router.get("/laplace/simulate", response_model=LaplaceSimulationResponse)
def laplace_simulation(
    m: Annotated[float, Query(gt=0, description="Mass in kilograms.")] = 1.0,
    c: Annotated[float, Query(ge=0, description="Damping coefficient.")] = 0.45,
    k: Annotated[float, Query(gt=0, description="Spring constant.")] = 4.0,
    force_amplitude: Annotated[
        float, Query(ge=0, description="Driving force amplitude.")
    ] = 1.0,
    time_end: Annotated[
        float, Query(gt=0, le=60, description="Simulation horizon in seconds.")
    ] = 12.0,
    num_points: Annotated[
        int, Query(ge=50, le=2000, description="Number of samples.")
    ] = 300,
) -> LaplaceSimulationResponse:
    return applications_service.simulate_laplace(
        m=m,
        c=c,
        k=k,
        force_amplitude=force_amplitude,
        time_end=time_end,
        num_points=num_points,
    )


@router.get("/fourier", response_model=FourierApplicationResponse)
def fourier_application() -> FourierApplicationResponse:
    return applications_service.get_fourier_application()


@router.get("/fourier/signal", response_model=FourierSignalResponse)
def fourier_signal(
    terms: Annotated[
        int, Query(ge=1, le=100, description="Number of Fourier terms.")
    ] = 10,
    num_points: Annotated[
        int, Query(ge=100, le=4000, description="Number of chart samples.")
    ] = 600,
) -> FourierSignalResponse:
    return applications_service.generate_fourier_signal(
        terms=terms,
        num_points=num_points,
    )
