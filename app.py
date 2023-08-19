import streamlit as st

from chart.all_time_standings import AllTimeStandings
from chart.scoring_box_plots import ScoringBoxPlots
from chart.draft_pick_player_positions import DraftPickPlayerPositions
from chart.top_single_week_scores import TopSingleWeekScores

PAGE_TITLE = "TCCC \U0001F984 \U0001F3C8 \U0001F3C6"
CHARTS = {
    "Standings": {
        "class": AllTimeStandings,
        "sql": "all_time_standings.sql",
        "args": [],
        "kwargs": {},
    },
    "Scoring": {
        "class": ScoringBoxPlots,
        "sql": "matchups_h2h.sql",
        "args": [],
        "kwargs": {},
    },
    "Draft": {
        "class": DraftPickPlayerPositions,
        "sql": "draft_pick_player_positions.sql",
        "args": [],
        "kwargs": {},
    },
    "Top Weeks": {
        "class": TopSingleWeekScores,
        "sql": "top_single_week_scores.sql",
        "args": [],
        "kwargs": {},
    },
}

st.set_page_config(
    page_title=PAGE_TITLE,
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title(PAGE_TITLE)
for tab_name, tab in zip(CHARTS.keys(), st.tabs(CHARTS.keys())):
    with tab:
        chart_dict = CHARTS[tab_name]
        class_instance = chart_dict["class"](chart_dict["sql"])
        df = class_instance.get_df()
        class_instance.get_chart(
            df, *chart_dict["args"], **chart_dict["kwargs"]
        )
