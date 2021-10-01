
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, DataReturnMode
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

import streamlit as st
from datetime import datetime, timedelta

def app(promodb,dim_partner, dim_product,fact_basesrp):
    st.title("New Promo")
    st.subheader("Insert new Promo to the DataBase")
    st.markdown("On this page you can add new Promo campaign or relaunch the existing one. All inputs are stored in one Promo Database.")
    
    #Make a mask Filter for user and his platform
    session_values = [st.session_state.sb_user, st.session_state.sb_partner]
    df = promodb.query(quer(["added_by","partner_name"],session_values)).copy()
    
    cols = df.columns
    if "entry_promo" not in st.session_state:
        st.session_state.entry_promo = pd.DataFrame(columns=cols)
    if "add_result" not in st.session_state:
        st.session_state.add_result = pd.DataFrame(columns=cols)
    if "entry_number" not in st.session_state:
            st.session_state.entry_number = 0

    if st.session_state.copy_promo:
        promo_name = st.selectbox(
        f"Promo Type",
        #np.insert(df.promo_name.unique(),0,"")
        df.promo_name.unique()
        ,key = 'pn'
        )
        add_all_franchise = st.checkbox("Select all Franchise", key = 'copy_promo_all_fracnhise')
        add_all_titles = st.checkbox("Select all Titles", key = 'copy_promo_all_titles')

    col1,col2 = st.columns([10,10])
    col11,col22 = st.columns(2)
    timestamp = pd.Timestamp(datetime.now()).strftime("%d-%m-%Y")

    with col1:
        promo = st.text_input("Start typing Promo")
        if promo != "":           
            st.selectbox("Did you mean one of these Promo's?",typesearch(promo,df,"promo_name"))
            
        promo_name = st.selectbox(
        f"Promo Type",
        #np.insert(df.promo_name.unique(),0,"")
        df.promo_name.unique(),
        #,key = 'pn'
        )
        if st.session_state.sb_new:
            title_series = st.text_input(
            f"Start typing Franchise",
            #key = 'tsn'
            )
            title = st.text_input(
            f"Title Name",
            #key = 'ttn'
            )
        else:
            title_series = st.session_state.sb_ts
            add_all = st.checkbox("Add all Titles", value = False, help = "Add all Titles for this Franchise",key = "add_all")
            if st.session_state.add_all:
                title = sorted(df.title_name[df.ips_project_title.isin([st.session_state.sb_ts])].unique())
                with st.expander("Titles"):
                    st.write(title)
            else:
                title = st.multiselect(
                    f"title_name",
                    sorted(df.title_name[df.ips_project_title.isin([st.session_state.sb_ts])].unique()),
                    key = 'tt'
                )
            # title_series = st.selectbox(
            #     f"title_name Series",
            #     sorted(df.ips_project_title.unique()),
            #     key = 'ts'
            # )

    with col2:
        base_srp = st.number_input(df.columns[5],step = 10,value = 50, key = "p1_bs")         #automatic from source #later
        discount = st.number_input(df.columns[6]+"%",min_value = 0.,max_value = 100.,value = 75., key = "p1_dc",step = 0.1)
        currency = st.selectbox("Currency", options = ['€','$','¥'])
        #discount = st.number_input(df.columns[6],min_value = 0.,max_value = 100.,value = 75., key = "p1_dc",step = 0.1)
        dsrp = round(base_srp*discount/100,2)
        st.write("dsrp: ", dsrp)
        
    with col11:
        period_start = st.date_input(df.columns[8], key = 'period_start')
        submitted = st.button("Add Promo Entry")

    with col22:
        period_end = st.date_input(df.columns[9], key = 'period_end',value = st.session_state.period_start+timedelta(7))
        length = (st.session_state.period_end-st.session_state.period_start) #timedelta class
        st.write("Duration:",length.days)

    if submitted:        
        if type(title) is list:
            for title in title:
                st.session_state.entry_number +=1
                entries = st.session_state.entry_number, id,promo_name,title_series,title,st.session_state.sb_partner,str(base_srp)+currency,"{:.2f}%".format(discount),str(dsrp)+currency,period_start,period_end,length.days,st.session_state.sb_user
                st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
                st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])   
        else:
            st.session_state.entry_number +=1
            entries = st.session_state.entry_number,id,promo_name,title_series,title,st.session_state.sb_partner,str(base_srp)+currency,"{}%.2f%".format(discount),str(dsrp)+currency,period_start,period_end,length.days,st.session_state.sb_user
            st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
            st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])
        st.info("Click un Upload button to add to Promo's DB")

    #df.iloc[x,]
    #df.loc[df.index[0:5],["col1,col2"]]

    show_table =  st.session_state.add_result.rename(columns = {"ips_project_title":"Franchise"})
    show_cols_add_result = ["entry_number","promo_name","Franchise","title_name","Partner_Name","base_srp","discount","dsrp","period_start","period_end","Duration","Publisher","added_by"]

    st.table(show_table)

    # return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
    # return_mode_value = DataReturnMode.__members__[return_mode]

    # update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=6)
    # update_mode_value = GridUpdateMode.__members__[update_mode] 

    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(st.session_state.add_result)
    
    #customize gridOptions
    #https://www.ag-grid.com/javascript-grid/column-properties/
    gb.configure_default_column(groupable=True, nableRowGroup=True)#,editable=True)# ,aggFunc='sum')
    gb.configure_column("entry_number", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision = 0)
    gb.configure_column("base_srp", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1)
    gb.configure_column("discount", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1,editable = True)
    gb.configure_column("dsrp", type=["numericColumn", "numberColumnFilter"]) #, "customCurrencyFormat" custom_currency_symbol="R$"
    gb.configure_column("period_start", type=["timeStamp"])#, custom_currency_symbol="R$", aggFunc='max')
    #gb.configure_column('row total', valueGetter=st.session_state.add_result.base_srp*st.session_state.add_result.discount, cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])

    
    js = JsCode("""
    function(e) {
        let api = e.api;        
        let sel = api.getSelectedRows();
        api.applyTransaction({remove: [sel]});
    };
    """)
    gb.configure_grid_options(onRowSelected=js) 
    gb.configure_grid_options(domLayout='normal')

    gb.configure_selection(
        selection_mode="multiple",
        #use_checkbox=True,
        rowMultiSelectWithClick=True,
        suppressRowDeselection=False,
        suppressRowClickSelection=False,
        groupSelectsChildren=True,
        groupSelectsFiltered=True,
    )
    gb.configure_side_bar('filter_panel') #filter_panel or column_panel
    gridOptions = gb.build()
    st.write(gridOptions)

    #How to add additional option example
    # https://www.ag-grid.com/documentation/react/row-height/
    # gb = gridOptionsBuilder.from_dataframe()
    # gb.configure_grid_options(rowHeight=50)
    # gridOptions = gb.build()

    grid_response = AgGrid(
        st.session_state.add_result,
        gridOptions=gridOptions,
        height=400, #grid_height
        width='100%',
        update_mode = 'value_changed', #update_mode_value , 
        data_return_mode= 'as_input', #return_mode_value , 
        allow_unsafe_jscode=True, #here 
        enable_enterprise_modules=False, #here
        fit_columns_on_grid_load=True,
        license_key=None,
        try_to_convert_back_to_original_types=True,
        conversion_errors='coerce',
        reload_data=False,
        theme='streamlit',
        key=None) 
    # my_list_of_options = ['Option 1', 'Option 2', 'Option 3']
    # gb.configure_column("field_name", editable=True, cellEditor='agSelectCellEditor', cellEditorParams={'values': my_list_of_options })
    st.write(grid_response)
    def delete_rows():
        st.session_state.add_result = st.session_state.add_result[~ st.session_state.add_result.entry_number.isin(grid_response["selected_rows"])]

    st.button("Delete Selected Rows", on_click = delete_rows())

    with st.expander("Delete Entry"):
        with st.form("Delete Entry",clear_on_submit = True):
            del_entry = st.multiselect(
                    f"Choose Entry number to delete title_name from Buffer Promo",
                    options = list(grid_response["data"]["entry_number"]),
                    key = 'del_entry')
            delete_promo = st.form_submit_button("Delete Promo Entry")

    if delete_promo: 
        try:
            if delete_promo: 
                st.session_state.add_result = st.session_state.add_result[~ st.session_state.add_result.entry_number.isin(del_entry)]
                if "del_entry" in st.session_state:
                    del st.session_state.del_entry
            #st.write(%timeit st.session_state.add_result = st.session_state.add_result[(st.session_state.add_result.title_name!=del_entry)]
            #st.session_state.add_result = st.session_state.add_result.query("entry_number != @del_entry")
            #st.session_state.add_result = st.session_state.add_result[st.session_state.add_result.apply(lambda x: x["title_name"] != del_entry, axis=1)]
            # st.write(newdf)
        except (IndexError, st.errors.StreamlitAPIException):
            st.experimental_rerun()

    if 'data' in grid_response:
        st.dataframe(grid_response['data'])
    
    upload_button = st.button("Upload to Promo DataBase")
    if upload_button:
        #try:
            st.success("SUCCESS!")
            st.success("You have successfully added following entries to DB:")
            upload = grid_response
            upload['data'].set_index('promo_id',inplace = True)
            #upload['data'].index.name = 'ID'
            st.table(upload['data'].style.hide_index())
            #upload = st.session_state.add_result.rename(columns = {"ips_project_title":"Franchise"})
            #st.write(upload.values())
            #show_cols = ["promo_name","Franchise","title_name","Partner_Name","base_srp","discount","dsrp","period_start","period_end","Duration","Publisher","added_by"]
            ts = datetime.now()
            upload['Timestamp'] = ts.strftime('%Y-%m-%d-%H')
            clear_session(st.session_state)
            with st.expander("+"):
                st.table(upload['data'])
                #st.write("Session State:{}".format(st.session_state))
            return (upload['data'])
        #except:
        #    st.spinner("Sorry, smth went wrong! Rerunning...")
            #st.caching.clear_cache()
            #st.experimental_rerun()
            #st.stop()

    #last top 10 by period_end
    lastc = st.container()
    with lastc:
            st.title('Last Promos')
            check = st.empty()
            check.checkbox("Show all", key = 'checking')                       
            if st.session_state.checking:
                last = promodb.query(quer(["added_by"],[st.session_state.sb_user])).reset_index()
                last["period_start"] = last["period_start"].apply(datetime.date)
                last["period_end"] = last["period_end"].apply(datetime.date)
                last = last.sort_values(["period_end"], ascending = False).reset_index(drop = True)
                last.rename(columns = {"ips_project_title":"Franchise"},inplace = True)
                st.dataframe(last)
                #last = df[(df.period_start>start_period)&(df.period_end<end_period)]
            else:
                last = df.sort_values(["period_end"], ascending = False)[:10].reset_index(drop = True)
                last["period_start"] = last["period_start"].apply(datetime.date)
                last["period_end"] =last["period_end"].apply(datetime.date)
                #last["period_end"] =last["period_end"].dt.hour #if pd.to_datetime
                last.rename(columns = {"ips_project_title":"Franchise"},inplace = True)
                st.dataframe(last)

           

