from typing import Optional

import pandas as pd
from nba_api.stats.endpoints import commonteamroster, leaguedashplayerstats
from nba_api.stats.static import teams


def fetch_player_stats(season: str = "2025-26", per_mode: str = "PerGame") -> pd.DataFrame:
    """Fetch league-wide player stats for the selected season."""
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_simple=per_mode,
        timeout=30,
    )
    frame = stats.get_data_frames()[0]
    if frame.empty:
        return frame
    frame = frame.rename(columns={
        "PLAYER_ID": "player_id",
        "PLAYER_NAME": "player_name",
        "TEAM_ABBREVIATION": "team_abbreviation",
        "MIN": "minutes",
        "PTS": "points",
        "REB": "rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "TOV": "turnovers",
        "FG_PCT": "field_goal_pct",
        "FG3_PCT": "three_pt_pct",
        "FT_PCT": "free_throw_pct",
        "TS_PCT": "true_shooting_pct",
    })
    numeric = [
        "minutes",
        "points",
        "rebounds",
        "assists",
        "steals",
        "blocks",
        "turnovers",
        "field_goal_pct",
        "three_pt_pct",
        "free_throw_pct",
        "true_shooting_pct",
    ]
    for col in numeric:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)
    return frame


def fetch_team_roster(team_abbreviation: str, season: str = "2025-26") -> pd.DataFrame:
    """Fetch the current roster for a team."""
    team = teams.find_team_by_abbreviation(team_abbreviation)
    if not team:
        raise ValueError(f"Unknown team abbreviation: {team_abbreviation}")
    roster = commonteamroster.CommonTeamRoster(
        team_id=team["id"],
        season=season,
        timeout=30,
    )
    frame = roster.get_data_frames()[0]
    frame = frame.rename(columns={
        "PLAYER": "player_name",
        "PLAYER_ID": "player_id",
        "POSITION": "position",
        "HEIGHT": "height",
        "WEIGHT": "weight",
        "SCHOOL": "college",
    })
    return frame[["player_id", "player_name", "position", "height", "weight", "college"]]


def build_roster_with_stats(team_abbreviation: str, season: str = "2025-26") -> pd.DataFrame:
    """Build a roster DataFrame enriched with stats."""
    roster = fetch_team_roster(team_abbreviation, season=season)
    stats = fetch_player_stats(season=season)
    enriched = roster.merge(stats, how="left", on=["player_id", "player_name"])
    return enriched
