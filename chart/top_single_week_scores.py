import streamlit as st
import pandas as pd

from chart.helpers.charter import Charter
from chart.helpers import constants


class TopSingleWeekScores(Charter):
    def get_chart(self, df, *args, **kwargs):
        dfc = df.copy()
        dfc.columns = [
            "Manager",
            "Points",
            "Year",
            "Week",
        ]
        dfc["concat"] = dfc["Manager"] + dfc["Year"] + dfc["Week"]
        dfc = dfc.set_index("concat")
        dfc = pd.DataFrame(dfc["Points"]).style.set_table_styles(
            constants.CENTER_ALIGN_TABLE_TEXT
            + constants.INCREASE_TABLE_FONT_SIZE
        )
        st.table(dfc)
