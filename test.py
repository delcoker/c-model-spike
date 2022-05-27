import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st

from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)


# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["Sheet8"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")

client_data = pd.read_excel("CMODEL NEW TEST.xlsx", sheet_name="Sheet8")
client_data.head()

industry_list = ["Finance", "Tech"]
# [x for x in range(0, len(industry_list))],
industries = st.multiselect("Choose Industries", industry_list, default=["Tech"])
# !streamlit run /usr/local/lib/python3.7/dist-packages/ipykernel_launcher.py [ARGUMENTS]
