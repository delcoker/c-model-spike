import pandas as pd
import streamlit as st

from google.oauth2 import service_account
from gsheetsdb import connect


def get_raw_data():
    # # Create a connection object.
    # credentials = service_account.Credentials.from_service_account_info(
    #     st.secrets["gcp_service_account"],
    #     scopes=[
    #         "https://www.googleapis.com/auth/spreadsheets",
    #     ],
    # )
    # conn = connect(credentials=credentials)

    conn = connect()

    # Perform SQL query on the Google Sheet.
    # Uses st.cache to only rerun when the query changes or after 10 min.
    @st.cache(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        # rows = rows.fetchall()
        return rows

    picklist_sheet = st.secrets["public_gsheets_url"]["raw_data_sheet"]

    rows = run_query(f'SELECT * FROM "{picklist_sheet}"')

    # Print results.
    # for header in headers:
    for row in rows:
        # print(f"{row.name} has a :{row.pet}:")
        print(row)

    return pd.DataFrame(rows)


print(get_raw_data().head())
