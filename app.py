import altair as alt
import pandas as pd
import streamlit as st
from pathlib import Path

from nba_trade_simulator.data import build_roster_with_stats
from nba_trade_simulator.data import fetch_player_shot_locations
from nba_trade_simulator.salary import load_salary_data
from nba_trade_simulator.simulator import (
    aggregate_shot_attempts_by_status,
    build_team_a_salary_comparison,
)

TEAM_CODES = ["ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET",
              "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN",
              "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS",
              "TOR", "UTA", "WAS"]
LAST_COMPLETED_SEASON = "2025-26"


@st.cache_data(ttl=3600)
def load_roster(team_code: str, salary_file: str):
    roster = build_roster_with_stats(team_code, season=LAST_COMPLETED_SEASON)
    salaries = load_salary_data(salary_file)
    return roster.merge(salaries[["player_name", "salary"]], how="left", on="player_name")


@st.cache_data(ttl=86400)
def load_shot_locations(season: str):
    return fetch_player_shot_locations(season)


def format_salary(value: float) -> str:
    return f"${value / 1_000_000:,.1f}M"


def clear_team_a_players() -> None:
    st.session_state["players_a"] = []


def clear_team_b_players() -> None:
    st.session_state["players_b"] = []


def swap_teams() -> None:
    st.session_state["team_a"], st.session_state["team_b"] = (
        st.session_state["team_b"],
        st.session_state["team_a"],
    )
    st.session_state["players_a"], st.session_state["players_b"] = (
        st.session_state["players_b"],
        st.session_state["players_a"],
    )


st.set_page_config(page_title="NBA Trade Simulator", layout="wide")
st.title("NBA Roster Simulator")
st.caption("Build a trade package to see how the roster salary changes.")

salary_file = str(Path(__file__).with_name("nba_salaries.csv"))

st.session_state.setdefault("team_a", TEAM_CODES[0])
st.session_state.setdefault("team_b", TEAM_CODES[1])
st.session_state.setdefault("players_a", [])
st.session_state.setdefault("players_b", [])
if st.session_state["team_b"] == st.session_state["team_a"]:
    st.session_state["team_b"] = next(
        team for team in TEAM_CODES if team != st.session_state["team_a"]
    )
    st.session_state["players_b"] = []

team_a_column, swap_column, team_b_column = st.columns(
    [5, 2, 5],
    vertical_alignment="bottom",
)
with team_a_column:
    team_a = st.selectbox(
        "Team A",
        TEAM_CODES,
        key="team_a",
        on_change=clear_team_a_players,
    )
with swap_column:
    st.button(
        "Swap teams",
        icon=":material/swap_horiz:",
        on_click=swap_teams,
        width="stretch",
    )
with team_b_column:
    team_b = st.selectbox(
        "Team B",
        [team for team in TEAM_CODES if team != team_a],
        key="team_b",
        on_change=clear_team_b_players,
    )

try:
    roster_a = load_roster(team_a, salary_file)
    roster_b = load_roster(team_b, salary_file)
except Exception as error:
    st.error(f"Could not load roster or salary data: {error}")
    st.stop()

try:
    player_shot_locations = load_shot_locations(LAST_COMPLETED_SEASON)
except Exception as error:
    st.error(f"Could not load {LAST_COMPLETED_SEASON} shot-location data: {error}")
    st.stop()

players_a = st.multiselect(
    f"{team_a} players to trade",
    roster_a["player_name"].tolist(),
    key="players_a",
)

players_b = st.multiselect(
    f"{team_b} players to trade",
    roster_b["player_name"].tolist(),
    key="players_b",
)

comparison = build_team_a_salary_comparison(
    roster_a=roster_a,
    roster_b=roster_b,
    team_a_out=players_a,
    team_b_in=players_b,
)
shot_breakdown = aggregate_shot_attempts_by_status(
    comparison,
    player_shot_locations,
)

