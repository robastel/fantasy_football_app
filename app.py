from pathlib import Path

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from plotly.colors import qualitative
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from utils import constants

PAGE_TITLE = "TCCC \U0001F984 \U0001F3C8 \U0001F3C6"
TAB_NAMES = ["Standings", "Scoring", "Drafts"]
SCORING_SUB_TAB_NAMES = ["Scoring Dispersion", "Top Single Weeks"]
DRAFT_SUB_TAB_NAMES = [
    "Positions Drafted By Round",
    "Favorite Players \U0001F496",
]

gbq_credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
gbq_client = bigquery.Client(credentials=gbq_credentials)
sql_dir = Path(Path(__file__).parent, "sql")
sql_paths = list(sql_dir.iterdir())
dfs = dict()


@st.cache_data(ttl=21600)
def get_df(sql):
    df = gbq_client.query(sql).result().to_dataframe()
    return df


def get_all_dfs(paths):
    for p in paths:
        dfs[p.stem] = get_df(p.read_text())


st.set_page_config(
    page_title=PAGE_TITLE,
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title(PAGE_TITLE)
standings, scoring, drafts = st.tabs(TAB_NAMES)
get_all_dfs(sql_paths)

with standings:
    # ALL TIME STANDINGS
    dfs["all_time_standings"]["regular_season_win_rate"] = (
        100 * dfs["all_time_standings"]["regular_season_win_rate"]
    )
    dfs["all_time_standings"] = dfs["all_time_standings"].set_index(
        "manager_initials"
    )
    dfs["all_time_standings"] = dfs["all_time_standings"].style.text_gradient(
        cmap="summer_r",
        low=0.15,
        high=0.3,
        axis=0,
    )
    dfs["all_time_standings"] = dfs["all_time_standings"].format(
        formatter="{:.1f}%", subset="regular_season_win_rate"
    )
    st.dataframe(
        dfs["all_time_standings"],
        height=493,
        use_container_width=True,
        column_config={
            "manager_initials": st.column_config.Column(
                label="Mgr",
                help="Manager initials",
            ),
            "first_place_count": st.column_config.Column(
                label="1st\U0001F947",
                help="1st place finishes",
            ),
            "second_place_count": st.column_config.Column(
                label="2nd\U0001F948",
                help="2nd place finishes",
            ),
            "third_place_count": st.column_config.Column(
                label="3rd\U0001F949",
                help="3rd place finishes",
            ),
            "made_playoffs_count": st.column_config.Column(
                label="Playoffs",
                help="Number of seasons reaching the playoffs",
            ),
            "league_rating": st.column_config.Column(
                label="TCCCR", help="\U0001F643"
            ),
            "regular_season_win_rate": st.column_config.Column(
                label="RSW%",
                help="Regular season win percentage",
            ),
            "regular_season_first_place_count": st.column_config.Column(
                label="RS1",
                help="Regular season 1st place finishes",
            ),
            "regular_season_most_points_count": st.column_config.Column(
                label="RSP",
                help="Number of regular seasons with the most total points",
            ),
            "regular_season_single_week_most_points_count": st.column_config.Column(
                label="RSSW",
                help="Number of regular seasons with the highest single week score",
            ),
            "season_count": st.column_config.Column(
                label="Seasons",
                help="Number of seasons participated in",
            ),
        },
    )
    st.write("Note: Hover over column labels for descriptions.")

with scoring:
    dispersion, top_weeks = st.tabs(SCORING_SUB_TAB_NAMES)
    # SCORING DISPERSION
    with dispersion:
        manager_medians = (
            dfs["matchups_h2h"]
            .groupby("manager_initials")["points"]
            .median()
            .sort_values()
        )
        managers = manager_medians.index
        normalized_medians = mcolors.Normalize(
            vmin=manager_medians.min() * 0.99,
            vmax=manager_medians.max(),
        )
        color_map = plt.cm.get_cmap("summer_r")
        fig = go.Figure()
        for manager, median in zip(managers, manager_medians):
            fig.add_trace(
                go.Box(
                    x=dfs["matchups_h2h"][
                        dfs["matchups_h2h"]["manager_initials"] == manager
                    ]["points"],
                    name=manager,
                    orientation="h",
                    line_color=(
                        f"rgba{str(color_map(normalized_medians(median)))}"
                    ),
                    boxpoints=False,
                    fillcolor="rgba(0, 0, 0, 0)",
                )
            )
        fig.update_layout(
            **constants.PLOTLY_DEFAULT_LAYOUT_KWARGS,
            title_text="All Time Scoring Dispersion",
            xaxis_title_text="Weekly Points Scored",
            xaxis_showgrid=True,
            xaxis_tickvals=list(range(0, 301, 20)),
            xaxis_zeroline=False,
            yaxis_title_text="Manager",
            yaxis_showgrid=False,
            showlegend=False,
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )
        st.write(
            "How to read this box-and-whiskers plot:"
            "\n\nEach manager has a boxplot consisting of 5 values."
            "\n - The leftmost tick represents the manager's least number of"
            " points ever scored in a week."
            "\n - The left side of the box represents the manager's 25th"
            " percentile score. Roughly 25% of the manager's all time scores"
            " fall below this score (meaning roughly 75% are greater than this"
            " score)."
            "\n - The line within the box represents the manager's median"
            " score. Roughly 50% of the manager's all time scores fall on"
            " either side of this score."
            "\n - The right side of the box represents the manager's 75th"
            " percentile score. Roughly 75% of the manager's all time scores"
            " fall below this score (meaning roughly 25% are greater than this"
            " score)."
            "\n - The rightmost tick represents the manager's greatest number"
            " of points ever scored in a week."
        )

    # TOP SINGLE WEEK SCORES
    with top_weeks:
        dfs["top_single_week_scores"]["z-score"] = stats.zscore(
            dfs["top_single_week_scores"]["points"]
        )
        dfs["top_single_week_scores"]["approx_odds"] = (
            1 / (1 - stats.norm.cdf(dfs["top_single_week_scores"]["z-score"]))
        ) / dfs["top_single_week_scores"]["avg_matchups_per_season"]
        dfs["top_single_week_scores"]["approx_odds"] = dfs[
            "top_single_week_scores"
        ]["approx_odds"].apply(
            lambda x: (
                f"Once per {round(x, 2)} seasons"
                if x > 1
                else f"{round(1 / x, 2)} times per season"
            )
        )
        dfs["top_single_week_scores"].columns = [
            "Rank",
            "Manager",
            "Week",
            "Points",
            "Avg Matchups Per Season",
            "Z-score",
            "Expected Frequency",
        ]
        st.dataframe(
            dfs["top_single_week_scores"]
            .drop(["Avg Matchups Per Season", "Z-score"], axis=1)
            .head(100),
            hide_index=True,
            use_container_width=True,
            height=735,
        )

with drafts:
    positions, favorites = st.tabs(DRAFT_SUB_TAB_NAMES)
    with positions:
        # DRAFT PICK PLAYER POSITIONS
        dfs["draft_pick_player_positions"] = dfs[
            "draft_pick_player_positions"
        ].sort_values(["manager_initials", "round_num"])
        dfs["draft_pick_player_positions"] = dfs[
            "draft_pick_player_positions"
        ].set_index("manager_initials")
        all_managers_name = "All Managers"
        manager = st.selectbox(
            "Choose a manager:",
            [all_managers_name]
            + list(np.sort(dfs["draft_pick_player_positions"].index.unique())),
            0,
        )
        df_all_managers = (
            dfs["draft_pick_player_positions"].groupby("round_num").sum()
        )
        df_all_managers = df_all_managers.reset_index()
        df_all_managers.index = [all_managers_name] * len(df_all_managers)
        df_combined = pd.concat(
            [dfs["draft_pick_player_positions"], df_all_managers]
        )
        round_nums = np.sort(
            dfs["draft_pick_player_positions"]["round_num"].unique()
        )
        player_positions = (
            dfs["draft_pick_player_positions"]
            .drop("round_num", axis=1)
            .columns
        )
        df_pos = df_combined[player_positions]
        df_pos = 100 * df_pos.div(df_pos.sum(axis=1), axis=0)
        fig = go.Figure()
        colors = qualitative.Vivid
        for i, pos in enumerate(player_positions):
            fig.add_trace(
                go.Bar(
                    x=round_nums,
                    y=df_pos.loc[manager, pos],
                    name=pos.upper(),
                    marker_color=colors[i],
                )
            )
        fig.update_layout(
            **constants.PLOTLY_DEFAULT_LAYOUT_KWARGS,
            barmode="relative",
            title_text="Positions Drafted by Round",
            xaxis_title_text="Draft Round",
            xaxis_type="category",
            yaxis_title_text="Share of Draft Picks",
            yaxis_range=[0, 100],
            yaxis_ticksuffix="%",
            legend_orientation="h",
            legend_y=-0.2,
            legend_x=0.5,
            legend_xanchor="center",
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )

    # FAVORITE PLAYERS
    with favorites:
        st.dataframe(
            dfs["favorite_players"],
            use_container_width=True,
            hide_index=True,
            height=422,
            column_config={
                "manager_initials": st.column_config.Column(
                    label="Manager",
                    help="Manager Initials",
                ),
                "favorite_players": st.column_config.Column(
                    label=(
                        "Favorite Players (# of Seasons Drafted [3 seasons"
                        " minimum])"
                    ),
                    help=(
                        "Names of most drafted players by team with the number"
                        " of season drafted in parentheses"
                    ),
                ),
            },
        )
