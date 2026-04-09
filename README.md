# ETF Guardian — Agentic ETF Monitoring System

## Overview

This project implements an agentic decision-support system for long-term ETF monitoring.

The system analyzes a given ETF and:

- detects material changes (e.g. assets under management, cost structure)
- interprets them in terms of risk
- identifies better alternatives within the same exposure group
- returns structured, explainable output via a REST API

The core objective is to filter noise and surface only meaningful signals that may require investor attention.

The system is designed as a deterministic, testable pipeline, where all decision logic is explicitly defined and traceable, without relying on LLM-based reasoning.

## Key Features

- Agentic pipeline built with LangGraph (multi-step orchestration)
- Deterministic decision logic (fully testable and explainable)
- ETF change detection with direction and severity classification
- Risk classification layer (cost, liquidity, structural signals)
- Comparable ETF selection constrained by exposure group
- Dominant ETF identification based on cost and AUM thresholds
- Structured outputs using Pydantic schemas
- REST API (FastAPI) for programmatic access
- Unit and integration tests

## Tech Stack

- Python
- FastAPI (API layer)
- LangGraph (agent orchestration)
- Pydantic (data validation and structured output)
- yfinance (market data ingestion)
- pytest (testing)

## System Architecture

The system is structured as a modular decision pipeline composed of the following layers:

- **Data ingestion**  
  Retrieves ETF data from Yahoo Finance, with controlled fallback logic for missing fields (e.g. expense ratio).

- **Agent orchestration (LangGraph)**  
  Coordinates the execution of multiple processing steps as a stateful pipeline.

- **Decision logic layer**  
  Implements deterministic rules for:
  - change detection
  - risk classification
  - comparable ETF selection
  - dominance evaluation

- **Output synthesis**  
  Converts the internal agent state into a structured, user-facing response.

- **API layer (FastAPI)**  
  Exposes the system via a REST endpoint for external use.

The architecture separates data retrieval, decision logic, and presentation, ensuring testability and extensibility.

## Pipeline

The system follows a deterministic agent pipeline:

```text
User request (`/analyze?ticker=...`)
      │
      ▼
Fetch current ETF snapshot
      │
      ▼
Load / simulate previous snapshot
      │
      ▼
Detect changes (e.g. AUM, cost)
      │
      ▼
Classify risks
      │
      ▼
Select comparable ETFs (same exposure group)
      │
      ▼
Evaluate dominance (cost + AUM)
      │
      ▼
Synthesize structured output
```


### 1. Data Retrieval
ETF data is fetched using Yahoo Finance, with fallback logic for missing fields (e.g. expense ratio).

### 2. Change Detection
The current snapshot is compared with a previous snapshot to identify material changes (e.g. AUM growth), including direction and severity.

### 3. Risk Classification
Detected changes are mapped to risk categories (e.g. liquidity, cost), while avoiding false positives for benign changes.

### 4. Comparable Selection
Comparable ETFs are selected based on predefined exposure groups to ensure valid comparisons.

### 5. Dominance Evaluation
A dominant ETF is identified if:
- it has a lower expense ratio
- and sufficient AUM relative to the current ETF

### 6. Output Synthesis
The final output is constructed as a structured response, including:
- status
- status explanation
- dominant ETF (if applicable)

The pipeline is fully deterministic and each step operates on a shared state, ensuring traceability and testability.

## Project Structure

```text
etf-monitoring-agent
│
├── api
│   └── main.py                  # FastAPI application
│
├── src
│   └── etf_monitoring_agent
│       ├── agent
│       │   ├── graph.py          # LangGraph pipeline definition
│       │   ├── state.py          # agent state definition (TypedDict)
│       │   └── nodes
│       │       ├── changes.py    # change detection logic
│       │       ├── comparables.py# comparable ETF selection
│       │       ├── dominance.py  # dominant ETF identification
│       │       ├── fetch.py      # current ETF snapshot retrieval
│       │       ├── history.py    # previous snapshot loading / simulation
│       │       ├── risks.py      # risk classification logic
│       │       └── synthesize.py # final output construction
│       │
│       ├── schemas
│       │   ├── input.py          # input schema (API / agent entry point)
│       │   ├── internal.py       # internal data models
│       │   └── output.py         # API response schema
│       │
│       └── tools
│           ├── comparables.py    # exposure-based comparable ETF selection
│           └── etf_data.py       # data ingestion (yfinance + fallback logic)
│
├── tests                        # unit and integration tests
│   ├── test_api.py
│   ├── test_dominance.py
│   └── test_graph.py
│
├── .gitignore
├── pyproject.toml
├── LICENSE
└── README.md
```

