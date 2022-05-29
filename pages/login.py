from datetime import datetime
import random

import pandas as pd
import pygsheets
import streamlit as st

# authorization
gc = pygsheets.authorize(service_file='C:/Users/delco/Downloads/c-model-test-d0c7fbbcfbff.json')

# Create empty dataframe
df = pd.DataFrame()

x = random.randint(1, 18)
y = random.randint(1, 33)


var1 = st.empty()


def app():
    with var1.form(key='login'):
        username = st.text_input("username")
        password = st.text_input("password", type='password')
        submit_button = st.form_submit_button(label="Log In")

    if submit_button and password == 'del':
        st.success(f"Welcome {username}")

        # Create a column
        df['name'] = [username + "->" + str(datetime.now())]

        # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
        sh = gc.open('spike-test')

        # select the first sheet
        wks = sh[0]

        # update the first sheet with df, starting at cell B2.
        wks.set_dataframe(df, (y, x))

        var1.empty()

        return True
    else:

        return False
