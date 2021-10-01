### streamlit version == 0.85.1

# import apps (pages)
# from streamlit.state.session_state import SessionState
# from altair.vegalite.v4.schema.core import TitleAnchor
# from streamlit.state.session_state import SessionState 

import promo_1
import promo_2
import promo_3
import promo_x
#import other libraries
import streamlit as st
import pandas as pd
import glob
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns
# import base64
# import io

@st.cache(suppress_st_warning=True)
def load_metadata_promo():
    DATA_URL = "C:\\Users\\o.georgievskiy\\Koch Media GmbH\\Internship - Oleg Georgievskiy - General\\Promo Tracker\\Promo_Old_c.csv"
    df = pd.read_csv(DATA_URL, delimiter = ";", index_col = None)   #check for delimiter in csv or other file format adjust accordingly
    df["Period_Start"] = pd.to_datetime(df["Period_Start"],infer_datetime_format = True,format = "%m/%d/%Y")
    df["Period_End"] = pd.to_datetime(df["Period_End"],infer_datetime_format = True,format = "%m/%d/%Y")
    return df
    #return df.set_index("Promo ID")

@st.cache(suppress_st_warning=True)
def load_metadata_dwh(): 
    PATH = "C:\\Users\\o.georgievskiy\\Koch Media GmbH\\Internship - Oleg Georgievskiy - General\\Promo Tracker\\DWH_Dimensions"
    filenames = glob.glob(PATH+"/*.csv")
    #DFS - a list of dataframes from files
    dfs = []
    for filename in filenames:
        df = pd.read_csv(filename, delimiter = ";", index_col = None)
        dfs.append(df)
    return (dfs)
    # f_partner = "dim_partner.csv"
    # f_product = "dim_product.csv"
    # f_product_BASE_SRP = "dim_product_BASE_SRP.csv"
                # f_promotions = "dim_promotions.csv"
    # f_promotions = "fact_promotions.csv"

@st.cache(suppress_st_warning=True)
def load_dim_product():
    PATH = "C:\\Users\\o.georgievskiy\\Koch Media GmbH\\Internship - Oleg Georgievskiy - General\\Promo Tracker\\DWH_Dimensions\\"
    f_partner = "dim_partner.csv"
    f_product = "dim_product.csv"
    df = pd.read_csv(PATH+f_product)

def main():

#     hide_streamlit_style = """
# 	<style>
# 	/* This is to hide hamburger menu completely */ 3
# 	#MainMenu {visibility: hidden;}
# 	/* This is to hide Streamlit footer */
# 	footer {visibility: hidden;}
# 	/*
# 	If you did not hide the hamburger menu completely,
# 	you can use the following styles to control which items on the menu to hide.
# 	*/
# 	ul[data-testid=main-menu-list] > li:nth-of-type(4), /* Documentation */
# 	ul[data-testid=main-menu-list] > li:nth-of-type(5), /* Ask a question */
# 	ul[data-testid=main-menu-list] > li:nth-of-type(6), /* Report a bug */
# 	ul[data-testid=main-menu-list] > li:nth-of-type(7), /* Streamlit for Teams */
# 	ul[data-testid=main-menu-list] > div:nth-of-type(2) /* 2nd divider */
# 		{display: none;}
# 	</style>
# """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # n_promo_cols = [
    #                     "Promo_ID" ,                    #0 Index?! not visible, internal. Oleg: Discuss with Carles about origination. Could be used to refer to previous Promos for ease of creating new one.               
    #                     "Promo_Name",                   #1
    #                     "Title_Series",                 #2 visible, drop-down. Oleg: Include regex search!
    #                     "Title",                        #3 visible, drop-down. Oleg: make dependent on "Title Series"
    #                     "Partner_Name",                 #4          
    #                     "Base_SRP",                     #5 visible, automatic. Discuss the source origin with Carles/Pierre.
    #                     "Discount",                     #6 
    #                     "DSRP",                         #7 visible, automatic. DSRP = Base SRP * Discount %
    #                     "Period_Start",                 #8
    #                     "Period_End",                   #9
    #                     "Publisher",                    #10 visible, automatic. Depends on what?                                           
    #                     "Added_by"                      #11 not visible, automatic. 
    # ]
    
    st.set_page_config(
        page_title = "Promo Tracker DB",
        page_icon = "🧊",
        layout="wide",
        initial_sidebar_state = "collapsed")

    hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
    st.markdown(hide_footer_style, unsafe_allow_html=True)

    data_df_promo = load_metadata_promo()
    dfs_dwh = load_metadata_dwh()
    # dim_partner = dfs_dwh[0]
    # dim_product = dfs_dwh[1]
    # dim_product_BASE_SRP = dfs_dwh[2]
    # dim_promotions = dfs_dwh[3]
    # fact_promot = dfs_dwh[4]

    #First screen with App/Page selection
    PAGES = {
    #"Log": promo_0,
    "New Promo X": promo_x,
    "New Promo": promo_1,
    "Promo Overview": promo_2,
    "Promo DB": promo_3
    }

    st.info('Hello! This is an app to handle and view Promos!')
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", options = list(PAGES.keys()))
    page = PAGES[selection]


    st.sidebar1 = st.sidebar.empty()
    st.sidebar2 = st.sidebar.empty()
    st.sidebar3 = st.sidebar.empty()
    st.sidebar4 = st.sidebar.empty()
    st.sidebar5 = st.sidebar.empty()
    st.sidebar6 = st.sidebar.empty()

    pams = (
        "Raquel",  #Microsoft
        "Lorenzo", #EPIC
        "Simone",
        "Kenji",   #PSN, Nintendo

    )

    #st.sidebar.selectbox("Added_by", options = list(data_df_promo.Added_by.unique()),key= 'sb_user')
    st.sidebar.selectbox("Added by", options = pams,key= 'sb_user')
    # if "user_name" not in st.session_state:
    #     st.session_state.user_name = sb_u

    sb_user = st.session_state.sb_user
    #st.sidebar1.write(st.session_state)

    dim_partner = dfs_dwh[0]#.set_index(dfs_dwh[0]["dwh_id_dlpartner"])
    sb_partner = st.sidebar2.selectbox("Partner", options = list(dim_partner.name),key = 'sb_partner')#, on_change= promo_1.clear_session(st.session_state))
    #sb_partner = st.sidebar2.selectbox("Partner", options = list(data_df_promo.Partner_Name[data_df_promo.Added_by.isin([sb_user])].unique()),key = 'sb_partner')#, on_change= promo_1.clear_session(st.session_state))
    #sb_p = st.sidebar2.selectbox("Partner", options = list(data_df_promo.Partner_Name[data_df_promo.Added_by.isin([st.session_state.user_name])].unique()))
    # if "partner_name" not in st.session_state:
    #     st.session_state.partner_name = sb_p

    dim_product = dfs_dwh[1]#.set_index(dfs_dwh[1]["dwh_id_dlpartner"])
