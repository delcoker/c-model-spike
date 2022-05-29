import streamlit as st

var1 = st.empty()


def app():
    with var1.form(key='login'):
        username = st.text_input("username")
        password = st.text_input("password", type='password')
        submit_button = st.form_submit_button(label="Log In")

    if submit_button and password == 'del':
        st.success(f"Welcome {username}")
        var1.empty()

        return True
    else:

        return False
