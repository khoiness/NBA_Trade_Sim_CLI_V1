import json
from pathlib import Path
from typing import List, Optional

import click
import pandas as pd

try:
    from .data import build_roster_with_stats, fetch_player_stats
    from .export import export_csv, export_json
    from .salary import load_salary_data
except ImportError:  # pragma: no cover - supports running this file directly
    from data import build_roster_with_stats, fetch_player_stats
    from export import export_csv, export_json
    from salary import load_salary_data


def parse_player_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@click.group()
def main() -> None:
    """NBA Trade Simulator CLI."""
    pass


@main.command(name="dump-stats")
@click.option("--season", default="2025-26", show_default=True, help="Season to load stats for.")
@click.option("--output", required=True, type=click.Path(), help="Output JSON file path for player statistics.")
def dump_stats(season: str, output: str) -> None:
    click.echo(f"Fetching player statistics for season {season}...")
    stats = fetch_player_stats(season=season)
    stats.to_json(output, orient="records", indent=2)
    click.echo(f"Wrote stats for {len(stats)} players to {output}")


if __name__ == "__main__":
    main()
