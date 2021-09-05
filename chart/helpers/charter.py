from abc import ABC, abstractmethod
from pathlib import Path

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


SQL_DIR = Path(Path(__file__).parents[2].resolve(), "sql")
GBQ_CREDENTIALS = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
GBQ_CLIENT = bigquery.Client(credentials=GBQ_CREDENTIALS)


class Charter(ABC):
    def __init__(self, file):
        self.sql_path = Path(SQL_DIR, file)

    @st.cache(ttl=60 * 60 * 6)
    def get_df(self):
        sql = self.sql_path.read_text()
        df = GBQ_CLIENT.query(sql).result().to_dataframe()
        return df

    @abstractmethod
    def get_chart(self, df, *args, **kwargs):
        raise NotImplementedError

    def __call__(self):
        df = self.get_df()
        self.get_chart(df)