st.subheader(f"{team_a} roster salaries")
stack_data = comparison[["status", "player_name", "salary_millions"]].copy()
bar_chart = alt.Chart(stack_data).mark_bar().encode(
    x=alt.X(
        "status:N",
        title=None,
        sort=["Before trade", "After trade", " "],
    ),
    y=alt.Y(
        "salary_millions:Q",
        title="Salary ($M)",
        stack="zero",
        scale=alt.Scale(domain=[0, 250], nice=False),
        axis=alt.Axis(format="$,.0f", tickCount=11),
    ),
    color=alt.Color(
        "player_name:N",
        scale=alt.Scale(
            domain=sorted(set(roster_a["player_name"]).union(roster_b["player_name"])),
            scheme="observable10",
        ),
        legend=None,
    ),
    order=alt.Order("salary_millions:Q", sort="descending"),
    tooltip=[
        alt.Tooltip("status:N", title="Roster"),
        alt.Tooltip("player_name:N", title="Player"),
        alt.Tooltip("salary_millions:Q", title="Salary ($M)", format=",.3f"),
    ],
)
threshold_data = pd.DataFrame(
    [
        {
            "threshold": "Salary cap",
            "salary": 164.961,
            "label": "Salary cap  $164.961M",
            "status": " ",
        },
        {
            "threshold": "Luxury tax",
            "salary": 200.428,
            "label": "Luxury tax  $200.428M",
            "status": " ",
        },
        {
            "threshold": "First apron",
            "salary": 209.015,
            "label": "First apron  $209.015M",
            "status": " ",
        },
        {
            "threshold": "Second apron",
            "salary": 221.686,
            "label": "Second apron  $221.686M",
            "status": " ",
        },
    ]
)
threshold_colors = alt.Scale(
    domain=["Salary cap", "Luxury tax", "First apron", "Second apron"],
    range=["#2A91FF", "#FF9D3B", "#FF5959", "#FCB1E7"],
)
threshold_chart = alt.Chart(threshold_data).encode(
    y=alt.Y(
        "salary:Q",
        title="Salary ($M)",
        scale=alt.Scale(domain=[0, 250], nice=False),
        axis=alt.Axis(format="$,.0f", tickCount=11),
    ),
    color=alt.Color("threshold:N", scale=threshold_colors, legend=None),
)
threshold_lines = threshold_chart.mark_rule(strokeWidth=2, strokeDash=[4, 3]).encode(
    tooltip=[
        alt.Tooltip("threshold:N", title="Threshold"),
        alt.Tooltip("salary:Q", title="Salary ($M)", format=",.3f"),
    ],
)
threshold_labels = threshold_chart.mark_text(align="left", dx=6, dy=-6).encode(
    x=alt.X("status:N", title=None, sort=["Before trade", "After trade", " "]),
    text="label:N",
)
st.altair_chart(
    (bar_chart + threshold_lines + threshold_labels)
    .properties(height=1000)
    .resolve_scale(color="independent")
    .configure_view(stroke=None),
    width="stretch",
)

st.subheader(f"{LAST_COMPLETED_SEASON} shot breakdown")
shot_colors = alt.Scale(
    domain=[
        "Restricted area",
        "Paint",
        "Mid-range",
        "Corner three",
        "Above the break three",
    ],
    range=["#E69F00", "#56B4E9", "#009E73", "#D55E00", "#0072B2"],
)
before_shots, after_shots = st.columns(2)
for column, status in (
    (before_shots, "Before trade"),
    (after_shots, "After trade"),
):
    status_shots = shot_breakdown.loc[
        shot_breakdown["status"] == status
    ].copy()
    total_attempts = float(status_shots["attempts"].sum())
    with column:
        st.markdown(f"**{status}**")
        if total_attempts == 0:
            st.info(f"No {LAST_COMPLETED_SEASON} shot attempts are available.")
            continue
        pie_chart = (
            alt.Chart(status_shots)
            .mark_arc(outerRadius=120)
            .encode(
                theta=alt.Theta("attempts:Q", stack=True),
                color=alt.Color(
                    "shot_area:N",
                    title="Shot area",
                    scale=shot_colors,
                ),
                tooltip=[
                    alt.Tooltip("shot_area:N", title="Shot area"),
                    alt.Tooltip("attempts:Q", title="Attempts", format=","),
                    alt.Tooltip(
                        "proportion:Q",
                        title="Share of shots",
                        format=".1%",
                    ),
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(pie_chart, width="stretch")