# ['dwh_id_dlproduct',
#  'product_id',
#  'dwh_id_dlpartner',
#  'dwh_id_product',
#  'product_name',
#  'title_id',
#  'title_name',
#  'content_type',
#  'platform',
#  'product_release_date',
#  'publisher',
#  'ips_project_code',
#  'ips_project_title',
#  'ips_project_label']

    #FIND how to use numerical values insteead of applying new column 
    #dim_product.join(dim_partner["name"]).rename(columns = {"name":"partner_name"})

    #FIND and add Partner Name based on its id of another df
    dim_product["partner_name"] = dim_product.apply(lambda x: dim_partner[(dim_partner.dwh_id_dlpartner == x.dwh_id_dlpartner)].values[0][1], axis=1)
    sb_ts = st.sidebar3.selectbox("Franchise", options = list(dim_product.ips_project_title[(dim_product.partner_name.isin([sb_partner]))].unique()),key = 'sb_ts')
    # sb_ts = st.sidebar3.selectbox("Franchise", options = list(data_df_promo.Title_Series[(data_df_promo.Partner_Name.isin([sb_partner]))&(data_df_promo.Added_by.isin([sb_user]))].unique()),key = 'sb_ts')
    #sb_ts = st.sidebar3.selectbox("Title Series", options = list(data_df_promo.Title_Series[data_df_promo.Partner_Name.isin([st.session_state.partner_name])].unique()))
    # if "title_series" not in st.session_state:
    #     st.session_state.title_series = sb_ts

    sb_new = st.sidebar4.checkbox("Add New Title", key = 'sb_new', value = False)
    copy_promo = st.sidebar5.checkbox("Copy Promo Campaign", key = 'copy_promo', value = False)

    #st.sidebar6.write(st.session_state)

    if page == promo_x:
        # all_data = pd.concat([data_df_promo,df], keys = data_df_promo.columns)
        df = page.app(data_df_promo,dfs_dwh)
        print (df)
    # elif page == promo_1:
    #     df = page.app(data_df_promo,dfs_dwh)
    #     print (df)
    # elif page == promo_2: 
    #     page.app(data_df_promo,dfs_dwh)
    # elif page == promo_3:
    #     page.app(data_df_promo,dfs_dwh)

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

# def login(data_df_promo, user, password, partner):
#     if (user, password, partner) not in data_df_promo.Added_by.unique():
#         #return (user, password, partner)
#         return (user, password, partner), False
#     else:
#         return (user, password, partner), True
    