#def create_id():

def typesearch(input,df,col):
    df["match"] = df[col].apply(lambda x: fuzz.ratio(input,x))
    dff = df.sort_values("match",ascending = False)
    #top = df["promo_name"].head(5)
    #top["formatted"] = top.apply(lambda x: eval(x["promo_name"]), axis=1)
    # top["formatted"] = top.apply(lambda x: ", ".join(eval(x["artists"])) + " - " + x["name"], axis=1)
    return dff[col].unique()

def clear_session(session):
    for k in session.keys():
        del st.session_state[k]
        #if k not in ["sb_user","sb_partner","sb_ts"]:
        #    del st.session_state[k]
       
def add_entry(entry,cols):
    st.session_state.entry_promo = pd.DataFrame(data = [entry], columns = cols)                                                                                    
    st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])                                                                                     
    st.info("Click un Upload button to add to Promo's DB")
    return st.session_state.add_result

def construct_filters(df):

    promo_name = st.selectbox(
        f"Promo Name",
        df.promo_name.unique()
    )

    title_series = st.selectbox(
        f"title_name Series",
        sorted(df.ips_project_title.unique())
    )
    
    title = st.multiselect(
        f"title_name",
        sorted(df.title_name[df.ips_project_title.isin([title_series])].unique())
    )

    publisher = df[df.ips_project_title.isin([title_series])].Publisher.unique().item()
    st.write("Publisher:", publisher)


