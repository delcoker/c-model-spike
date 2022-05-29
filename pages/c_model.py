import streamlit as st

import _dependency_container


def app():
    # constants
    page_name = 'C-Model'

    st.title(page_name)
    st.write(f'This is the `{page_name}` page of this app')

    with st.form(key='my_form'):
        _dependency_container.selected_product = st.selectbox("Choose Product", _dependency_container.products)
        _dependency_container.desired_growth = st.slider(label='Growth Amount', min_value=0, max_value=9999999)

        submit_button = st.form_submit_button(label='Run the Model')

    if submit_button:
        st.write(_dependency_container.run_c_model(_dependency_container.selected_product))
