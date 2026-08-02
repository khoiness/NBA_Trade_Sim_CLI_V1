# NBA Trade Simulator CLI

A small structured Python app that uses `nba_api` to evaluate NBA trade proposals and apply basic salary matching rules.

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

## Usage

Evaluate a trade between two teams by player names or IDs:

```powershell
python -m nba_trade_simulator.cli simulate \
  --team-a LAL \
  --team-b BOS \
  --team-a-players LeBron James,Anthony Davis \
  --team-b-players Jayson Tatum,Jaylen Brown \
  --output "trade_report.json"
```

If you have a CSV salary file, pass it with `--salary-file`.

## Project structure

- `nba_trade_simulator/data.py` — loads roster and player statistics
- `nba_trade_simulator/scoring.py` — computes player value scores
- `nba_trade_simulator/salary.py` — salary matching helpers
- `nba_trade_simulator/simulator.py` — trade evaluation logic
- `nba_trade_simulator/export.py` — JSON/CSV output helpers
- `nba_trade_simulator/cli.py` — CLI entrypoint
