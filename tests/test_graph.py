from agent.graph import build_graph
from schemas.internal import ETFSnapshot


def test_graph_runs_end_to_end_with_mocked_snapshot(monkeypatch):
    graph = build_graph()

    mock_snapshot = ETFSnapshot(
        ticker="MOCK",
        expense_ratio=0.01,
        aum=1_000_000,
    )

    def mock_fetch(ticker: str) -> ETFSnapshot:
        return mock_snapshot
    
    monkeypatch.setattr(
        "agent.nodes.fetch.fetch_etf_snapshot",
        mock_fetch
    )

    result = graph.invoke({"ticker": "MOCK"})

    assert result["current_snapshot"].ticker == "MOCK"
    assert "previous_snapshot" in result
    assert "detected_changes" in result
    assert len(result["detected_changes"]) >= 1
    