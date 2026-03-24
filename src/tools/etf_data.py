import yfinance as yf
from schemas.internal import ETFSnapshot


def fetch_etf_snapshot(ticker: str) -> ETFSnapshot:
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.info

    return ETFSnapshot(
        ticker=ticker,
        fund_name=info.get("longName"),
        issuer=info.get("companyOfficers", [{}])[0].get("name") if info.get("companyOfficers") else None,
        expense_ratio=info.get("expenseRatio"),
        aum=info.get("totalAssets"),
        currency=info.get("currency"),
        replication_method=None,  # not in yfinance
        top_holdings=[],  # will add later
        sector_allocation=[],
        country_allocation=[],
    )