# def create_new_user():
#     with st.form("User registration"):
#         user = st.text_input("Enter your name")
#         password = st.text_input("Enter your passport")
#         partner = st.text_input("Enter Partner")
#         button = st.form_submit_button("Submit")
#     if button:
#         return (user,password,partner),True

# with st.form("Login Page"):
    # user = st.text_input("Enter your name")
    #session_state = st.session_state.get()
    # st.session_state.user = st.selectbox("Added_by", options = list(data_df_promo.Added_by.unique()))
    # st.session_state.password = st.text_input("Enter your passport")
    # st.session_state.partner = st.selectbox("Partner", options = list(data_df_promo.Partner_Name[data_df_promo.Added_by.isin([st.session_state.user])].unique()))
    # st.session_state.registration = st.button("Add new member or assign Partner")
    # st.session_state.button = st.button("Login")
    # st.write(st.session_state.button)
    # if st.session_state.registration:
    #     if "log" not in st.session_state:
    #         st.session_state.log = create_new_user(data_df_promo,st.session_state.user,st.session_state.password,st.session_state.partner)

    # if st.session_state.button:
    #     if "log" not in st.session_state:
    #         st.session_state.log = login(data_df_promo,st.session_state.user,st.session_state.password,st.session_state.partner)
    #     if st.session_state.log[1]:
    #         st.write(st.session_state.log[1])
    #         st.write(st.session_state.log[0])

if __name__ == '__main__':
    main()

# # Piping one st.cache function into another forms a computation DAG.
# summary_type = st.selectbox("Type of summary:", ["sum", "any"])
# metadata = load_metadata()
# summary = create_summary(metadata, summary_type)
# st.write('## Metadata', metadata, '## Summary', summary)

    # print (****ABB.iloc[ABB.index.get_loc('2001-05-09') + 1]*****)
    # df2.loc[:,"Column Name"] - extracrt a column - possible to do .mean(), .sum()....
    # df2[["Column 1","Column2","Column 3"] - extracrt specific columns 
    # df2["Column Name"] - specific column
    # df2.loc["Row Name/Index",:] - specific row
    # df2[1:3] - specific rows
    # df2["Row","Column"] - specific cell


# button press to start vomputations
# arg_1 = st.some_widget(...)
# arg_2 = st.some_widget(...)
# ...

# @cache_on_button_press('Submit')
# def some_long_computation(arg_1, arg_2, ...)
#    ... # <- some long computation

# return_value = some_long_computation(arg_1, arg_2, ...)
# # do something with the return value


# info = st.expander("+")
#         with info:
#               st.markdown("""*
#               Takes one of more columns out of the dataset so these columns do not appear in the results.
#               *""")


# import perfplot

# plt.figure(figsize=(10, 10))
# plt.title('Quantitative Comparison of Filtering Speeds')
# perfplot.show(
#     setup=random_array,
#     kernels=[loop, boolean_index, loop_numba, boolean_index_numba],
#     n_range=[2**k for k in range(2, 22)],
#     logx=True,
#     logy=True,
#     equality_check=False,
#     xlabel='len(df)')

# from os import listdir
# from os.path import isfile, join
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]

# DataFrame Manipulations
# cities = [city for city, df in all_data.groupby('City')]


# df = all_data[all_data['Order ID'].duplicated(keep = False)]
# df['Grouped'] = df.grouby('Order ID')['Product'].transform(lambda x:','.join(x))  - concatenates items in Product column for each Order Id. DUPLICATES!
# df = df[['Order Id','Product]].drop_duplicates()

# product_group = all_data.groupby('Product')
# quantity_ordered = product_group.sum()['Quantity']
# product = [product for product,df in product_group]
# plt.bar(product,quantity_ordered)
# plt.ylabel('')
# plt,xticks(products, rotation ='vertical', size = 8)
# plt.show()

# Counting unique pairs of numbers into a python dictionary
# from  itertools import combinations
# from collections import Counter
# count = Counter()
# for row in df['Grouped']:
#     row_list = row.split(',')
#     count.update(Counter(combinations(row_list,2)))

# for key, value in count.most_common(10):   - most_common function
#     print (key,value)

# #Secondary Y axis
# prices - all_data.groupby('Product').mean()['Price']
# fig, ax1 = plt.subplots()
# ax2=ax1.twinx()
# ax1.bar(products,quantity_ordered)
# ax2.plot(products,prices,'b-')
# ax1.setxlabel('')
# ax1.set_ylabel('')
# ax2.set_ylabel('',color = 'b')
# ax1.set_xticklabels(product,rotation = 'vertical',size = 8)