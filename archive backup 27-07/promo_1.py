from promo_2 import construct_filters
from altair.vegalite.v4.api import condition
from altair.vegalite.v4.schema.core import ConditionalAxisLabelAlign
import pandas as pd
import numpy as np
from pandas.core import base
import streamlit as st
from datetime import datetime, timedelta
import time
import datetime as dt

# add length

def app(data):
    st.title("New Promo")
    st.subheader("Insert new Promo to the DataBase")
    st.markdown("On this page you can add new Promo campaign or relaunch the existing one. All inputs are stored in one Promo Database.")
    df = data.reset_index()                              #reset ID's to be a column

    session_values = [st.session_state.sb_user, st.session_state.sb_partner, st.session_state.sb_ts]
    
    # st.write(quer(["Added_by","Partner_Name","Title_Series"],session_values))
    df = df.query(quer(["Added_by","Partner_Name","Title_Series"],session_values))
    #st.write(df)
        
    # query = 'Added_by == {} & Partner_Name == {} & Title_Series == {} & Title == {}'.format(st.session_state.user_name, st.session_state.partner_name, st.session_state.title_series, st.session_state.title)
    # df = df.query[query]

    if "entry_promo" not in st.session_state:
        st.session_state.entry_promo = pd.DataFrame(columns=df.columns)
    
    if "add_result" not in st.session_state:
        st.session_state.add_result = pd.DataFrame(columns=df.columns)
    #ids = df[df.columns[0]]                              #get all ID's
    

    # with st.beta_expander("Add New Promo"):
    #     #st.markdown("1. Insert information about the Promo in the fields below. \t 2. Click on 'Add Promo Entry' button.\t 3. Repeat 1st step untill all desired Promo's are added to the Buffer.\t 4. Verify that entered information is correct. You may also delete any wrong entry.\t 5. Finally, click on 'Upload to Promo DataBase' to send data to storage.")
    #     with st.form("Add New Promo", clear_on_submit=True):
    #         with st.beta_container():
    #             col1_c, col2_c = st.beta_columns(2)
    #             with col1_c:
    #                 promo_name = st.text_input(df.columns[1])#, key = "p1_pn")
    #                 title_series = st.text_input(df.columns[2])#, key = "p1_ts",)
    #                 base_srp = st.text_input(df.columns[5])#, key = "p1_bs")         #automatic
    #                 dsrp = st.text_input(df.columns[7])#, key = "p1_ds")             #automatic
    #                 partner_name = st.text_input(df.columns[4])#, key = "p1_pr")
    #                 period_start = st.date_input(df.columns[8])#, key = "p1_ps")
    #             with col2_c:
    #                 id = st.text_input(df.columns[0])#, key = "p1_id")               #create_id() #implement function of creation
    #                 title = st.text_input(df.columns[3])#, key = "p1_tt")
    #                 discount = st.text_input(df.columns[6])#, key = "p1_dc")
    #                 added_by = st.text_input(df.columns[11])#, key = "p1_ab")        #automatic - login credentials
    #                 publisher = st.text_input(df.columns[10])#, key = "p1_pb")
    #                 period_end = st.date_input(df.columns[9])#, key = "p1_pe")
    #             form_button = st.form_submit_button("Add Promo Info",
    #             help = "1.Insert information about the Promo in the fields below. \t 2. Click on 'Add Promo Entry' button.\t 3. Repeat 1st step untill all desired Promo's are added to the Buffer.\t 4. Verify that entered information is correct. You may also delete any wrong entry.\t 5. Finally, click on 'Upload to Promo DataBase' to send data to storage.",
    #             )
    #             if form_button:
    #                 entries = [id,promo_name,title_series,title,partner_name,base_srp,discount,dsrp,period_start,period_end,publisher,added_by]
    #                 st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = df.columns)                                                                                    
    #                 st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])                                                                                     
    #                 st.info("Click un Upload button to add to Promo's DB")

    
    #st.table(st.session_state.add_result)
    col1,col2 = st.beta_columns(2)
    col11,col22 = st.beta_columns(2)
    timestamp = pd.Timestamp(datetime.now()).strftime("%d-%m-%Y")

    with col1:
        promo_name = st.selectbox(
            f"Promo Name",
            np.insert(df.Promo_Name.unique(),0,""),
            key = 'pn'
        )
        if st.session_state.sb_new:
            title_series = st.text_input(
            f"Title Series",
            key = 'tsn'
            )
        else:
            title_series = st.selectbox(
                f"Title Series",
                sorted(df.Title_Series.unique()),
                key = 'ts'
            )
        if st.session_state.sb_new:
            title = st.text_input(
            f"Title",
            key = 'ttn'
            )
        else:
            title = st.multiselect(
                f"Title",
                sorted(df.Title[df.Title_Series.isin([title_series])].unique()),
                key = 'tt'
            )

    with col2:
        id = promo_name + timestamp               #create_id() #implement function of creation
        base_srp = st.number_input(df.columns[5],step = 10)#, key = "p1_bs")         #automatic
        discount = st.number_input(df.columns[6])#, key = "p1_dc")
        dsrp = "29.99"
        st.write("DSRP: ", dsrp)
        if st.session_state.sb_new:
            publisher = st.text_input(
            f"Publisher",
            key = 'pbn'
            )
        else:
            publisher = sorted(df[df.Title_Series.isin([title_series])].Publisher.unique())
            if len(publisher)>1:
                publisher = st.selectbox(
                f"Title Series",
                sorted(df.Publisher.unique()),
                key = 'pb'
                )
            else:
                publisher = publisher[0]
                st.write("Publisher:", publisher)
        
    with col11:
        period_start = st.date_input(df.columns[8], key = 'period_start')
        submitted = st.button("Add Promo Entry")

    with col22:
        period_end = st.date_input(df.columns[9], key = 'period_end',value = st.session_state.period_start+timedelta(7))
        length = st.session_state.period_end-st.session_state.period_start
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
                entries = id,promo_name,title_series,title,st.session_state.sb_partner,base_srp,discount,dsrp,period_start,period_end,length,publisher,st.session_state.sb_user
                st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = df.columns)
                st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])   
        else:
            entries = id,promo_name,title_series,title,st.session_state.sb_partner,base_srp,discount,dsrp,period_start,period_end,length,publisher,st.session_state.sb_user
            st.session_state.entry_promo = pd.DataFrame(data = [entries], columns = df.columns)
            st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])
        st.info("Click un Upload button to add to Promo's DB")

    del_entry = st.selectbox("Choose Titles to delete from Buffer Promo",
        np.insert(st.session_state.add_result.Title.unique(),0,""),
        key = 'del_entry'
        )
    delete_promo = st.button("Delete Promo Entry")
    
  
    if delete_promo: 
        st.session_state.add_result = st.session_state.add_result[~st.session_state.add_result.Title.isin([del_entry])]    
        #st.write(st.session_state.add_result)   

    # with st.beta_expander("View buffer Promo"):   
    #     st.write(st.session_state.add_result)
    #     upload_button = st.button("Upload to Promo DataBase")
    st.write(st.session_state.add_result)
    upload_button = st.button("Upload to Promo DataBase")



    if upload_button:
        try:
            st.success("SUCCESS!")
            st.success("You have successfully added following entries to DB:")
            upload = st.session_state.add_result
            clear_session(st.session_state)
            with st.beta_expander("+"):
                st.table(upload)
            return (upload)
        except:
            st.warning("WARNING")
            st.stop()

    #last top 10 by Period_End
    lastc = st.beta_container()
    #with lastc.beta_expander('Last Promos'):
    with lastc:
            st.title('Last Promos')
            check = st.empty()
            #start_period, end_period = '01.01.2019','01.01.2023'
            check.checkbox("Show all", key = 'checking')
            #st.write("Range:", start_period, end_period)
            #speriod = st.slider("Choose period", min_value = start_period, value=['01.01.2019','01.01.2023'], max_value = end_period)
            
            if st.session_state.checking:
                last = data.query(quer(["Added_by"],[st.session_state.sb_user])).reset_index()
                last = last.sort_values(["Period_End"], ascending = False).reset_index(drop = True)
                st.write(last)
                #last = df[(df.Period_Start>start_period)&(df.Period_End<end_period)]
            else:
                last = df.sort_values(["Period_End"], ascending = False)[:10].reset_index(drop = True)
                st.write(last)

    #st.write (st.session_state)
        

