from promo_2 import construct_filters
from altair.vegalite.v4.api import condition
from altair.vegalite.v4.schema.core import ConditionalAxisLabelAlign
from fuzzywuzzy import fuzz

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, DataReturnMode

import pandas as pd
import numpy as np
from pandas.core import base, series
import streamlit as st
from datetime import datetime, timedelta
import time
import datetime as dt
import timeit
import pyarrow as pa

from sqlalchemy import create_engine
from sqlalchemy.types import String, Integer, Date, Float, DECIMAL
#import connection to DB function from main app
from promo import connection

#franchise name - title_name series
#promo type


def app(promodb,dim_partner, dim_product,fact_basesrp):
    st.title("New Promo")
    st.subheader("Insert new Promo to the DataBase")
    st.markdown("On this page you can add new Promo campaign or relaunch the existing one. All inputs are stored in one Promo Database.")
    
    #Make a mask Filter for user and his platform
    session_values = [st.session_state.sb_user, st.session_state.sb_partner]
    promodb = promodb.query(quer(["added_by","partner_name"],session_values)).copy()

    types = {
    # 'promo_id'         :'int64',
    # 'dwh_id_promotion' :'object',
    'promo_name'       : String(128),
    'ips_project_title': String(128),
    'title_name'       : String(128),
    'partner_name'     : String(16),
    'base_srp'         : Float,
    'discount'         : DECIMAL(4,2),#Float(precision=4,decimal_return_scale=2,),
    'dsrp'             : Float,
    'currency'         : String(1),
    'platform'         : String(16),
    'period_start'     : Date,
    'period_end'       : Date,
    'duration'         : Integer(),
    'added_by'         : String(16),
    'dwh_id_dlpartner' : Integer(),
    'dwh_id_dlproduct' : Integer()}
    
    cols = promodb.columns[2:]
    # st.write(cols)
    if "entry_promo" not in st.session_state:
        st.session_state.entry_promo = pd.DataFrame(columns=cols)
    if "add_result" not in st.session_state:
        st.session_state.add_result = pd.DataFrame(columns=cols)

   
    # with st.expander("Add New Promo"):
    #     #st.markdown("1. Insert information about the Promo in the fields below. \t 2. Click on 'Add Promo Entry' button.\t 3. Repeat 1st step untill all desired Promo's are added to the Buffer.\t 4. Verify that entered information is correct. You may also delete any wrong entry.\t 5. Finally, click on 'Upload to Promo DataBase' to send data to storage.")
    #     with st.form("Add New Promo", clear_on_submit=True):
    #         with st.container():
    #             col1_c, col2_c = st.columns(2)
    #             with col1_c:
    #                 promo_name = st.text_input(dim_product.columns[1])#, key = "p1_pn")
    #                 ips_project_title = st.text_input(dim_product.columns[2])#, key = "p1_ts",)
    #                 base_srp = st.text_input(dim_product.columns[5])#, key = "p1_bs")         #automatic
    #                 dsrp = st.text_input(dim_product.columns[7])#, key = "p1_ds")             #automatic
    #                 partner_name = st.text_input(dim_product.columns[4])#, key = "p1_pr")
    #                 period_start = st.date_input(dim_product.columns[8])#, key = "p1_ps")
    #             with col2_c:
    #                 id = st.text_input(dim_product.columns[0])#, key = "p1_id")               #create_id() #implement function of creation
    #                 title_name = st.text_input(dim_product.columns[3])#, key = "p1_tt")
    #                 discount = st.text_input(dim_product.columns[6])#, key = "p1_dc")
    #                 added_by = st.text_input(dim_product.columns[11])#, key = "p1_ab")        #automatic - login credentials
    #                 publisher = st.text_input(dim_product.columns[10])#, key = "p1_pb")
    #                 period_end = st.date_input(dim_product.columns[9])#, key = "p1_pe")
    #             form_button = st.form_submit_button("Add Promo Info",
    #             help = "1.Insert information about the Promo in the fields below. \t 2. Click on 'Add Promo Entry' button.\t 3. Repeat 1st step untill all desired Promo's are added to the Buffer.\t 4. Verify that entered information is correct. You may also delete any wrong entry.\t 5. Finally, click on 'Upload to Promo DataBase' to send data to storage.",
    #             )
    #             if form_button:
    #                 entries = [id,promo_name,ips_project_title,title_name,partner_name,base_srp,discount,dsrp,period_start,period_end,publisher,added_by]
    #                 st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = dim_product.columns)                                                                                    
    #                 st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])                                                                                     
    #                 st.info("Click un Upload button to add to Promo's DB")

    
    col1,col2 = st.columns([10,10])
    col11,col22 = st.columns(2)
    timestamp = pd.Timestamp(datetime.now()).strftime("%d-%m-%Y")

    with col1:
        # promo = st.text_input("Start typing Promo")
        # if promo != "":
        #     dim_product['Match'] = dim_product["promo_name"].apply(lambda x: fuzz.ratio(promo,x))
        #     dim_product.sort_values("Match",ascending = False, inplace = True)
        #     #top = dim_product["promo_name"].head(5)
        #     #top["formatted"] = top.apply(lambda x: eval(x["promo_name"]), axis=1)
        #     # top["formatted"] = top.apply(lambda x: ", ".join(eval(x["artists"])) + " - " + x["name"], axis=1)
        #     st.selectbox("Did you mean one of these Promo's?", dim_product["promo_name"].unique())
        promo_name = st.text_input(
        f"Promo Name",
        promodb.promo_name.unique()
        )
        st.write(st.session_state.sb_ts)
        ips_project_title = st.session_state.sb_ts
        add_all = st.checkbox("Add all Titles", value = False, help = "Add all Titles for this Franchise",key = "add_all")
        if st.session_state.add_all:
            titles = sorted(dim_product.title_name[(dim_product.ips_project_title.isin([st.session_state.sb_ts]))&(dim_product.partner_name==st.session_state.sb_partner)].unique())
            with st.expander("Titles"):
                st.write(titles)
        else:
            titles = st.multiselect(
                f"Title Name",
                sorted(dim_product.title_name[(dim_product.ips_project_title.isin([st.session_state.sb_ts]))&(dim_product.partner_name==st.session_state.sb_partner)].unique()),
                key = 'tt'
            )
        platform = st.text_input("Platform")
        # publisher = sorted(dim_product[dim_product.ips_project_title.isin([st.session_state.sb_ts])].Publisher.unique())
        # if len(publisher)>1:
        #     publisher = st.selectbox(
        #     f"Publisher",
        #     sorted(dim_product.Publisher.unique()),
        #     #key = 'pb'
        #     )
        # else:
        #     publisher = publisher[0]
        #     #st.write("Publisher:", publisher)

    with col2:
        base_srp = st.number_input("Base SRP",min_value=0.0, key = "p1_bs")         #automatic from source #later
        discount = st.number_input("Enter Discount %",min_value = 0.,max_value = 100.,value = 50., key = "p1_dc",step = 0.1)
        currency = st.selectbox("Currency", options = ['€','$','¥'])
        #discount = st.number_input(dim_product.columns[6],min_value = 0.,max_value = 100.,value = 75., key = "p1_dc",step = 0.1)
        dsrp = round(base_srp*discount/100,2)
        st.write("DSRP: ", dsrp)
        
    with col11:
        period_start = st.date_input("Period Start", key = 'period_start')
        submitted = st.button("Add Promo Entry")

    with col22:
        period_end = st.date_input("Period End", key = 'period_end',value = st.session_state.period_start+timedelta(7))
        length = (st.session_state.period_end-st.session_state.period_start) #timedelta class
        st.write("Duration:",length.days)

    if submitted:
        if type(titles) is list:
            for title_name in titles:
                dwh_id_dlpartner = dim_product.dwh_id_dlpartner[(dim_product.partner_name==st.session_state.sb_partner)].unique()[0] #partner_name is an additional field from main app, not in dwh db
                dwh_id_dlproduct = dim_product.dwh_id_dlproduct[(dim_product.title_name == title_name) & (dim_product.partner_name == st.session_state.sb_partner)].unique()[0]
                entries = promo_name,ips_project_title,title_name,st.session_state.sb_partner,str(base_srp),discount,str(dsrp),currency,platform,period_start,period_end,length.days,st.session_state.sb_user,dwh_id_dlpartner,dwh_id_dlproduct
                st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
                st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])   
        else:
            dwh_id_dlpartner = dim_product.dwh_id_dlpartner[(dim_product.partner_name==st.session_state.sb_partner)].unique()[0] #partner_name is an additional field from [main app, not in dwh db
            dwh_id_dlproduct = dim_product.dwh_id_dlproduct[(dim_product.title_name == titles) & (dim_product.partner_name == st.session_state.sb_partner)].unique()[0]
            entries = promo_name,ips_project_title,titles,st.session_state.sb_partner,str(base_srp),discount,str(dsrp),currency,platform,period_start,period_end,length.days,st.session_state.sb_user,dwh_id_dlpartner,dwh_id_dlproduct
            st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = cols)
            st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])
        # "{:.2f}%".format(discount)
        st.session_state.add_result.reset_index(inplace=True, drop = True)
        st.info("Click un Upload button to add to Promo's DB")
    
    # arrowpromo = pa.Schema.from_pandas(promodb)
    # dfresult = st.session_state.add_result.astype(types)
    # st.write(arrowpromo)
    # st.write(dfresult)


    #dim_product.iloc[x,]
    #dim_product.loc[dim_product.index[0:5],["col1,col2"]]

    #st.session_state.add_result.reset_index(drop = True, inplace = True)
    #st.session_state.add_result.set_index("Promo_ID",inplace = True)
    # show_table =  st.session_state.add_result.rename(columns = {"ips_project_title":"Franchise"})
    # show_cols_add_result = ["promo_name","ips_project_title","title_name","partner_name","base_srp","discount","dsrp","currency","period_start","period_end","duration","added_by"]
    # show_cols = ["Promo Name","Franchise","Title","Partner Name","Base SRP","Discount","DSRP","Currency","Period Start","Period End","Duration","Added by"]
    # show_table = st.session_state.add_result[show_cols_add_result].copy()
    # show_table.set_axis(show_cols,axis=1)
    # st.table(show_table)

