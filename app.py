import streamlit as st

from chart.all_time_standings import AllTimeStandings
from chart.scoring_box_plots import ScoringBoxPlots
from chart.draft_pick_player_positions import DraftPickPlayerPositions
from chart.top_single_week_scores import TopSingleWeekScores

PAGE_TITLE = "\U0001F3C6 TCCC Fantasy Football \U0001F3C8"
CHARTS = {
    "Welcome": {},
    "All Time Standings": {
        "class": AllTimeStandings,
        "sql": "all_time_standings.sql",
        "args": [],
        "kwargs": {},
    },
    "Scoring Box Plots": {
        "class": ScoringBoxPlots,
        "sql": "matchups_h2h.sql",
        "args": [],
        "kwargs": {},
    },
    "Draft Pick Player Positions": {
        "class": DraftPickPlayerPositions,
        "sql": "draft_pick_player_positions.sql",
        "args": [],
        "kwargs": {},
    },
    "Top Single Week Scores": {
        "class": TopSingleWeekScores,
        "sql": "top_single_week_scores.sql",
        "args": [],
        "kwargs": {},
    },
}


def run():
    st.set_page_config(
        page_title=PAGE_TITLE,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title(PAGE_TITLE)
    st.sidebar.header(PAGE_TITLE)
    chart_name = st.sidebar.radio("Select a page:", CHARTS, 0)
    if chart_name == "Welcome":
        st.write(
            """Welcome to the statistics site of TCCC Fantasy Football!"""
            """\n\nChoose a page in the left sidebar."""
            """\n\nUse the ">" symbol in the upper left corner to expand the"""
            """ sidebar if it is not visible."""
        )
    else:
        chart_dict = CHARTS[chart_name]
        class_instance = chart_dict["class"](chart_dict["sql"])
        df = class_instance.get_df()
        class_instance.get_chart(
            df, *chart_dict["args"], **chart_dict["kwargs"]
        )


if __name__ == "__main__":
    run()