#def create_id():

def clear_session(session):
    for k in session.keys():
        print(k)
        del st.session_state[k]
       
def add_entry(entry,cols):
    st.session_state.entry_promo = pd.DataFrame(data = [entry], columns = cols)                                                                                    
    st.session_state.add_result = st.session_state.add_result.append([st.session_state.entry_promo])                                                                                     
    st.info("Click un Upload button to add to Promo's DB")
    return st.session_state.add_result

# # filter df 2.2 ms
# def filt_df(df,columns,values):
#     for x,v in zip(columns,values):
#         data = df.loc[lambda df: (df[x]==v)]
#     return (data)
#%timeit x=filt(df,columns,values)

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

# st.title('Counter Example')
# if 'count' not in st.session_state:
#     st.session_state.count = 0
#     st.session_state.last_updated = datetime.time(0,0)

# def update_counter():
#     st.session_state.count += st.session_state.increment_value
#     st.session_state.last_updated = st.session_state.update_time

# with st.form(key='my_form'):
#     st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
#     st.number_input('Enter a value', value=0, step=1, key='increment_value')
#     submit = st.form_submit_button(label='Update', on_click=update_counter)


# df["timestamp_col"] = pd.Timestamp(datetime.now())
# df["formatted_col"] = df["timestamp_col"].map(lambda ts: ts.strftime("%d-%m-%Y"))