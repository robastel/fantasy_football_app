import streamlit as st
from scipy import stats

from chart.helpers.charter import Charter


class TopSingleWeekScores(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc['z-score'] = stats.zscore(dfc['points'])
        dfc['approx_odds'] = (1 / (1 - stats.norm.cdf(dfc['z-score'])))
        dfc['approx_odds'] = '1 in ' + dfc['approx_odds'].astype(int).astype(str)
        dfc.columns = [
            "Rank",
            "Manager",
            "Year",
            "Week",
            "Points",
            "Z-score",
            "Approximate Odds",
        ]
        st.dataframe(
            dfc.head(100),
            hide_index=True,
            use_container_width=True,
            height=735
        )
