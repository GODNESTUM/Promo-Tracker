
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, DataReturnMode
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

import streamlit as st
from datetime import datetime, timedelta

def app(data_all_promos,dfs_dwh):
    st.title("New Promo")
    st.subheader("Insert new Promo to the DataBase")
    st.markdown("On this page you can add new Promo campaign or relaunch the existing one. All inputs are stored in one Promo Database.")
    st.write(dfs_dwh)
    dim_partner = dfs_dwh[0]
    dim_product = dfs_dwh[1]
    #dim_partner

    #Make a mask Filter for user and his platform
    session_values = [st.session_state.sb_user, st.session_state.sb_partner]
    df = data_all_promos.query(quer(["Added_by","Partner_Name"],session_values))
    
    # cols = np.insert(df.columns,0,"Entry_Number")
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
        #np.insert(df.Promo_Name.unique(),0,"")
        df.Promo_Name.unique()
        ,key = 'pn'
        )
        add_all_franchise = st.checkbox("Select all Franchise", key = 'copy_promo_all_fracnhise')
        add_all_titles = st.checkbox("Select all Titles", key = 'copy_promo_all_titles')

    col0,col1,col2 = st.columns([2,10,10])
    col00,col11,col22 = st.columns(3)
    timestamp = pd.Timestamp(datetime.now()).strftime("%d-%m-%Y")
    
    with col1:
        promo = st.text_input("Start typing Promo")
        if promo != "":
            df['Match'] = df["Promo_Name"].apply(lambda x: fuzz.ratio(promo,x))
            df.sort_values("Match",ascending = False, inplace = True)
            #top = df["Promo_Name"].head(5)
            #top["formatted"] = top.apply(lambda x: eval(x["Promo_Name"]), axis=1)
            # top["formatted"] = top.apply(lambda x: ", ".join(eval(x["artists"])) + " - " + x["name"], axis=1)
            st.selectbox("Did you mean one of these Promo's?", df["Promo_Name"].unique())
            
        promo_name = st.selectbox(
        f"Promo Type",
        #np.insert(df.Promo_Name.unique(),0,"")
        df.Promo_Name.unique()
        #,key = 'pn'
        )
        if st.session_state.sb_new:
            title_series = st.text_input(
            f"Franchise",
            #key = 'tsn'
            )
            title = st.text_input(
            f"Title",
            #key = 'ttn'
            )
        else:
            title_series = st.session_state.sb_ts
            add_all = st.checkbox("Add all Titles", value = False, help = "Add all Titles for this Franchise",key = "add_all")
            if st.session_state.add_all:
                title = sorted(df.Title[df.Title_Series.isin([st.session_state.sb_ts])].unique())
                with st.expander("Titles"):
                    st.write(title)
            else:
                title = st.multiselect(
                    f"Title",
                    sorted(df.Title[df.Title_Series.isin([st.session_state.sb_ts])].unique()),
                    key = 'tt'
                )
            # title_series = st.selectbox(
            #     f"Title Series",
            #     sorted(df.Title_Series.unique()),
            #     key = 'ts'
            # )
        # if st.session_state.sb_new:
        #     publisher = st.text_input(
        #     f"Publisher",
        #     #key = 'pbn'
        #     )
        # else:
        publisher = sorted(df[df.Title_Series.isin([st.session_state.sb_ts])].Publisher.unique())
        if len(publisher)>1:
            publisher = st.selectbox(
            f"Publisher",
            sorted(df.Publisher.unique()),
            #key = 'pb'
            )
        else:
            publisher = publisher[0]
            #st.write("Publisher:", publisher)

    id = promo_name + timestamp               #create_id() #later - implement function of creation
    with col2:
        base_srp = st.number_input(df.columns[5],step = 10,value = 50, key = "p1_bs")         #automatic from source #later
        discount = st.number_input(df.columns[6]+"%",min_value = 0.,max_value = 100.,value = 75., key = "p1_dc",step = 0.1)
        currency = st.selectbox("Currency", options = ['€','$','¥'])
        #discount = st.number_input(df.columns[6],min_value = 0.,max_value = 100.,value = 75., key = "p1_dc",step = 0.1)
        dsrp = round(base_srp*discount/100,2)
        st.write("DSRP: ", dsrp)
        
    with col11:
        period_start = st.date_input(df.columns[8], key = 'period_start')
        #st.write(st.session_state)
        submitted = st.button("Add Promo Entry")

    with col22:
        period_end = st.date_input(df.columns[9], key = 'period_end',value = st.session_state.period_start+timedelta(7))
        #st.write(type(period_start))
        length = (st.session_state.period_end-st.session_state.period_start) #timedelta class
        # st.write(type(length.days)) #int class
        st.write("Duration:",length.days)

    if submitted:
        # with st.spinner(text = f"Promo DB has been up...."):
        #     time.sleep(4)
        # with st.spinner(text = f"...WAIT FOR IT!!!!..."):
        #     time.sleep(3)
        # with st.spinner(text = f"WAAAAAAAAAAAAAAAAIT"):
        #     time.sleep(2)
        # st.warning("DATED!!!!")
        
        if type(title) is list:
            for title in title:
                st.session_state.entry_number +=1
                entries = st.session_state.entry_number, id,promo_name,title_series,title,st.session_state.sb_partner,str(base_srp)+currency,"{:.2f}%".format(discount),str(dsrp)+currency,period_start,period_end,length.days,publisher,st.session_state.sb_user
                st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
                st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])   
        else:
            st.session_state.entry_number +=1
            entries = st.session_state.entry_number,id,promo_name,title_series,title,st.session_state.sb_partner,str(base_srp)+currency,"{}%.2f%".format(discount),str(dsrp)+currency,period_start,period_end,length.days,publisher,st.session_state.sb_user
            st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
            st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])
        st.info("Click un Upload button to add to Promo's DB")

    #df.iloc[x,]
    #df.loc[df.index[0:5],["col1,col2"]]

    show_table =  st.session_state.add_result.rename(columns = {"Title_Series":"Franchise"})
    show_cols_add_result = ["Entry_Number","Promo_Name","Franchise","Title","Partner_Name","Base_SRP","Discount","DSRP","Period_Start","Period_End","Duration","Publisher","Added_by"]

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
    gb.configure_column("Entry_Numer", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision = 0)
    gb.configure_column("Base_SRP", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1)
    gb.configure_column("Discount", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1,editable = True)
    gb.configure_column("DSRP", type=["numericColumn", "numberColumnFilter"]) #, "customCurrencyFormat" custom_currency_symbol="R$"
    gb.configure_column("Period_Start", type=["timeStamp"])#, custom_currency_symbol="R$", aggFunc='max')
    #gb.configure_column('row total', valueGetter=st.session_state.add_result.Base_SRP*st.session_state.add_result.Discount, cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])

    
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
        st.session_state.add_result = st.session_state.add_result[~ st.session_state.add_result.Entry_Number.isin(grid_response["selected_rows"])]

    st.button("Delete Selected Rows", on_click = delete_rows())

    with st.expander("Delete Entry"):
        with st.form("Delete Entry",clear_on_submit = True):
            del_entry = st.multiselect(
                    f"Choose Entry number to delete Title from Buffer Promo",
                    options = list(grid_response["data"]["Entry_Number"]),
                    key = 'del_entry')
            delete_promo = st.form_submit_button("Delete Promo Entry")

    if delete_promo: 
        try:
            if delete_promo: 
                st.session_state.add_result = st.session_state.add_result[~ st.session_state.add_result.Entry_Number.isin(del_entry)]
                if "del_entry" in st.session_state:
                    del st.session_state.del_entry
            #st.write(%timeit st.session_state.add_result = st.session_state.add_result[(st.session_state.add_result.Title!=del_entry)]
            #st.session_state.add_result = st.session_state.add_result.query("Entry_Number != @del_entry")
            #st.session_state.add_result = st.session_state.add_result[st.session_state.add_result.apply(lambda x: x["Title"] != del_entry, axis=1)]
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
            upload['data'].set_index('Promo_ID',inplace = True)
            #upload['data'].index.name = 'ID'
            st.table(upload['data'].style.hide_index())
            #upload = st.session_state.add_result.rename(columns = {"Title_Series":"Franchise"})
            #st.write(upload.values())
            #show_cols = ["Promo_Name","Franchise","Title","Partner_Name","Base_SRP","Discount","DSRP","Period_Start","Period_End","Duration","Publisher","Added_by"]
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

    #last top 10 by Period_End
    lastc = st.container()
    with lastc:
            st.title('Last Promos')
            check = st.empty()
            check.checkbox("Show all", key = 'checking')
                       
            if st.session_state.checking:
                last = data.query(quer(["Added_by"],[st.session_state.sb_user])).reset_index()
                last["Period_Start"] = last["Period_Start"].apply(datetime.date)
                last["Period_End"] = last["Period_End"].apply(datetime.date)
                last = last.sort_values(["Period_End"], ascending = False).reset_index(drop = True)
                last.rename(columns = {"Title_Series":"Franchise"},inplace = True)
                st.dataframe(last)
                #last = df[(df.Period_Start>start_period)&(df.Period_End<end_period)]
            else:
                last = df.sort_values(["Period_End"], ascending = False)[:10].reset_index(drop = True)
                last["Period_Start"] = last["Period_Start"].apply(datetime.date)
                last["Period_End"] =last["Period_End"].apply(datetime.date)
                #last["Period_End"] =last["Period_End"].dt.hour #if pd.to_datetime
                last.rename(columns = {"Title_Series":"Franchise"},inplace = True)
                st.dataframe(last)

           

