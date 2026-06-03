import csv
import json
from typing import Any, Dict


def export_json(report: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)


def export_csv(report: Dict[str, Any], path: str) -> None:
    rows = []
    for team_key in ["team_a", "team_b"]:
        team = report[team_key]
        side = "outgoing"
        for row in team["outgoing"]:
            rows.append({
                "team": team["name"],
                "side": side,
                "player_name": row.get("player_name"),
                "player_id": row.get("player_id"),
                "player_value": row.get("player_value", 0),
                "salary": row.get("salary", 0),
            })
        side = "incoming"
        for row in team["incoming"]:
            rows.append({
                "team": team["name"],
                "side": side,
                "player_name": row.get("player_name"),
                "player_id": row.get("player_id"),
                "player_value": row.get("player_value", 0),
                "salary": row.get("salary", 0),
            })
    fieldnames = ["team", "side", "player_name", "player_id", "player_value", "salary"]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
