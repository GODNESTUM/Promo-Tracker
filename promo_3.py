import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

def app(data, data_whs):
    df_template = pd.DataFrame(
        '',
        index=range(10),
        columns=list('abcde')
    )

    with st.form('example form') as f:
        st.header('Example Form')
        response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
        st.form_submit_button()

    st.write(response['data'])  

# def app(data):
#     st.title('Promo DB')
#     #st.write (st.session_state)
#     st.dataframe(data)
#     print (type(data))


# df['date'] = pd.to_datetime(df['date'])
# df = df.style.format({'date': lambda x: "{}".format(x.strftime('%m/%d/%Y %H:%M:%S'))}).set_table_styles('styles')
# st.dataframe(df)