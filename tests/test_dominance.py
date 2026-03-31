from schemas.internal import ETFSnapshot, ComparableETF
from agent.nodes.dominance import find_dominant_etf


def test_find_dominant_etf_returns_better_candidate():
    current = ETFSnapshot(
        ticker="TEST",
        expense_ratio=0.01,
        aum=100_000_000,
    )

    comparables = [
        ComparableETF(ticker="COMP1", expense_ratio=0.009, aum=60_000_000),
        ComparableETF(ticker="COMP2", expense_ratio=0.011, aum=80_000_000),
        ComparableETF(ticker="COMP3", expense_ratio=0.008, aum=40_000_000),  # Too small
    ]

    dominant = find_dominant_etf(current, comparables)

    assert dominant is not None
    assert dominant.ticker == "COMP1"


def test_find_dominant_etf_returns_none_if_no_better_candidate():
    current = ETFSnapshot(
        ticker="TEST",
        expense_ratio=0.01,
        aum=100_000_000,
    )

    comparables = [
        ComparableETF(ticker="COMP1", expense_ratio=0.011, aum=60_000_000),
        ComparableETF(ticker="COMP2", expense_ratio=0.012, aum=80_000_000),
    ]

    dominant = find_dominant_etf(current, comparables)

    assert dominant is None


def test_find_dominant_etf_selects_lowest_cost_candidate():
    current = ETFSnapshot(
        ticker="TEST",
        expense_ratio=0.01,
        aum=100_000_000,
    )

    comparables = [
        ComparableETF(ticker="COMP1", expense_ratio=0.009, aum=60_000_000),
        ComparableETF(ticker="COMP2", expense_ratio=0.007, aum=60_000_000),
    ]

    dominant = find_dominant_etf(current, comparables)

    assert dominant is not None
    assert dominant.ticker == "COMP2"