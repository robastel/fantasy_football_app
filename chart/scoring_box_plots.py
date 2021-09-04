import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from chart.helpers.charter import Charter
from chart.helpers import constants

class ScoringBoxPlots(Charter):
    def get_chart(self, df, *args, **kwargs):
        manager_medians = (
            df.groupby("manager_initials")["points"].median().sort_values()
        )
        managers = manager_medians.index
        normalized_medians = mcolors.Normalize(
            vmin=manager_medians.min(),
            vmax=manager_medians.max(),
        )
        color_map = plt.cm.get_cmap("RdYlGn")
        fig = go.Figure()
        for manager, median in zip(managers, manager_medians):
            fig.add_trace(
                go.Box(
                    x=df[df["manager_initials"] == manager]["points"],
                    name=manager,
                    orientation=kwargs.get("orientation", "h"),
                    line_color=f"rgba{str(color_map(normalized_medians(median)))}",
                    boxpoints=False,
                    fillcolor="rgba(0, 0, 0, 0)",
                )
            )
        fig.update_layout(
            **constants.PLOTLY_DEFAULT_LAYOUT_KWARGS,
            title_text="All Time Scoring",
            xaxis_title_text="Weekly Points Scored",
            xaxis_showgrid=True,
            xaxis_tickvals=list(range(0,301,20)),
            xaxis_zeroline=False,
            yaxis_title_text="Manager",
            yaxis_showgrid=False,
            showlegend=False,
        )
        st.plotly_chart(
            fig, use_container_width=True, config={'displayModeBar': False}
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
