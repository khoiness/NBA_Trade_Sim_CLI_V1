from typing import Dict, List, Optional

import pandas as pd

from .scoring import add_value_scores, aggregate_trade_value
from .salary import compute_salary_total, salary_match_report


def resolve_player_selection(players: pd.DataFrame, selection: List[str]) -> pd.DataFrame:
    """Return a DataFrame of players matching the selection list by name or ID."""
    if players is None or players.empty or not selection:
        return pd.DataFrame(columns=players.columns)
    selected = players[players["player_name"].isin(selection) | players["player_id"].isin(selection)]
    if selected.empty:
        selected = players[players["player_name"].str.contains("|".join(selection), case=False, na=False)]
    return selected


def evaluate_trade(
    team_a_name: str,
    team_b_name: str,
    team_a_out: List[str],
    team_b_out: List[str],
    roster_a: pd.DataFrame,
    roster_b: pd.DataFrame,
    salary_a: Optional[pd.DataFrame] = None,
    salary_b: Optional[pd.DataFrame] = None,
    salary_tolerance: float = 0.125,
) -> Dict:
    """Evaluate a proposed trade from the perspective of both teams."""
    roster_a = add_value_scores(roster_a)
    roster_b = add_value_scores(roster_b)

    team_a_outgoing = resolve_player_selection(roster_a, team_a_out)
    team_b_outgoing = resolve_player_selection(roster_b, team_b_out)

    team_a_incoming = resolve_player_selection(roster_b, team_b_out)
    team_b_incoming = resolve_player_selection(roster_a, team_a_out)

    team_a_out_value = aggregate_trade_value(team_a_outgoing)
    team_a_in_value = aggregate_trade_value(team_a_incoming)
    team_b_out_value = aggregate_trade_value(team_b_outgoing)
    team_b_in_value = aggregate_trade_value(team_b_incoming)

    team_a_salary_out = compute_salary_total(team_a_outgoing)
    team_a_salary_in = compute_salary_total(team_a_incoming)
    team_b_salary_out = compute_salary_total(team_b_outgoing)
    team_b_salary_in = compute_salary_total(team_b_incoming)

    salary_report_a = salary_match_report(team_a_salary_out, team_a_salary_in, tolerance=salary_tolerance)
    salary_report_b = salary_match_report(team_b_salary_out, team_b_salary_in, tolerance=salary_tolerance)

    return {
        "team_a": {
            "name": team_a_name,
            "outgoing": team_a_outgoing.to_dict(orient="records"),
            "incoming": team_a_incoming.to_dict(orient="records"),
            "outgoing_value": team_a_out_value,
            "incoming_value": team_a_in_value,
            "delta_value": team_a_in_value - team_a_out_value,
            "salary": salary_report_a,
        },
        "team_b": {
            "name": team_b_name,
            "outgoing": team_b_outgoing.to_dict(orient="records"),
            "incoming": team_b_incoming.to_dict(orient="records"),
            "outgoing_value": team_b_out_value,
            "incoming_value": team_b_in_value,
            "delta_value": team_b_in_value - team_b_out_value,
            "salary": salary_report_b,
        },
        "summary": {
            "team_a_favorable": team_a_in_value >= team_a_out_value,
            "team_b_favorable": team_b_in_value >= team_b_out_value,
        },
    }
