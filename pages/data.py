import streamlit as st
import altair as alt
import _dependency_container


def app():
    # constants
    page_name = 'Data'

    st.title(page_name)
    st.write(f'This is the `{page_name}` page of this app')
    st.write("Let's load up your data")
    st.write(f"Current year is {_dependency_container.current_year}")

    st.write(_dependency_container.client_data)

    summed_data = _dependency_container.select_product("Product 1")[0]

    st.write(summed_data)

    c = alt.Chart(summed_data[['Close Month', 'ARR']]) \
        .mark_line() \
        .encode(x='Close Month', y='ARR', tooltip=['Close Month', 'ARR'])

    st.altair_chart(c, use_container_width=True)

    # fig, ax = plt.subplots()
    # ax.hist(_dependency_container.summed_data[['time', 'ARR']])
    # st.line_chart(_dependency_container.summed_data[['time', 'ARR']])
