import pandas as pd

from nba_trade_simulator.simulator import aggregate_shot_attempts_by_status


def test_aggregate_shot_attempts_by_status_reflects_trade_and_proportions():
    comparison = pd.DataFrame(
        [
            {"player_id": 1, "status": "Before trade"},
            {"player_id": 2, "status": "Before trade"},
            {"player_id": 1, "status": "After trade"},
            {"player_id": 3, "status": "After trade"},
        ]
    )
    shot_locations = pd.DataFrame(
        [
            {
                "player_id": 1,
                "restricted_area": 20,
                "paint": 10,
                "mid_range": 5,
                "corner_three": 5,
                "above_break_three": 10,
            },
            {
                "player_id": 2,
                "restricted_area": 10,
                "paint": 5,
                "mid_range": 5,
                "corner_three": 0,
                "above_break_three": 10,
            },
            {
                "player_id": 3,
                "restricted_area": 10,
                "paint": 0,
                "mid_range": 0,
                "corner_three": 10,
                "above_break_three": 20,
            },
        ]
    )

    result = aggregate_shot_attempts_by_status(comparison, shot_locations)
    totals = result.pivot(index="status", columns="shot_area", values="attempts")
    proportions = result.groupby("status")["proportion"].sum()

    assert totals.loc["Before trade", "Restricted area"] == 30
    assert totals.loc["Before trade", "Corner three"] == 5
    assert totals.loc["After trade", "Corner three"] == 15
    assert proportions.to_dict() == {"After trade": 1.0, "Before trade": 1.0}