# AGGRID PART to be thought of later
    return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
    return_mode_value = DataReturnMode.__members__[return_mode]

    update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=6)
    update_mode_value = GridUpdateMode.__members__[update_mode] 

    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(st.session_state.add_result)
    #customize gridOptions
    #https://www.ag-grid.com/javascript-grid/column-properties/
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True)#,editable=True)# ,aggFunc='sum')
    gb.configure_column("promo_name", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision = 0,checkboxSelection = True)
    gb.configure_column("base_srp", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1,editable = True)
    gb.configure_column("discount", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1,editable = True)
    gb.configure_column("dsrp", type=["numericColumn", "numberColumnFilter"],aggFunc='sum', editable = False) #, "customCurrencyFormat" custom_currency_symbol="R$"
    gb.configure_column("period_start", type=["timeStamp"])
    gb.configure_grid_options(domLayout='normal')
    #gb.configure_column('row total', valueGetter=st.session_state.add_result.Base_SRP()*st.session_state.add_result.Discount.to_numeric(), cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])
    gridOptions = gb.build()

    js = JsCode("""
    function(e) {
        let api = e.api;        
        let sel = api.getSelectedRows();
    };
    """) #api.applyTransaction({remove: [sel]});

    gb.configure_grid_options(onRowSelected=js) 
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

    grid_response = AgGrid(
        st.session_state.add_result,
        gridOptions=gridOptions,
        height=400, #grid_height
        width='100%',
        fit_columns_on_grid_load=False,
        update_mode= update_mode_value , #'value_changed'
        data_return_mode= return_mode_value , #'as_input'
        allow_unsafe_jscode=True, #here 
        enable_enterprise_modules=True, #here
        license_key=None,
        try_to_convert_back_to_original_types=True,
        conversion_errors='coerce',
        reload_data=False,
        theme='streamlit',
        key=None)
    
    upload_button1 = st.button("Upload only Selected Rows to Promo Databse")
    upload_button2 = st.button("Upload all Entries to Promo DataBase")
    if upload_button1:
        # try:
        if len(grid_response["selected_rows"])==0:
            st.warning("You haven't selected rows")
        else:
            upload = pd.DataFrame(grid_response["selected_rows"], index = None)
            upload.to_sql(name = 'f', con = connection(), if_exists = 'append', index = False, dtype = types)
            
        # upload['data'].set_index('Promo_ID',inplace = True)
        #upload['data'].index.name = 'ID'
        # # st.table(upload.style.hide_index())
        # show_cols = ["ID","Promo Name","Franchise","Title","Partner Name","Base SRP","Discount","DSRP","Currency","Platform","Period Start","Period End","Duration","Added by","ID Partner","ID Product"]
        # upload_renamed=pd.DataFrame.from_dict(upload)
        # upload_renamed.rename(show_cols,axis=1)
        # ts = datetime.now()
        # up = pd.DataFrame.from_dict(x for _,x in enumerate(upload))
        # up['Timestamp'] = ts.strftime('%Y-%m-%d-%H')
            st.success("SUCCESS!")
            st.success("You have successfully added following entries to DB:")
            with st.expander("+"):
                st.table(grid_response["selected_rows"])
            clear_session(st.session_state)
        # st.write(upload_renamed)
        # st.write(up)
        # with st.expander("+"):
        #     st.write(up)
            return grid_response["selected_rows"]
        # except:
        #     st.spinner("Sorry, smth went wrong! Rerunning...")
        #     # st.caching.clear_cache()
        #     st.experimental_rerun()

    if upload_button2:
        upload = grid_response["data"]
        upload["dwh_id_promotion"]="123321"
        #Upload data
        upload.to_sql(name = 'promodb', con = connection(), if_exists = 'append', index = False, dtype = types)
        clear_session(st.session_state)
        with st.expander("+"):
            st.table(upload)
        return upload

    #last top 10 by period_end
    lastc = st.container()
    #with lastc.expander('Last Promos'):
    with lastc:
            st.title('Last Promos')
            check = st.empty()
            check.checkbox("Show all", key = 'checking')
                       
            if st.session_state.checking:
                last = promodb.query(quer(["added_by"],[st.session_state.sb_user])).reset_index().copy()
                # last["period_start"] = last["period_start"].apply(datetime.date)
                # last["period_end"] = last["period_end"].apply(datetime.date)
                last = last.sort_values(["period_end"], ascending = False).reset_index(drop = True)
                last.rename(columns = {"ips_project_title":"Franchise"},inplace = True)
                st.dataframe(last)
                #last = dim_product[(dim_product.period_start>start_period)&(dim_product.period_end<end_period)]
            else:
                last = promodb.sort_values(["period_end"], ascending = False)[:10].reset_index(drop = True).copy()
                # last["period_start"] = last["period_start"].apply(datetime.date)
                # last["period_end"] =last["period_end"].apply(datetime.date)
                #last["period_end"] =last["period_end"].dt.hour #if pd.to_datetime
                last.rename(columns = {"ips_project_title":"Franchise"},inplace = True)
                st.dataframe(last)

           

