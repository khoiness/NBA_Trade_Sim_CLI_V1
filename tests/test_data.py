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
