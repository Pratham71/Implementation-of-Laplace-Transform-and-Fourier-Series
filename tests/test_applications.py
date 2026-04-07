from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page_serves_real_world_applications_experience() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Implementation of Laplace Transform and Fourier Series" in response.text
    assert "Spring-Mass-Damper System" in response.text
    assert "Audio Compression" in response.text
    assert "Pratham Nagpal" in response.text
    assert "Download Laplace Graph" in response.text
    assert "Download Fourier Graph" in response.text
    assert "Error Analysis" in response.text
    assert "Numerical Error Analysis" in response.text
    assert "Approximation Error Analysis" in response.text
    assert "Residual = m*y'' + c*y' + k*y - F(t)" in response.text
    assert "Absolute Error = |signal - approximation|" in response.text
    assert "RMSE = sqrt(mean(error^2))" in response.text
    assert "Fourier Coefficients" in response.text
    assert "Fourier Coefficient Plot" in response.text
    assert "Download Fourier Coefficients Graph" in response.text
    assert "a0 = 0" in response.text
    assert "Axis Guide" in response.text
    assert "Laplace x-axis: time t in seconds" in response.text
    assert "Fourier x-axis: x values in radians" in response.text
    assert "/static/app.js?v=coefficient-plot" in response.text
    assert response.headers["cache-control"] == "no-store"


def test_chart_renderer_includes_downloadable_wave_legends() -> None:
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "Displacement y(t)" in response.text
    assert "Applied force F(t)" in response.text
    assert "Original signal f(x)=x" in response.text
    assert "Fourier approximation" in response.text


def test_frontend_renders_fourier_coefficient_chart() -> None:
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "renderCoefficientChart" in response.text
    assert "fourier-coefficient-chart" in response.text
    assert "Cosine coefficient a_n" in response.text
    assert "Sine coefficient b_n" in response.text


def test_laplace_application_returns_learning_content() -> None:
    response = client.get("/api/applications/laplace")

    assert response.status_code == 200
    payload = response.json()

    assert payload["title"] == "Spring-Mass-Damper System"
    assert payload["learning_objective"]
    assert payload["equation"] == "m y'' + c y' + k y = F(t)"
    assert len(payload["variables"]) == 5
    assert "car suspension" in payload["use_cases"]


def test_laplace_simulation_returns_chart_ready_series() -> None:
    response = client.get("/api/applications/laplace/simulate")

    assert response.status_code == 200
    payload = response.json()

    assert len(payload["t"]) == len(payload["displacement"])
    assert len(payload["t"]) == len(payload["forcing"])
    assert len(payload["t"]) == 300
    assert payload["t"][0] == 0.0
    assert payload["t"][-1] == 12.0
    assert payload["error_analysis"]["solver_success"] is True
    assert payload["error_analysis"]["max_ode_residual"] >= 0
    assert payload["error_analysis"]["mean_ode_residual"] >= 0
    assert payload["error_analysis"]["relative_tolerance"] == 1e-6


def test_laplace_simulation_rejects_non_positive_mass() -> None:
    response = client.get("/api/applications/laplace/simulate?m=0")

    assert response.status_code == 422


def test_fourier_application_returns_learning_content() -> None:
    response = client.get("/api/applications/fourier")

    assert response.status_code == 200
    payload = response.json()

    assert payload["title"] == "Audio Compression"
    assert payload["concept"] == "signal decomposition"
    assert payload["learning_objective"]
    assert "music streaming" in payload["use_cases"]
    assert payload["series_equation"] == "f(t) = a0 + sum(an cos(nt) + bn sin(nt))"


def test_fourier_signal_returns_original_and_approximation() -> None:
    response = client.get("/api/applications/fourier/signal?terms=12")

    assert response.status_code == 200
    payload = response.json()

    assert len(payload["x"]) == len(payload["signal"])
    assert len(payload["x"]) == len(payload["approximation"])
    assert len(payload["x"]) == len(payload["absolute_error"])
    assert payload["terms_used"] == 12
    assert payload["error_analysis"]["mean_absolute_error"] > 0
    assert payload["error_analysis"]["root_mean_square_error"] > 0
    assert payload["error_analysis"]["max_absolute_error"] > 0
    assert payload["coefficients"]["a0"] == 0.0
    assert payload["coefficients"]["an_note"] == "an = 0 for all n because f(x)=x is odd."
    assert payload["coefficients"]["terms"][0]["n"] == 1
    assert payload["coefficients"]["terms"][0]["an"] == 0.0
    assert payload["coefficients"]["terms"][0]["bn"] == 2.0
    assert payload["coefficients"]["terms"][1]["bn"] == -1.0


def test_fourier_coefficients_follow_selected_term_count() -> None:
    response = client.get("/api/applications/fourier/signal?terms=20")

    assert response.status_code == 200
    coefficient_terms = response.json()["coefficients"]["terms"]

    assert len(coefficient_terms) == 20
    assert coefficient_terms[-1]["n"] == 20
    assert coefficient_terms[-1]["bn"] == -0.1


def test_fourier_error_decreases_when_more_terms_are_used() -> None:
    low_terms = client.get("/api/applications/fourier/signal?terms=5").json()
    high_terms = client.get("/api/applications/fourier/signal?terms=20").json()

    assert (
        high_terms["error_analysis"]["mean_absolute_error"]
        < low_terms["error_analysis"]["mean_absolute_error"]
    )


def test_fourier_signal_rejects_too_few_terms() -> None:
    response = client.get("/api/applications/fourier/signal?terms=0")

    assert response.status_code == 422
