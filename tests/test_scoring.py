import pandas as pd

from nba_trade_simulator.scoring import add_value_scores, compute_player_value


def test_compute_player_value_positive():
    row = pd.Series({
        "points": 20,
        "assists": 5,
        "rebounds": 7,
        "steals": 1,
        "blocks": 1,
        "turnovers": 2,
        "minutes": 32,
        "true_shooting_pct": 0.58,
        "field_goal_pct": 0.48,
        "age": 28,
    })
    value = compute_player_value(row)
    assert value > 0


def test_add_value_scores_adds_column():
    df = pd.DataFrame([
        {"player_name": "Test Player", "points": 10, "assists": 3, "rebounds": 5, "turnovers": 1, "minutes": 25, "true_shooting_pct": 0.55, "field_goal_pct": 0.45},
    ])
    scored = add_value_scores(df)
    assert "player_value" in scored.columns
    assert scored.at[0, "player_value"] > 0
