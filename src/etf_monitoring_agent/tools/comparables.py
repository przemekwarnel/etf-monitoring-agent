from etf_monitoring_agent.schemas.internal import ComparableETF, ETFSnapshot


ETF_EXPOSURE_MAP = {
    "SPY": "sp500",
    "IVV": "sp500",
    "VOO": "sp500",
    "VWCE": "global_equity",
    "IWDA": "global_equity",
    "SWDA": "global_equity",
    "EEM": "emerging_markets",
    "IEMG": "emerging_markets",
    "VWO": "emerging_markets",
    "ARKK": "innovation_growth",
    "QQQM": "innovation_growth",
}


COMPARABLES_BY_EXPOSURE = {
    "sp500": [
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
    ],
    "global_equity": [
        ComparableETF(
            ticker="VWCE",
            fund_name="Vanguard FTSE All-World UCITS ETF",
            expense_ratio=0.0022,
            aum=25e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="IWDA",
            fund_name="iShares Core MSCI World UCITS ETF",
            expense_ratio=0.0020,
            aum=70e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="SWDA",
            fund_name="iShares Core MSCI World UCITS ETF USD (Acc)",
            expense_ratio=0.0020,
            aum=65e9,
            currency="USD",
            replication_method="physical",
        ),
    ],
    "emerging_markets": [
        ComparableETF(
            ticker="EEM",
            fund_name="iShares MSCI Emerging Markets ETF",
            expense_ratio=0.0069,
            aum=25e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="IEMG",
            fund_name="iShares Core MSCI Emerging Markets ETF",
            expense_ratio=0.0009,
            aum=80e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="VWO",
            fund_name="Vanguard FTSE Emerging Markets ETF",
            expense_ratio=0.0008,
            aum=75e9,
            currency="USD",
            replication_method="physical",
        ),
    ],
    "innovation_growth": [
        ComparableETF(
            ticker="ARKK",
            fund_name="ARK Innovation ETF",
            expense_ratio=0.0075,
            aum=7e9,
            currency="USD",
            replication_method="physical",
        ),
        ComparableETF(
            ticker="QQQM",
            fund_name="Invesco NASDAQ 100 ETF",
            expense_ratio=0.0015,
            aum=30e9,
            currency="USD",
            replication_method="physical",
        ),
    ],
}


def normalize_base_ticker(ticker: str) -> str:
    """Normalize a ticker by removing exchange suffixes and converting it to uppercase."""
    return ticker.split(".")[0].upper()


def get_exposure_group(ticker: str) -> str:
    """Return the exposure group used to select comparable ETFs for a given ticker."""
    return ETF_EXPOSURE_MAP.get(ticker, "unknown")


def find_comparable_etfs(snapshot: ETFSnapshot) -> list[ComparableETF]:
    """Return comparable ETFs from the same exposure group as the input ETF."""

    base_ticker = normalize_base_ticker(snapshot.ticker)
    exposure_group = get_exposure_group(base_ticker)

    if exposure_group == "unknown":
        return []

    comparable_etfs = COMPARABLES_BY_EXPOSURE.get(exposure_group, [])

    return [etf for etf in comparable_etfs if etf.ticker != base_ticker]