## API

The system exposes a REST API for ETF analysis.

### Endpoint

`GET /analyze?ticker=...`

### Description

Runs the full agent pipeline for the provided ETF ticker and returns a structured analysis.

### Query Parameters

- `ticker` (str): ETF ticker symbol (e.g. `VWCE`, `SPY`, `EEM`)

### Response Model

The endpoint returns a structured response defined by `ETFAnalysisOutput`, including:

- `ticker`
- `status` (stable | monitor | review)
- `status_reason`
- `detected_changes`
- `risk_flags`
- `dominant_etf` (if applicable)

The API layer is intentionally kept thin and delegates all logic to the agent pipeline.

## Example Response

Example request:


```bash
GET /analyze?ticker=VWCE`
```

Example response:

```json
{
  "ticker": "VWCE",
  "status": "review",
  "status_reason": "IWDA provides a lower-cost alternative with sufficient scale.",
  "detected_changes": [
    {
      "change_type": "aum_increase",
      "severity": "low",
      "description": "AUM changed from 47588877926.40 to 59486097408.00 (25.0%)."
    }
  ],
  "risk_flags": [],
  "dominant_etf": {
    "ticker": "IWDA",
    "fund_name": "iShares Core MSCI World UCITS ETF",
    "expense_ratio": 0.002,
    "aum": 70000000000,
    "currency": "USD",
    "replication_method": "physical"
  }
}
```

## Installation

Clone the repository and install the project in editable mode:

```bash
git clone https://github.com/przemekwarnel/etf-monitoring-agent.git
cd etf-monitoring-agent

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

## How to Run

Start the FastAPI application locally:

```bash
PYTHONPATH=src uvicorn api.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## Testing

Run the full test suite:

```bash
pytest
```

## Design Decisions

### Deterministic decision logic instead of LLM-based reasoning

The core system is fully deterministic. All decisions (change detection, risk classification, dominance) are implemented as explicit rules rather than relying on LLMs.

This ensures:
- full testability
- predictable behavior
- easier debugging
- no hidden decision logic

LLMs can be introduced later as an optional explanation layer, but not as part of the core decision-making.

---

### Agent-based architecture with LangGraph

The system is implemented as a multi-step agent pipeline using LangGraph, where each node operates on a shared state.

This approach allows:
- clear separation of responsibilities
- step-by-step traceability
- modular testing of individual components
- easy extension of the pipeline

---

### Exposure-based comparable selection

Comparable ETFs are selected using predefined exposure groups (e.g. S&P 500, emerging markets, global equity).

This prevents invalid comparisons (e.g. global ETF vs single-market ETF) and ensures that dominance evaluation is meaningful.

The current implementation is rule-based, but can be extended with richer metadata or external data sources.

---

### Explicit dominance criteria

A dominant ETF is identified only if it satisfies both:

- lower expense ratio
- sufficient AUM relative to the current ETF

This avoids recommending:
- illiquid alternatives
- marginal improvements that are not practically relevant

---

### Separation of internal and output schemas

The system distinguishes between:
- internal data models used in the pipeline
- output schemas exposed via the API

This prevents leakage of internal implementation details and keeps the API contract stable.

---

### Thin API layer

The FastAPI layer contains no business logic and only orchestrates the execution of the agent pipeline.

All decision-making is delegated to the core system, ensuring:
- clean architecture
- easier testing
- reusability of the core logic outside the API context

---

### Controlled handling of missing data

ETF data retrieved from Yahoo Finance is not fully reliable (e.g. missing expense ratios).

To ensure consistent behavior, fallback values are used where necessary.

This allows the system to remain functional while clearly isolating data quality limitations from decision logic.

## Limitations

- Expense ratio data is partially based on fallback values due to limitations of Yahoo Finance
- Comparable ETF selection is rule-based and limited to predefined exposure groups
- No persistent storage of ETF snapshots (change detection is based on simulated previous state)
- No alerting or scheduling mechanism (analysis is triggered manually via API)
- Limited coverage of ETF universe (only selected tickers supported in comparables mapping)


## Future Work

- Persistent storage of ETF snapshots (e.g. SQLite or object storage)
- Scheduled monitoring and alerting (e.g. cron-based jobs, email/webhook notifications)
- Improved comparable selection using richer ETF metadata (region, index, sector)
- Portfolio-level analysis (concentration, overlap, weighted cost)
- Optional LLM-based explanation layer for natural language summaries
- Deployment as a public API or demo application