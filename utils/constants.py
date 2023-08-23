import streamlit as st

PLOTLY_DEFAULT_LAYOUT_KWARGS = {
    "title_x": 0.5,
    "title_xanchor": "center",
    "title_xref": "paper",
    "margin": {"l": 30, "r": 30, "t": 30, "b": 30},
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "font_color": st.get_option("theme.textColor"),
    # x axis
    "xaxis_title_font": {"size": 16},
    "xaxis_tickfont": {"size": 16},
    "xaxis_gridcolor": "rgb(128, 128, 128)",
    # y axis
    "yaxis_title_font": {"size": 16},
    "yaxis_tickfont": {"size": 16},
    "yaxis_gridcolor": "rgb(128, 128, 128)",
    # legend
    "legend_font_size": 16,
}
