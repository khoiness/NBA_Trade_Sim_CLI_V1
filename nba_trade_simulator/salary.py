import pandas as pd


def load_salary_data(path: str, season: str = "2026-27") -> pd.DataFrame:
    """Load player salary information from the salary CSV."""
    salaries = pd.read_csv(path)
    if "Player" not in salaries.columns and "PLAYER_NAME" not in salaries.columns:
        salaries = pd.read_csv(path, skiprows=1)
    name_column = "PLAYER_NAME" if "PLAYER_NAME" in salaries.columns else "Player"
    salary_column = "SALARY" if "SALARY" in salaries.columns else season
    if name_column not in salaries.columns or salary_column not in salaries.columns:
        raise ValueError(f"Salary CSV must contain {name_column!r} and {salary_column!r}")
    salaries = salaries.rename(columns={name_column: "player_name", salary_column: "salary"})
    if "player_id" not in salaries.columns:
        salaries["player_id"] = pd.NA
    salaries["salary"] = pd.to_numeric(
        salaries["salary"].replace(r"[\$,]", "", regex=True),
        errors="coerce",
    ).fillna(0)
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
