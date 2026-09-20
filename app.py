import streamlit as st

from nba_trade_simulator.data import build_roster_with_stats
from nba_trade_simulator.simulator import evaluate_trade

TEAM_CODES = ["ATL", "BOS", "BRK", "CHA", "CHI", "CLE", "DAL", "DEN", "DET",
              "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
              "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS",
              "TOR", "UTA", "WAS"]


@st.cache_data(ttl=3600)
def load_roster(team_code: str):
    roster = build_roster_with_stats(team_code)
    roster["salary"] = 0.0
    return roster


st.set_page_config(page_title="NBA Trade Simulator", layout="wide")
st.title("NBA Trade Simulator")

team_a = st.selectbox("Team A", TEAM_CODES)
team_b = st.selectbox(
    "Team B",
    [team for team in TEAM_CODES if team != team_a],
)

roster_a = load_roster(team_a)
roster_b = load_roster(team_b)

players_a = st.multiselect(
    f"{team_a} players to trade",
    roster_a["player_name"].tolist(),
)

players_b = st.multiselect(
    f"{team_b} players to trade",
    roster_b["player_name"].tolist(),
)

if st.button("Evaluate trade", type="primary"):
    report = evaluate_trade(
        team_a_name=team_a,
        team_b_name=team_b,
        team_a_out=players_a,
        team_b_out=players_b,
        roster_a=roster_a,
        roster_b=roster_b,
    )

    st.subheader("Trade result")
    st.json(report)