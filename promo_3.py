import streamlit as st
import pandas as pd

def show_table(data):
    st.title('Promo DB')
    #st.write (st.session_state)
    st.dataframe(data)
    print (type(data))


# df['date'] = pd.to_datetime(df['date'])
# df = df.style.format({'date': lambda x: "{}".format(x.strftime('%m/%d/%Y %H:%M:%S'))}).set_table_styles('styles')
# st.dataframe(df)