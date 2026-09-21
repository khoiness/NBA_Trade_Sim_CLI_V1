from typing import List

import pandas as pd

def build_team_a_salary_comparison(
    roster_a: pd.DataFrame,
    roster_b: pd.DataFrame,
    team_a_out: List[str],
    team_b_in: List[str],
) -> pd.DataFrame:
    """Return Team A's player salaries before and after a proposed trade."""
    incoming = roster_b[roster_b["player_name"].isin(team_b_in)].copy()

    before = roster_a[["player_name", "salary"]].copy()
    before["status"] = "Before trade"
    after = roster_a[~roster_a["player_name"].isin(team_a_out)][["player_name", "salary"]].copy()
    incoming_after = incoming[["player_name", "salary"]].copy()
    after = pd.concat([after, incoming_after], ignore_index=True)
    after["status"] = "After trade"

    comparison = pd.concat([before, after], ignore_index=True)
    comparison["salary"] = pd.to_numeric(comparison["salary"], errors="coerce").fillna(0)
    comparison["salary_millions"] = comparison["salary"] / 1_000_000
    return comparison.sort_values(["status", "salary"], ascending=[True, False]).reset_index(drop=True)
