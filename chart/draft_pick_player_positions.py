import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from chart.helpers.charter import Charter
from chart.helpers import constants

class DraftPickPlayerPositions(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc = dfc.sort_values(['manager_initials', 'round_num'])
        dfc = dfc.set_index("manager_initials")
        all_managers_name = "All Managers"
        manager = st.selectbox(
            "Choose a manager:",
            [all_managers_name] + list(np.sort(dfc.index.unique())),
            0,
        )
        df_all_managers = dfc.groupby("round_num").sum()
        df_all_managers = df_all_managers.reset_index()
        df_all_managers.index = [all_managers_name] * len(df_all_managers)
        df_combined = pd.concat([dfc, df_all_managers])
        round_nums = np.sort(dfc["round_num"].unique())
        player_positions = dfc.drop("round_num", axis=1).columns
        df_pos = df_combined[player_positions]
        df_pos = 100 * df_pos.div(df_pos.sum(axis=1), axis=0)
        fig = go.Figure()
        for pos in player_positions:
            fig.add_trace(
                go.Bar(
                    x=round_nums,
                    y=df_pos.loc[manager, pos],
                    name=pos.upper(),
                )
            )
        fig.update_layout(
            **constants.PLOTLY_DEFAULT_LAYOUT_KWARGS,
            barmode="relative",
            title_text="Draft Pick Player Position by Round",
            xaxis_title_text="Draft Round",
            xaxis_type="category",
            yaxis_title_text="Share of Draft Picks",
            yaxis_range=[0, 100],
            yaxis_ticksuffix="%",
            legend_orientation="h",
            legend_y=-0.2,
            legend_x=0.5,
            legend_xanchor='center',
        )
        st.plotly_chart(
            fig, use_container_width=True, config={'displayModeBar': False}
        )
