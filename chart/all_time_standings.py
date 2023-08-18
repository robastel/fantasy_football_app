import streamlit as st

import pandas as pd

from chart.helpers.charter import Charter


class AllTimeStandings(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc.columns = [
            "Manager",
            "1st \U0001F947",
            "2nd \U0001F948",
            "3rd \U0001F949",
            "Playoffs",
            "TCCC Rating",
            "RS Win %",
            "RS 1st",
            "RS Points",
            "RS High Week",
            "Seasons",
        ]
        dfc["RS Win %"] = 100 * dfc["RS Win %"]
        dfc = dfc.set_index("Manager")
        dfc = dfc.style.text_gradient(cmap="summer_r", low=.15, high=.15, axis=0)
        dfc = dfc.format(formatter="{:.1f}%", subset='RS Win %')
        st.dataframe(dfc, height=493, use_container_width=True)
        st.write('*RS = Regular Season')
