# AI-Powered Financial Research Agent

A full-stack financial research application built with **HTML/CSS/JavaScript + FastAPI + Python**.

## Phase 1 completed
- FastAPI backend
- HTML/CSS/JavaScript frontend
- Stock ticker search
- Historical market-data retrieval using `yfinance`
- SMA, EMA, RSI and return/volatility calculations
- Interactive Chart.js visualizations
- REST API endpoint with Swagger docs

## Roadmap
1. Financial news API
2. LLM sentiment analysis
3. LangChain/LangGraph tool calling
4. RAG over financial reports
5. PostgreSQL + pgvector
6. Production hardening, Docker and deployment

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
Open `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

> Educational/research project. It does not execute trades or provide personalized financial advice.
