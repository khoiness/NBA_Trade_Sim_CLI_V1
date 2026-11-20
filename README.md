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

Choose Team A and Team B, select outgoing and incoming players, and compare Team A's salary totals and player-by-player salary stacks before and after a proposed trade. The app also shows the roster's 2025–26 shot distribution across five court areas before and after the trade. Use **Swap teams** to reverse the teams and trade packages. The salary visualization includes 2026–27 cap, tax, and apron thresholds.

## Run with Docker

Build the image from the repository root:

```powershell
docker build -t nba-trade-simulator .
```

Run the app and open <http://localhost:8501>:

```powershell
docker run --rm -p 8501:8501 nba-trade-simulator
```

The app fetches roster, statistics, and shot-location data from the NBA API while it runs, so the container needs network access.

## Live development with Docker Compose

Start the app from the repository root:

```powershell
docker compose up --build
```

Open <http://localhost:8501>. The project is mounted into the container, and Streamlit watches for file changes and reruns the app when you save edits. Stop the app with `Ctrl+C`.

## Project structure

- `nba_trade_simulator/data.py` — loads roster and player statistics
- `nba_trade_simulator/scoring.py` — computes player value scores
- `nba_trade_simulator/salary.py` — salary matching helpers
- `nba_trade_simulator/simulator.py` — Team A salary comparison logic
- `nba_trade_simulator/export.py` — JSON/CSV output helpers
- `nba_trade_simulator/cli.py` — CLI entrypoint
