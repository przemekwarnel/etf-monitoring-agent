from schemas.internal import ETFSnapshot, ComparableETF


def find_comparable_etfs(snapshot: ETFSnapshot) -> list[ComparableETF]:
    """
    Return a temporary list of comparable ETFs for development and pipeline testing.
    """

    comparable_etfs = [
        ComparableETF(
            ticker="SPY",
            fund_name="SPDR S&P 500 ETF Trust",
            expense_ratio=0.009,
            aum=400e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="IVV",
            fund_name="iShares Core S&P 500 ETF",
            expense_ratio=0.003,
            aum=300e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="VOO",
            fund_name="Vanguard S&P 500 ETF",
            expense_ratio=0.003,
            aum=200e9,
            currency="USD",
            replication_method="physical",
        ),
    ]   

    return comparable_etfs