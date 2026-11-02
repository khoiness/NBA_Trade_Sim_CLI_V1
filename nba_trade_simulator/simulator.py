from typing import List

import pandas as pd

from nba_trade_simulator.data import SHOT_AREA_COLUMNS, SHOT_AREA_LABELS


def build_team_a_salary_comparison(
    roster_a: pd.DataFrame,
    roster_b: pd.DataFrame,
    team_a_out: List[str],
    team_b_in: List[str],
) -> pd.DataFrame:
    """Return Team A's player salaries before and after a proposed trade."""
    incoming = roster_b[roster_b["player_name"].isin(team_b_in)].copy()

    before = roster_a[["player_id", "player_name", "salary"]].copy()
    before["status"] = "Before trade"
    after = roster_a[~roster_a["player_name"].isin(team_a_out)][
        ["player_id", "player_name", "salary"]
    ].copy()
    incoming_after = incoming[["player_id", "player_name", "salary"]].copy()
    after = pd.concat([after, incoming_after], ignore_index=True)
    after["status"] = "After trade"

    comparison = pd.concat([before, after], ignore_index=True)
    comparison["salary"] = pd.to_numeric(comparison["salary"], errors="coerce").fillna(0)
    comparison["salary_millions"] = comparison["salary"] / 1_000_000
    return comparison.sort_values(["status", "salary"], ascending=[True, False]).reset_index(drop=True)


def aggregate_shot_attempts_by_status(
    comparison: pd.DataFrame,
    player_shot_locations: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate shot attempts and proportions by roster status and shot area."""
    comparison_shots = comparison[["status", "player_id"]].merge(
        player_shot_locations[["player_id", *SHOT_AREA_COLUMNS]],
        on="player_id",
        how="left",
        validate="many_to_one",
    )
    for column in SHOT_AREA_COLUMNS:
        comparison_shots[column] = pd.to_numeric(
            comparison_shots[column], errors="coerce"
        ).fillna(0)

    shot_totals = (
        comparison_shots.groupby("status")[list(SHOT_AREA_COLUMNS)]
        .sum()
        .reindex(["Before trade", "After trade"], fill_value=0)
        .rename_axis("status")
        .reset_index()
        .melt(
            id_vars="status",
            var_name="shot_area",
            value_name="attempts",
        )
    )
    shot_totals["shot_area"] = shot_totals["shot_area"].map(SHOT_AREA_LABELS)
    shot_totals["total_attempts"] = shot_totals.groupby("status")[
        "attempts"
    ].transform("sum")
    shot_totals["proportion"] = (
        shot_totals["attempts"]
        .div(shot_totals["total_attempts"].where(shot_totals["total_attempts"] > 0))
        .fillna(0)
    )
    return shot_totals
