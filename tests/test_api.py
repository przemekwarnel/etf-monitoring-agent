from fastapi.testclient import TestClient

import api.main
from schemas.output import ETFAnalysisOutput


client = TestClient(api.main.app)


def build_mock_analysis_output() -> ETFAnalysisOutput:
    """Create a representative ETF analysis response for API tests."""
    return ETFAnalysisOutput(
        ticker="VWCE",
        status="stable",
        detected_changes=[],
        risk_flags=[],
        dominant_etf=None,
    )


def test_root_returns_service_metadata():
    response = client.get("/")

    assert response.status_code == 200

    payload = response.json()
    assert payload["service"] == "ETF Monitoring & Analysis Agent"
    assert payload["version"] == "0.1.0"
    assert payload["docs_url"] == "/docs"


def test_health_returns_ok_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_structured_output(monkeypatch):
    mock_output = build_mock_analysis_output()
    captured_state = {}

    class FakeGraph:
        def invoke(self, state: dict) -> dict:
            captured_state["state"] = state
            return {"final_output": mock_output}

    monkeypatch.setattr(api.main, "graph", FakeGraph())

    response = client.get("/analyze", params={"ticker": "vwce"})

    assert response.status_code == 200

    payload = response.json()
    assert payload["ticker"] == "VWCE"
    assert payload["status"] == "stable"
    assert payload["detected_changes"] == []
    assert payload["risk_flags"] == []
    assert payload["dominant_etf"] is None

    assert captured_state["state"] == {"ticker": "VWCE"}