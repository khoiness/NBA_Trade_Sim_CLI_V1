# NBA Trade Simulator

A small Python app that uses `nba_api` to explore NBA rosters and compare team salary totals before and after a proposed trade.

## Features
- Fetch rosters and player stats from `nba_api`
- Compute player value scores from season statistics
- Evaluate proposed trades and score roster changes
- Apply simple salary matching rules for feasibility
- Export results as JSON or CSV for external visualization

## Installation

1. Create a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Interactive app

Start the Streamlit interface:

```powershell
streamlit run app.py
```

Choose Team A, choose a second team, select outgoing and incoming players, and review Team A's complete salary roster before and after the proposed trade.

## CLI usage

Dump player statistics by season:

```powershell
python -m nba_trade_simulator.cli dump-stats \
  --season 2025-26 \
  --output "stats.json"
```

The previous two-team trade evaluator is temporarily disabled while the salary comparison view is being developed.

## Project structure

- `nba_trade_simulator/data.py` — loads roster and player statistics
- `nba_trade_simulator/scoring.py` — computes player value scores
- `nba_trade_simulator/salary.py` — salary matching helpers
- `nba_trade_simulator/simulator.py` — Team A salary comparison logic
- `nba_trade_simulator/export.py` — JSON/CSV output helpers
- `nba_trade_simulator/cli.py` — CLI entrypoint
