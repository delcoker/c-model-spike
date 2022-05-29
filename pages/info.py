import streamlit as st
import _dependency_container


def app():
    # constants
    page_name = 'Info'

    st.title(page_name)
    st.write(f'This is the `{page_name}` page of this app')
    st.write("Let's get your details")
    st.write(f"Current year is {_dependency_container.current_year}")

    with st.form(key='my_form'):
        industry_select = _dependency_container.get_pick_lists()[0]

        submit_button = st.form_submit_button(label='Save my Info')

    if submit_button:
        st.error("This is actually not being saved. `🐱Just for keche!©️`")
