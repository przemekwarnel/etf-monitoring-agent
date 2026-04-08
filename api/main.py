from fastapi import FastAPI, HTTPException, Query

from etf_monitoring_agent.agent.graph import build_graph
from etf_monitoring_agent.schemas.output import ETFAnalysisOutput


graph = build_graph()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application for the ETF analysis service."""

    app = FastAPI(
        title="ETF Monitoring & Analysis Agent",
        version="0.1.0",
        description="API for analyzing ETFs with a LangGraph-based agent pipeline.",
    )

    @app.get("/")
    def root() -> dict[str, str]:
        """Return basic metadata about the API service."""
        return {
            "service": "ETF Monitoring & Analysis Agent",
            "version": "0.1.0",
            "docs_url": "/docs",
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        """Return a simple health status for monitoring and deployment checks."""
        return {"status": "ok"}

    @app.get("/analyze", response_model=ETFAnalysisOutput)
    def analyze_etf(
        ticker: str = Query(..., min_length=1, description="ETF ticker, e.g. VWCE"),
    ) -> ETFAnalysisOutput:
        """Run the ETF analysis graph for the provided ticker and return structured results."""

        normalized_ticker = ticker.strip().upper()

        try:
            result = graph.invoke({"ticker": normalized_ticker})
            return result["final_output"]
        except KeyError as exc:
            raise HTTPException(status_code=500, detail="Graph did not return final_output") from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"ETF analysis failed: {exc}") from exc
        
    return app


app = create_app()