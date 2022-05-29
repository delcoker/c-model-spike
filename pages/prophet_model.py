import streamlit as st
import altair as alt
import _dependency_container


def app():
    # constants
    page_name = 'C-Model'

    st.title(page_name)
    st.write(f'This is the `{page_name}` page of this app')
    st.write("Let's model your data")

    # # summarize the forecast
    # st.write(_dependency_container.forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    #
    # # plot forecast
    # c = alt.Chart(_dependency_container.forecast) \
    #     .mark_line() \
    #     .encode(x='ds', y='y', tooltip=['ds', 'y'])
    #
    # st.altair_chart(c, use_container_width=True)
