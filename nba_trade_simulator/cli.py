import json
from pathlib import Path
from typing import List, Optional

import click
import pandas as pd

try:
    from .data import build_roster_with_stats, fetch_player_stats
    from .export import export_csv, export_json
    from .salary import load_salary_data
    from .simulator import evaluate_trade
except ImportError:  # pragma: no cover - supports running this file directly
    from data import build_roster_with_stats, fetch_player_stats
    from export import export_csv, export_json
    from salary import load_salary_data
    from simulator import evaluate_trade


def parse_player_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@click.group()
def main() -> None:
    """NBA Trade Simulator CLI."""
    pass


@main.command(name="simulate")
@click.option("--team-a", required=True, help="Team A abbreviation, e.g. LAL.")
@click.option("--team-b", required=True, help="Team B abbreviation, e.g. BOS.")
@click.option(
    "--team-a-players",
    required=True,
    help="Comma-separated list of Team A players moving out of the roster.",
)
@click.option(
    "--team-b-players",
    required=True,
    help="Comma-separated list of Team B players moving out of the roster.",
)
@click.option("--salary-file", type=click.Path(exists=True), help="Optional CSV file with player salary data.")
@click.option("--output", required=True, type=click.Path(), help="Output file path for JSON or CSV.")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "csv"], case_sensitive=False),
    default="json",
    show_default=True,
    help="Export format for the trade report.",
)
def simulate(
    team_a: str,
    team_b: str,
    team_a_players: str,
    team_b_players: str,
    salary_file: Optional[str],
    output: str,
    output_format: str,
) -> None:
    team_a_players_list = parse_player_list(team_a_players)
    team_b_players_list = parse_player_list(team_b_players)

    click.echo(f"Loading roster for {team_a} and {team_b}...")
    roster_a = build_roster_with_stats(team_a)
    roster_b = build_roster_with_stats(team_b)

    salary_a = pd.DataFrame()
    salary_b = pd.DataFrame()
    if salary_file:
        click.echo(f"Loading salary data from {salary_file}...")
        salaries = load_salary_data(salary_file)
        salary_a = roster_a.merge(salaries, how="left", on=["player_id", "player_name"])
        salary_b = roster_b.merge(salaries, how="left", on=["player_id", "player_name"])
    else:
        roster_a["salary"] = 0.0
        roster_b["salary"] = 0.0
        salary_a = roster_a
        salary_b = roster_b

    click.echo("Evaluating trade...")
    report = evaluate_trade(
        team_a_name=team_a,
        team_b_name=team_b,
        team_a_out=team_a_players_list,
        team_b_out=team_b_players_list,
        roster_a=salary_a,
        roster_b=salary_b,
    )

    output_path = Path(output)
    if output_format.lower() == "json":
        export_json(report, str(output_path))
    else:
        export_csv(report, str(output_path))

    click.echo(f"Trade simulation complete. Results written to {output_path}")


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