#def create_id():

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
        df.Promo_Name.unique()
    )

    title_series = st.selectbox(
        f"Title Series",
        sorted(df.Title_Series.unique())
    )
    
    title = st.multiselect(
        f"Title",
        sorted(df.Title[df.Title_Series.isin([title_series])].unique())
    )

    publisher = df[df.Title_Series.isin([title_series])].Publisher.unique().item()
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

#data = st.file_uploader('Upload here',type = 'csv')
# if data is not None:
#      appdata = pd.read_csv(data)  #read the data fro
#      appdata['ds'] = pd.to_datetime(appdata['ds'],errors='coerce') 
#      st.write(data) #display the data  
#      max_date = appdata['ds'].max() #compute latest date in the data 

    #  obj = Prophet() #Instantiate Prophet object 
    #  obj.fit(appdata)  #fit the data 
    #forecast_filtered =  forecast[forecast['ds'] > max_date] 

    #ids = df[df.columns[0]]                              #get all ID'spi
    
    
# elif pandas_array.dtype == np.object:
#         proto_array.strings.data.extend(map(str, pandas_array))
#  elif pandas_array.dtype.name.startswith("datetime64"):
#         # Just convert straight to ISO 8601, preserving timezone
#         # awareness/unawareness. The frontend will render it correctly.
#         proto_array.datetimes.data.extend(pandas_array.map(datetime.datetime.isoformat))
#     else:
#         raise NotImplementedError("Dtype %s not understood." % pandas_array.dtype)


