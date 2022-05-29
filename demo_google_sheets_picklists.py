import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st

from google.oauth2 import service_account
from gsheetsdb import connect

# import industries from picklist_values

from google_sheets_picklist_values import get_pick_lists  # industries, revenue_models, currencies, data_sources, time_periods, time, groups

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


demo_sheet = st.secrets["public_gsheets_url"]["Sheet1"]

rows = run_query(f'SELECT * FROM "{demo_sheet}"')


# print(rows)

# Print results.
# for row in rows:
#     st.write(f"{row.name} has a :{row.pet}:")
#     print(f"{row.name} has a :{row.pet}:")

# client_data = pd.read_excel("CMODEL NEW TEST.xlsx", sheet_name="Sheet8")
# client_data.head()

# revenue_models, currencies, data_sources, time_periods, time, groups

# def get_pick_lists():
#     industries = get_pick_list_values()[0]
#     revenue_models = get_pick_list_values()[1]
#     currencies = get_pick_list_values()[2]
#     data_sources = get_pick_list_values()[3]
#     # time_periods = get_pick_list_values()[4]
#
#     industry_select = st.selectbox("Choose Industry", industries)
#     revenue_models_select = st.multiselect("revenue_models", revenue_models, default=[revenue_models[0]])
#     currencies_select = st.multiselect("currencies", currencies, default=[currencies[0]])
#     data_sources_select = st.multiselect("data_sources", data_sources, default=[data_sources[0]])
#     # time_periods_select = st.multiselect("time_periods", time_periods, default=[time_periods[0]])
#     # time_select = st.multiselect("time", time, default=[time[0]])
#     # groups_select = st.multiselect("groups", groups, default=[groups[0]])
#
#     return industry_select, revenue_models_select, currencies_select, data_sources_select
