import pandas as pd

from nba_trade_simulator import data


def test_fetch_player_stats_uses_supported_nba_api_parameter(monkeypatch):
    captured = {}

    class DummyLeagueDashPlayerStats:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def get_data_frames(self):
            return [pd.DataFrame()]

    monkeypatch.setattr(data.leaguedashplayerstats, "LeagueDashPlayerStats", DummyLeagueDashPlayerStats)

    data.fetch_player_stats(season="2025-26", per_mode="PerGame")

    assert captured["per_mode_detailed"] == "PerGame"
    assert "per_mode_simple" not in captured


def test_fetch_player_shot_locations_sums_corner_threes_and_uses_totals(monkeypatch):
    captured = {}
    columns = pd.MultiIndex.from_tuples(
        [
            ("", "PLAYER_ID"),
            ("Restricted Area", "FGA"),
            ("In The Paint (Non-RA)", "FGA"),
            ("Mid-Range", "FGA"),
            ("Left Corner 3", "FGA"),
            ("Right Corner 3", "FGA"),
            ("Above the Break 3", "FGA"),
        ]
    )
    frame = pd.DataFrame(
        [[1, 100, 50, 25, 10, 15, 75]],
        columns=columns,
    )

    class DummyLeagueDashPlayerShotLocations:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def get_data_frames(self):
            return [frame]

    monkeypatch.setattr(
        data.leaguedashplayershotlocations,
        "LeagueDashPlayerShotLocations",
        DummyLeagueDashPlayerShotLocations,
    )

    result = data.fetch_player_shot_locations(season="2025-26")

    assert captured["distance_range"] == "By Zone"
    assert captured["per_mode_detailed"] == "Totals"
    assert captured["season_type_all_star"] == "Regular Season"
    assert result.loc[0, "corner_three"] == 25
    assert result.loc[0, "restricted_area"] == 100
