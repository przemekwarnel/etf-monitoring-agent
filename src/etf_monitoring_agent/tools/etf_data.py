import yfinance as yf

from etf_monitoring_agent.schemas.internal import ETFSnapshot


ETF_SUFFIX_CANDIDATES = ["", ".DE", ".F", ".AS", ".DU"]

EXPENSE_RATIO_FALLBACK = {
    "SPY": 0.009,
    "IVV": 0.003,
    "VOO": 0.003,
    "VWCE": 0.0022,
    "EEM": 0.0069,
    "ARKK": 0.0075,
}


def _extract_info(symbol: str) -> dict:
    ticker_obj = yf.Ticker(symbol)
    info = ticker_obj.info or {}

    if not info or (
        info.get("regularMarketPrice") is None
        and info.get("longName") is None
        and info.get("shortName") is None
    ):
        return {}

    return info


def is_valid_etf_info(info: dict) -> bool:
    """Determine if the provided info dictionary contains valid ETF data."""

    has_name = info.get("longName") or info.get("shortName")

    has_core_data = any([
        info.get("totalAssets") is not None,
        info.get("expenseRatio") is not None,
        info.get("currency") is not None,
    ])

    return bool(has_name and has_core_data)


def get_expense_ratio(ticker: str) -> float | None:
    """
    Retrieve the expense ratio for a given ticker, using fallback values if necessary.
    """

    info = _extract_info(ticker)

    if is_valid_etf_info(info):
        return info.get("expenseRatio") or EXPENSE_RATIO_FALLBACK.get(ticker)
    
    return EXPENSE_RATIO_FALLBACK.get(ticker)
    

def fetch_etf_snapshot(ticker: str) -> ETFSnapshot:
    """
    Fetch ETF data from Yahoo Finance and return a validated ETFSnapshot.

    The function attempts multiple ticker suffixes (e.g. .DE, .F) to resolve
    ETF listings across exchanges.

    Raises:
        ValueError: If no valid ETF data could be retrieved.
    """
    
    last_tried_symbol = ticker

    for suffix in ETF_SUFFIX_CANDIDATES:
        symbol = f"{ticker}{suffix}"
        last_tried_symbol = symbol
        info = _extract_info(symbol)

        if is_valid_etf_info(info):
            return ETFSnapshot(
                ticker=symbol,
                fund_name=info.get("longName") or info.get("shortName"),
                issuer=None,
                expense_ratio=get_expense_ratio(ticker),
                aum=info.get("totalAssets"),
                currency=info.get("currency"),
                replication_method=None,
                top_holdings=[],
                sector_allocation=[],
                country_allocation=[],
                price=info.get("regularMarketPrice"),
            )

    raise ValueError(f"Could not fetch ETF data for ticker '{ticker}'. Last tried: {last_tried_symbol}")