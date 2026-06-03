import pandas as pd


def compute_player_value(row: pd.Series) -> float:
    """Compute a composite player value score from common per-game stats."""
    score = 0.0
    score += row.get("points", 0.0) * 1.0
    score += row.get("assists", 0.0) * 1.5
    score += row.get("rebounds", 0.0) * 1.2
    score += row.get("steals", 0.0) * 2.0
    score += row.get("blocks", 0.0) * 2.0
    score -= row.get("turnovers", 0.0) * 1.5
    score += row.get("minutes", 0.0) * 0.08
    score += row.get("true_shooting_pct", 0.0) * 8.0
    score += row.get("field_goal_pct", 0.0) * 2.0
    if row.get("age") is not None and row.get("age") > 0:
        age_penalty = max(0.0, (row["age"] - 27) * 0.3)
        score -= age_penalty
    return float(score)


def add_value_scores(players: pd.DataFrame) -> pd.DataFrame:
    """Add a computed value score for each player in the DataFrame."""
    players = players.copy()
    if "player_value" not in players.columns:
        players["player_value"] = players.apply(compute_player_value, axis=1)
    return players


def aggregate_trade_value(players: pd.DataFrame) -> float:
    """Sum the value scores for a group of players."""
    if players is None or players.empty:
        return 0.0
    return float(players["player_value"].sum())