# if __name__ == '__app__':
#     app()

### STRATIFIED SAMPLE
# def stratified_sample(df, strata, size=None, seed=None, keep_index= True): population = len(df)
#     size = __smpl_size(population, size)
#     tmp = df[strata]
#     tmp['size'] = 1
#     tmp_grpd = tmp.groupby(strata).count().reset_index()
#     tmp_grpd['samp_size'] = round(size/population * tmp_grpd['size']).astype(int)

#     # controlling variable to create the dataframe or append to it
#     first = True 
#     for i in range(len(tmp_grpd)):
#         # query generator for each iteration
#         qry=''
#         for s in range(len(strata)):
#             stratum = strata[s]
#             value = tmp_grpd.iloc[i][stratum]
#             n = tmp_grpd.iloc[i]['samp_size']

#             if type(value) == str:
#                 value = "'" + str(value) + "'"
            
#             if s != len(strata)-1:
#                 qry = qry + stratum + ' == ' + str(value) +' & '
#             else:
#                 qry = qry + stratum + ' == ' + str(value)
        
#         # final dataframe
#         if first:
#             stratified_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
#             first = False
#         else:
#             tmp_df = df.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
#             stratified_df = stratified_df.append(tmp_df, ignore_index=True)
    
#     return stratified_df



# def append_value(dict_obj, key, value):
# # Check if key exist in dict or not
#     if key in dict_obj:
#         # Key exist in dict.
#         # Check if type of value of key is list or not
#         if not isinstance(dict_obj[key], list):
#             # If type is not list then make it list
#             dict_obj[key] = [dict_obj[key]]
#         # Append the value in list
#         dict_obj[key].append(value)
#     else:
#         # As key is not in dict,
#         # so, add key-value pair
#         dict_obj[key] = value


# df["timestamp_col"] = pd.Timestamp(datetime.now())
# df["formatted_col"] = df["timestamp_col"].map(lambda ts: ts.strftime("%d-%m-%Y"))