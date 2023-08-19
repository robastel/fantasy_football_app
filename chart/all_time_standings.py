import streamlit as st

import pandas as pd

from chart.helpers.charter import Charter


class AllTimeStandings(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc.columns = [
            "Manager",
            "1st\U0001F947",
            "2nd\U0001F948",
            "3rd\U0001F949",
            "Playoffs",
            "TCCCR",
            "RSW%",
            "RS1",
            "RSPts",
            "RSTopWeek",
            "Seasons",
        ]
        dfc["RSW%"] = 100 * dfc["RSW%"]
        dfc = dfc.set_index("Manager")
        dfc = dfc.style.text_gradient(cmap="summer_r", low=.15, high=.3, axis=0)
        dfc = dfc.format(formatter="{:.1f}%", subset='RSW%')
        st.dataframe(dfc, height=493, use_container_width=True)
