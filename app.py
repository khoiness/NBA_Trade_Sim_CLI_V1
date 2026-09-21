import streamlit as st
from pathlib import Path

from nba_trade_simulator.data import build_roster_with_stats
from nba_trade_simulator.salary import load_salary_data
from nba_trade_simulator.simulator import build_team_a_salary_comparison

TEAM_CODES = ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET",
              "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
              "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS",
              "TOR", "UTA", "WAS"]


@st.cache_data(ttl=3600)
def load_roster(team_code: str, salary_file: str):
    roster = build_roster_with_stats(team_code)
    salaries = load_salary_data(salary_file)
    return roster.merge(salaries[["player_name", "salary"]], how="left", on="player_name")


def format_salary(value: float) -> str:
    return f"${value / 1_000_000:,.1f}M"


st.set_page_config(page_title="NBA Trade Simulator", layout="wide")
st.title("NBA Salary Before and After")
st.caption("Choose a Team A package and incoming players to see how the roster salary changes.")

salary_file = str(Path(__file__).with_name("nba_salaries.csv"))

team_a = st.selectbox("Team A", TEAM_CODES)
team_b = st.selectbox(
    "Team B",
    [team for team in TEAM_CODES if team != team_a],
)

try:
    roster_a = load_roster(team_a, salary_file)
    roster_b = load_roster(team_b, salary_file)
except Exception as error:
    st.error(f"Could not load roster or salary data: {error}")
    st.stop()

players_a = st.multiselect(
    f"{team_a} players to trade",
    roster_a["player_name"].tolist(),
)

players_b = st.multiselect(
    f"{team_b} players to trade",
    roster_b["player_name"].tolist(),
)

comparison = build_team_a_salary_comparison(
    roster_a=roster_a,
    roster_b=roster_b,
    team_a_out=players_a,
    team_b_in=players_b,
)

totals = comparison.groupby("status", as_index=False)["salary"].sum()
before_total = float(totals.loc[totals["status"] == "Before trade", "salary"].sum())
after_total = float(totals.loc[totals["status"] == "After trade", "salary"].sum())

before_column, after_column, change_column = st.columns(3)
before_column.metric("Before trade", format_salary(before_total))
after_column.metric("After trade", format_salary(after_total))
change_column.metric("Change", format_salary(after_total - before_total), delta=after_total - before_total)

st.subheader(f"{team_a} salary visual")
chart_data = totals.set_index("status").rename(columns={"salary": "Total salary"})
st.bar_chart(chart_data.reindex(["After trade", "Before trade"]), y="Total salary", x_label="", y_label="Salary ($)", sort = "-Total salary")

st.subheader("Team A roster salaries")
display_data = comparison[["status", "player_name", "salary_millions"]].rename(
    columns={
        "status": "View",
        "player_name": "Player",
        "salary_millions": "Salary ($M)",
    }
)
st.dataframe(
    display_data,
    hide_index=True,
    width="stretch",
    column_config={"Salary ($M)": st.column_config.NumberColumn(format="$%.1fM")},
)