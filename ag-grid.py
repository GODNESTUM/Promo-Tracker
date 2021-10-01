import string

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

st.set_page_config(layout='wide')


def display_table(df: pd.DataFrame) -> AgGrid:
    # Configure AgGrid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode = 'single', use_checkbox=True,rowMultiSelectWithClick=True)
    
    # Custom JS code for interactive rows deletion
    # For credits SEE: 
    # https://github.com/PablocFonseca/streamlit-aggrid/blob/1acb526ba43b5aac9c8eb22cc54eeb05696cd84d/examples/example_highlight_change.py#L21
    # https://ag-grid.zendesk.com/hc/en-us/articles/360020160932-Removing-selected-rows-or-cells-when-Backspace-or-Delete-is-pressed
    js = JsCode("""
    function(e) {
        let api = e.api;        
        let sel = api.getSelectedRows();
        
        api.applyTransaction({remove: sel});
    };
    """)
    gb.configure_grid_options(onRowSelected=js) 
    return AgGrid(
        df,
        gridOptions=gb.build(),
        # this override the default VALUE_CHANGED
        update_mode=GridUpdateMode.MODEL_CHANGED,
        # needed for js injection
        allow_unsafe_jscode=True
# Define dummy data
rng = np.random.default_rng(2021)
N_SAMPLES = 100
N_FEATURES = 10
df = pd.DataFrame(rng.integers(0, N_SAMPLES, size=(
    N_SAMPLES, N_FEATURES)), columns=list(string.ascii_uppercase[:N_FEATURES]))

st.info("Select a row to remove it")
response = display_table(df)
st.write(response)
st.write(f"Dataframe shape: {response['data'].shape}")



