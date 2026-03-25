import yfinance as yf

from schemas.internal import ETFSnapshot


ETF_SUFFIX_CANDIDATES = ["", ".DE", ".F", ".AS", ".DU"]


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
                expense_ratio=info.get("expenseRatio"),
                aum=info.get("totalAssets"),
                currency=info.get("currency"),
                replication_method=None,
                top_holdings=[],
                sector_allocation=[],
                country_allocation=[],
                price=info.get("regularMarketPrice"),
            )

    raise ValueError(f"Could not fetch ETF data for ticker '{ticker}'. Last tried: {last_tried_symbol}")