#def create_id():

def clear_session(session):
    for k in session.keys():
        del st.session_state[k]
        #if k not in ["sb_user","sb_partner","sb_ts"]:
        #    del st.session_state[k]

def connection():
        #UPLOADING TO MYSQL DB
        client_cert = 'C:\\Users\\o.georgievskiy\\client-cert.pem'
        client_key = 'C:\\Users\\o.georgievskiy\\client-key.pem'
        server_ca = 'C:\\Users\\o.georgievskiy\\server-ca.pem'
        #Connection attributes
        db_data = 'mysql+mysqlconnector://' + 'root' + ':' + 'sA2gw3Fpkpe9sn35' + '@' + '34.89.188.155' + ':3306/' + 'promotions' + '?charset=utf8mb4' #pip install mysqlclient 
        connect_args={
                "ssl_ca":server_ca,
                "ssl_cert": client_cert,
                "ssl_key": client_key
            }
        #Create Connection
        engine = create_engine(db_data, connect_args = connect_args)
        return engine
       
def add_entry(entry,cols):
    st.session_state.entry_promo = pd.DataFrame(data = [entry], columns = cols)                                                                                    
    st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])                                                                                     
    st.info("Click un Upload button to add to Promo's DB")
    return st.session_state.add_result

def construct_filters(dim_product):

    promo_name = st.selectbox(
        f"Promo Name",
        dim_product.promo_name.unique()
    )

    ips_project_title = st.selectbox(
        f"title_name Series",
        sorted(dim_product.ips_project_title.unique())
    )
    
    title_name = st.multiselect(
        f"title_name",
        sorted(dim_product.title_name[dim_product.ips_project_title.isin([ips_project_title])].unique())
    )

    publisher = dim_product[dim_product.ips_project_title.isin([ips_project_title])].Publisher.unique().item()
    st.write("Publisher:", publisher)