# # filter df 2.2 ms
# def filt_df(df,columns,values):
#     for x,v in zip(columns,values):
#         data = df.loc[lambda df: (df[x]==v)]
#     return (data)
#%timeit x=filt(df,columns,values)


## filter df 3.17ms
def quer(columns,values):
    qry = ""
    s = 0
    for x, v in zip(columns,values):
        if s != len(columns)-1:
            qry = qry + x + ' == ' + '"'+str(v)+'"' +' & '
        else:
            qry = qry + x + ' == ' +'"'+ str(v)+'"'
        s+=1
    return (qry)
# x = df.query(quer(columns,values))

    
    
# elif pandas_array.dtype == np.object:
#         proto_array.strings.data.extend(map(str, pandas_array))
#  elif pandas_array.dtype.name.startswith("datetime64"):
#         # Just convert straight to ISO 8601, preserving timezone
#         # awareness/unawareness. The frontend will render it correctly.
#         proto_array.datetimes.data.extend(pandas_array.map(datetime.datetime.isoformat))
#     else:
#         raise NotImplementedError("Dtype %s not understood." % pandas_array.dtype)

# df["timestamp_col"] = pd.Timestamp(datetime.now())
# df["formatted_col"] = df["timestamp_col"].map(lambda ts: ts.strftime("%d-%m-%Y"))