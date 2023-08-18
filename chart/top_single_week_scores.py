import streamlit as st
from scipy import stats

from chart.helpers.charter import Charter


class TopSingleWeekScores(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc['z-score'] = stats.zscore(dfc['points'])
        dfc['approx_odds'] = (
            (1 / (1 - stats.norm.cdf(dfc['z-score'])))
            / dfc['avg_matchups_per_season']
        )
        dfc['approx_odds'] = dfc['approx_odds'].apply(
                lambda x: (
                    f'Once every {round(x, 2)} seasons' if x > 1
                    else f'{round(1 / x, 2)} times per season'
                )
        )
        dfc.columns = [
            "Rank",
            "Manager",
            "Year",
            "Week",
            "Points",
            "Avg Matchups Per Season",
            "Z-score",
            "League-wide expected frequency of achieving this score or higher",
        ]
        st.dataframe(
            dfc.drop(['Avg Matchups Per Season', 'Z-score'], axis=1).head(100),
            hide_index=True,
            use_container_width=True,
            height=735
        )