# # filter dim_product 2.2 ms
# def filt_df(dim_product,columns,values):
#     for x,v in zip(columns,values):
#         data = dim_product.loc[lambda dim_product: (dim_product[x]==v)]
#     return (data)
#%timeit x=filt(dim_product,columns,values)


## filter dim_product 3.17ms
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


def rename_keys(dict_, new_keys):
    """
     new_keys: type List(), must match length of dict_
    """

    # dict_ = {oldK: value}
    # d1={oldK:newK,} maps old keys to the new ones:  
    d1 = dict( zip( list(dict_.keys()), new_keys) )

          # d1{oldK} == new_key 
    return {d1[oldK]: value for oldK, value in dict_.items()}

# x = dim_product.query(quer(columns,values))

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
# def stratified_sample(dim_product, strata, size=None, seed=None, keep_index= True): population = len(dim_product)
#     size = __smpl_size(population, size)
#     tmp = dim_product[strata]
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
#             stratified_df = dim_product.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
#             first = False
#         else:
#             tmp_df = dim_product.query(qry).sample(n=n, random_state=seed).reset_index(drop=(not keep_index))
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


# dim_product["timestamp_col"] = pd.Timestamp(datetime.now())
# dim_product["formatted_col"] = dim_product["timestamp_col"].map(lambda ts: ts.strftime("%d-%m-%Y"))