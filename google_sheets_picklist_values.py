import streamlit as st

from google.oauth2 import service_account
from gsheetsdb import connect


def get_pick_lists():
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

    picklist_sheet = st.secrets["public_gsheets_url"]["Picklist_Values"]

    rows = run_query(f'SELECT * FROM "{picklist_sheet}"')

    # print(rows)
    headers = ["Industry Sector (Picklist Values)", "Revenue Model (Picklist)", "Currency (Picklist)", "Data Sources (Picklist)", "EM1 View Results - Time Period (Picklist)",
               "EM1 View Results - Time", "EM1 View Results - Groups - (Picklist)"]

    industries = []
    revenue_models = []
    currencies = []
    data_sources = []
    time_periods = []
    time = []
    groups = []

    # Print results.
    # for header in headers:
    for row in rows:
        # print(f"{row.name} has a :{row.pet}:")
        industries.append(f"{row[0]}") if row[0] is not None else []
        revenue_models.append(row[1]) if row[1] is not None else []
        currencies.append(row[2]) if row[2] is not None else []
        data_sources.append(row[3]) if row[3] is not None else []
        time_periods.append(row[4]) if row[4] is not None else []
        time.append(row[5]) if row[5] is not None else []
        groups.append(row[6]) if row[6] is not None else []

    # picklist_values = [industries, revenue_models, currencies, data_sources, time_periods, time, groups]

    industry_select = st.selectbox("Choose Industry", industries)
    revenue_models_select = st.multiselect("Revenue Models", revenue_models, default=[revenue_models[0]])
    currencies_select = st.selectbox("Currency", currencies)
    data_sources_select = st.selectbox("Data Sources", data_sources)
    # time_periods_select = st.multiselect("time_periods", time_periods, default=[time_periods[0]])
    # time_select = st.multiselect("time", time, default=[time[0]])
    # groups_select = st.multiselect("groups", groups, default=[groups[0]])

    return industry_select, revenue_models_select, currencies_select, data_sources_select
