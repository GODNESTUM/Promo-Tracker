### streamlit version == 0.83

#import apps (pages)
#from streamlit.state.session_state import SessionState
# from altair.vegalite.v4.schema.core import TitleAnchor
# from streamlit.state.session_state import SessionState
import promo_1
import promo_2
import promo_3
#import other libraries
import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import base64
# import io

@st.cache(suppress_st_warning=True)
def load_metadata():
    DATA_URL = "C:\\Users\\o.georgievskiy\\Koch Media GmbH\\Internship - Oleg Georgievskiy - General\\Promo Tracker\\Promo_Old_c.csv"     
    df = pd.read_csv(DATA_URL, delimiter = ";", index_col="Promo_ID")   #check for delimiter in csv or other file format adjust accordingly
    df["Period_Start"] = pd.to_datetime(df["Period_Start"],infer_datetime_format = True)
    df["Period_End"] = pd.to_datetime(df["Period_End"],infer_datetime_format = True)
    return df
    #return df.set_index("Promo ID")

# @st.cache
# def create_summary(metadata, summary_type):
#     one_hot_encoded = pd.get_dummies(metadata[["frame", "label"]], columns=["label"])
#     return getattr(one_hot_encoded.groupby(["frame"]), summary_type)()




def main():

#     hide_streamlit_style = """
# 	<style>
# 	/* This is to hide hamburger menu completely */
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
    #                     "Added_by"                      #11 not visible, automatic. Oleg: Implement Login/Sign-up functionality.
    # ]
    
    st.set_page_config(
        page_title = "Promo Tracker DB",
        #page_icon = "🧊",
        layout="wide",
        initial_sidebar_state = "collapsed")

    hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
    st.markdown(hide_footer_style, unsafe_allow_html=True)

    data_df = load_metadata()
    #First screen with App/Page selection
    PAGES = {
    #"Log": promo_0,
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

    

    sb_user = st.sidebar.selectbox("Added_by", options = list(data_df.Added_by.unique()),key= 'sb_user')
    # if "user_name" not in st.session_state:
    #     st.session_state.user_name = sb_u

    sb_partner = st.sidebar2.selectbox("Partner", options = list(data_df.Partner_Name[data_df.Added_by.isin([sb_user])].unique()),key = 'sb_partner')
    #sb_p = st.sidebar2.selectbox("Partner", options = list(data_df.Partner_Name[data_df.Added_by.isin([st.session_state.user_name])].unique()))
    # if "partner_name" not in st.session_state:
    #     st.session_state.partner_name = sb_p

    sb_ts = st.sidebar3.selectbox("Title Series", options = list(data_df.Title_Series[(data_df.Partner_Name.isin([sb_partner]))&(data_df.Added_by.isin([sb_user]))].unique()),key = 'sb_ts')
    #sb_ts = st.sidebar3.selectbox("Title Series", options = list(data_df.Title_Series[data_df.Partner_Name.isin([st.session_state.partner_name])].unique()))
    # if "title_series" not in st.session_state:
    #     st.session_state.title_series = sb_ts
    
    #sb_t = st.sidebar4.selectbox("Title", options = list(data_df.Title[data_df.Title_Series.isin([sb_ts])].unique()),key = 'sb_t')
    # if "title" not in st.session_state:
    #     st.session_state.title = sb_t

    #session_values = st.session_state.user_name, st.session_state.partner_name, st.session_state.title_series, st.session_state.title

    sb_new = st.sidebar5.checkbox("Add New Title", key = 'sb_new')

    if page == promo_1:
        # all_data = pd.concat([data_df,df], keys = data_df.columns)
        df = page.app(data_df)
        print (df)
        # gc_data_unpivoted.reset_index()
        # gc_data_unpivoted = pd.concat([gc_data_unpivoted, gc_data_cagr_3y],ignore_index=True,axis=0,sort=False)
    if page == promo_2: 
        page.visualize(data_df)
    if page == promo_3:
        page.show_table(data_df)

def login(data_df, user, password, partner):
    if (user, password, partner) not in data_df.Added_by.unique():
        #return (user, password, partner)
        return (user, password, partner), False
    else:
        return (user, password, partner), True
    
def create_new_user():
    with st.form("User registration"):
        user = st.text_input("Enter your name")
        password = st.text_input("Enter your passport")
        partner = st.text_input("Enter Partner")
        button = st.form_submit_button("Submit")
    if button:
        return (user,password,partner),True

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

# with st.form("Login Page"):
    # user = st.text_input("Enter your name")
    #session_state = st.session_state.get()
    # st.session_state.user = st.selectbox("Added_by", options = list(data_df.Added_by.unique()))
    # st.session_state.password = st.text_input("Enter your passport")
    # st.session_state.partner = st.selectbox("Partner", options = list(data_df.Partner_Name[data_df.Added_by.isin([st.session_state.user])].unique()))
    # st.session_state.registration = st.button("Add new member or assign Partner")
    # st.session_state.button = st.button("Login")
    # st.write(st.session_state.button)
    # if st.session_state.registration:
    #     if "log" not in st.session_state:
    #         st.session_state.log = create_new_user(data_df,st.session_state.user,st.session_state.password,st.session_state.partner)

    # if st.session_state.button:
    #     if "log" not in st.session_state:
    #         st.session_state.log = login(data_df,st.session_state.user,st.session_state.password,st.session_state.partner)
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


# info = st.beta_expander("+")
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