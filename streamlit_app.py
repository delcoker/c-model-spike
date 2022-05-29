import streamlit as st
from mulitapp import MultiApp
from pages import login, data, linear_model, prophet_model, c_model, info
import _dependency_container

var1 = st.empty()
var2 = st.empty()

var1.title("Login")
var2.write('This is the `Login page`')

if not _dependency_container.logged_in:
    _dependency_container.logged_in = login.app()

if _dependency_container.logged_in:
    var1.empty()
    var2.empty()
    app = MultiApp()

    st.markdown('''C-Model''')

    app.add_app("Data", data.app)
    app.add_app("Info", info.app)
    app.add_app("Linear Regression Model", linear_model.app)
    # app.add_app("Prophet", prophet_model.app)
    app.add_app("C-Model", c_model.app)

    app.run()
