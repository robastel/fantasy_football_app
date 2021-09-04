import streamlit as st

from chart.helpers.charter import Charter
from chart.helpers import constants

class AllTimeStandings(Charter):
    def get_chart(self, df, *args, **kwargs):
        df.columns = [
            "Manager",
            "\U0001F947",
            "\U0001F948",
            "\U0001F949",
            "Made Playoffs",
            "Reg. Season Win %",
            "Seasons Played",
        ]
        df = df.astype(str)
        df = df.replace("0", "")
        df = df.set_index("Manager")
        df = df.style.set_table_styles(
            constants.INCREASE_TABLE_FONT_SIZE
            + constants.CENTER_ALIGN_TABLE_TEXT
            + [
                {
                    "selector": f"thead tr th:nth-of-type({n})",
                    "props": [
                        ("font-size", "3em"),
                    ],
                }
                for n in range(2, 5)
            ]
        )
        st.table(df)
