import pandas as pd


def load_salary_data(path: str) -> pd.DataFrame:
    """Load player salary information from a CSV file."""
    salaries = pd.read_csv(path)
    salaries = salaries.rename(columns={
        "PLAYER_ID": "player_id",
        "PLAYER_NAME": "player_name",
        "SALARY": "salary",
    })
    salaries["salary"] = pd.to_numeric(salaries["salary"], errors="coerce").fillna(0)
    return salaries[["player_id", "player_name", "salary"]]


def compute_salary_total(players) -> float:
    """Compute total salary for a group of players.

    Accepts a pandas DataFrame or a sequence of dict-like records.
    """
    if players is None:
        return 0.0
    if isinstance(players, pd.DataFrame):
        if players.empty:
            return 0.0
        return float(players["salary"].sum())
    salaries = pd.DataFrame(players)
    if salaries.empty or "salary" not in salaries.columns:
        return 0.0
    return float(salaries["salary"].sum())


def is_salary_match(outgoing: float, incoming: float, tolerance: float = 0.125) -> bool:
    """Check whether salaries match within a tolerance used for simple trade feasibility."""
    if outgoing <= 0 or incoming <= 0:
        return False
    lower = outgoing * (1 - tolerance)
    upper = outgoing * (1 + tolerance)
    return lower <= incoming <= upper


def salary_match_report(outgoing: float, incoming: float, tolerance: float = 0.125) -> dict:
    """Return a summary report of salary matching status."""
    return {
        "outgoing_salary": float(outgoing),
        "incoming_salary": float(incoming),
        "ratio": float(incoming / outgoing) if outgoing else 0.0,
        "tolerance": float(tolerance),
        "matches": is_salary_match(outgoing, incoming, tolerance),
    }
