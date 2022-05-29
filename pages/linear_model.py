import streamlit as st

import _dependency_container


def app():
    # constants
    page_name = 'Linear Model'

    st.title(page_name)
    st.write(f'This is the `{page_name}` page of this app. For the next 6 months.')

    product = "Product 1"
    summed_data = _dependency_container.select_product(product)[0]

    linear_predictions = _dependency_container.run_linear_regression(product, summed_data)

    st.write(linear_predictions)
